"""Offline control-flow tests; set RUN_BROWSER_TESTS=1 for real Chromium fixtures."""

import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from google.genai import types
from pydantic import ValidationError

from src.agent import web_builder as builder
from src.shared.gemini import BudgetExceeded, GeminiRun
from src.workflow.designer import WebsiteBrief, generate_website_brief


def example_brief():
    return WebsiteBrief.model_validate({
        "title": "Coffee", "audience": "Neighbors", "primary_goal": "Reserve a tasting",
        "assumptions": ["One location"], "visual_direction": "Warm editorial cafe",
        "tokens": {"colors": {"background": "#fff", "text": "#111", "accent": "#943", "muted": "#555"},
                   "heading_font": "Georgia", "body_font": "Arial", "typography": {"h1": "48px/1.1"},
                   "spacing": [4, 8, 16, 32], "radius": "8px", "shadows": "none"},
        "sections": [{"id": name, "purpose": name, "heading": name, "content": [name], "layout": "stack"}
                     for name in ["hero", "booking"]],
        "responsive_rules": ["Stack on mobile", "Max-width on desktop"],
        "interactions": [{"name": f"Choose {value}", "behavior": "Show a delayed result",
                          "steps": [{"action": "click", "selector": f"#{value}"}],
                          "expected_selector": "#result", "expected_text": value}
                         for value in ["espresso", "filter"]],
        "acceptance_criteria": ["Responsive", "Keyboard accessible", "Functional booking"],
    })


GOOD_HTML = """<!doctype html><html lang="en"><head><title>Coffee</title>
<meta name="viewport" content="width=device-width, initial-scale=1"></head>
<body><main><section id="hero"><h1>Coffee</h1></section><section id="booking">
<button id="espresso">Espresso</button><button id="filter">Filter</button>
<p id="result" aria-live="polite">espresso filter</p></section></main><script>
for (const id of ['espresso', 'filter']) document.getElementById(id).onclick = async () => {
document.getElementById('result').textContent = 'Loading';
await new Promise(resolve => setTimeout(resolve, 50));
document.getElementById('result').textContent = id; };
</script></body></html>"""


class ContractTests(unittest.TestCase):
    def test_rejects_empty_description_without_api(self):
        with self.assertRaises(ValueError):
            generate_website_brief("  ")

    def test_rejects_duplicate_section_ids(self):
        data = example_brief().model_dump()
        data["sections"][1]["id"] = "hero"
        with self.assertRaises(ValidationError):
            WebsiteBrief.model_validate(data)

    def test_rejects_arbitrary_tool_action(self):
        with self.assertRaises(ValidationError):
            builder.Decision(action="shell", reason="Run code")


class BudgetTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, {"GEMINI_API_KEY": "offline-placeholder", "MAX_STEPS": "1",
                                         "MAX_TOKENS_PER_RUN": "5000", "MAX_WALLCLOCK_SECONDS": "10"})
        self.env.start()
        self.client_patch = patch("src.shared.gemini.genai.Client")
        self.client = self.client_patch.start().return_value
        self.client.models.count_tokens.return_value.total_tokens = 100
        self.client.models.generate_content.return_value = types.GenerateContentResponse(
            candidates=[types.Candidate(content=types.Content(parts=[types.Part.from_text(
                text='{"action":"finish","reason":"Done"}')]))],
            usage_metadata=types.GenerateContentResponseUsageMetadata(total_token_count=200),
        )
        self.run = GeminiRun()

    def tearDown(self):
        self.run.close()
        self.client_patch.stop()
        self.env.stop()

    def test_step_limit_prevents_another_request(self):
        self.run.ask([], builder.Decision)
        with self.assertRaises(BudgetExceeded):
            self.run.ask([], builder.Decision)
        self.assertEqual(self.client.models.generate_content.call_count, 1)

    def test_input_tokens_can_exhaust_budget_before_generation(self):
        self.client.models.count_tokens.return_value.total_tokens = 4900
        with self.assertRaises(BudgetExceeded):
            self.run.ask([], builder.Decision)
        self.client.models.generate_content.assert_not_called()

    def test_expired_deadline_prevents_network(self):
        self.run.deadline = 0
        with self.assertRaises(BudgetExceeded):
            self.run.ask([], builder.Decision)
        self.client.models.count_tokens.assert_not_called()


class AgentTests(unittest.TestCase):
    def run_decisions(self, actions, reports, directory):
        fake = MagicMock()
        fake.max_steps = len(actions)
        fake.calls = []
        fake.summary.return_value = {"model": "offline", "tokens": 0}
        def ask(*args):
            retained_drafts = [json.loads(message.parts[0].text).get("html") for message in args[0]
                               if message.role == "model"]
            count = retained_drafts.count(GOOD_HTML)
            self.assertLessEqual(count, 1)
            if any(action["action"] == "write_html" for action in fake.calls):
                self.assertEqual(count, 1)
            decision = actions[len(fake.calls)]
            fake.calls.append(decision)
            return types.GenerateContentResponse(candidates=[types.Candidate(content=types.Content(
                parts=[types.Part.from_text(text=json.dumps(decision))]))])
        fake.ask.side_effect = ask
        with patch.object(builder, "GeminiRun", return_value=fake), patch.object(
                builder, "inspect_website", side_effect=reports):
            return builder.build_website(example_brief().model_dump_json(), Path(directory))

    def test_repair_and_stale_inspection_gate(self):
        write = {"action": "write_html", "reason": "Build", "html": GOOD_HTML}
        inspect = {"action": "inspect", "reason": "Verify"}
        finish = {"action": "finish", "reason": "Done"}
        actions = [finish, write, inspect, write, inspect, write, finish, inspect, finish]
        reports = [{"passed": False, "viewports": [], "errors": ["Broken interaction"]},
                   {"passed": True, "viewports": []}, {"passed": True, "viewports": []}]
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(self.run_decisions(actions, reports, directory), GOOD_HTML)
            trace = json.loads((Path(directory) / "run.json").read_text())
            self.assertEqual(trace["status"], "passed")
            self.assertEqual(trace["verified_revision"], 3)
            errors = [step["feedback"] for step in trace["trace"] if "feedback" in step
                      and "tool_error" in step["feedback"]]
            self.assertEqual(len(errors), 2)  # Premature finish and stale inspection.

    def test_step_exhaustion_does_not_return_unverified_html(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(BudgetExceeded):
                self.run_decisions([{"action": "write_html", "reason": "Build", "html": GOOD_HTML}], [], directory)
            self.assertEqual(json.loads((Path(directory) / "run.json").read_text())["status"], "failed")


@unittest.skipUnless(os.getenv("RUN_BROWSER_TESTS") == "1", "Set RUN_BROWSER_TESTS=1")
class BrowserTests(unittest.TestCase):
    def test_accepts_filter_that_hides_items_without_removing_them(self):
        with tempfile.TemporaryDirectory() as directory:
            page = Path(directory) / "index.html"
            html = GOOD_HTML.replace('>espresso filter</p>', '><span>espresso</span> <span>filter</span></p>')
            html = html.replace("document.getElementById('result').textContent = 'Loading';", "")
            html = html.replace("document.getElementById('result').textContent = id;",
                                "for (const span of document.querySelectorAll('#result span')) "
                                "span.style.display = span.textContent === id ? '' : 'none';")
            page.write_text(html)
            report = builder.inspect_website(page, example_brief(), timeout=60)
            self.assertTrue(report["passed"], report)

    def test_accepts_working_interactions_on_both_viewports(self):
        with tempfile.TemporaryDirectory() as directory:
            page = Path(directory) / "index.html"
            page.write_text(GOOD_HTML)
            report = builder.inspect_website(page, example_brief(), timeout=60)
            self.assertTrue(report["passed"], report)
            self.assertEqual(len(report["viewports"]), 2)

    def test_rejects_broken_interactions_on_both_viewports(self):
        with tempfile.TemporaryDirectory() as directory:
            page = Path(directory) / "index.html"
            page.write_text(GOOD_HTML.replace("textContent = id", "textContent = 'wrong'"))
            report = builder.inspect_website(page, example_brief(), timeout=60)
            self.assertFalse(report["passed"], report)
            self.assertTrue(all(view["failures"] for view in report["viewports"]), report)

    def test_rejects_static_expected_text_without_a_state_change(self):
        with tempfile.TemporaryDirectory() as directory:
            page = Path(directory) / "index.html"
            page.write_text(GOOD_HTML.replace("textContent = id", "textContent = 'espresso filter'"))
            report = builder.inspect_website(page, example_brief(), timeout=60)
            self.assertFalse(report["passed"], report)
            self.assertTrue(all(view["failures"] for view in report["viewports"]), report)


if __name__ == "__main__":
    unittest.main()
