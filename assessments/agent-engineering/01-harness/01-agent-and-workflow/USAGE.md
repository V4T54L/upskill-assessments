# Website prototype

Run commands from this task directory with the repository's virtualenv activated.
The root `.env` supplies `GEMINI_API_KEY`, `GEMINI_MODEL`, and optional run limits.
The defaults are 12 model decisions, 100,000 total input/output tokens and 300 seconds
per designer or builder invocation. Token counts include repeated conversation history;
preflight counts reserve output plus a protocol margin, with actual usage checked after
each response. Limits are local controls, not a provider billing guarantee.

```bash
pip install -r requirements.txt
python -m playwright install chromium

python -m src.workflow.designer "An editorial coffee shop site with tasting reservations" --output runs/brief.json
python -m src.agent.web_builder --brief-file runs/brief.json --output-dir runs/coffee
```

The builder can also read a JSON brief from stdin with `python -m src.agent.web_builder -`.
An installed Google Chrome is a fallback when Playwright Chromium is unavailable.
Use a fresh output directory for each run. CDN scripts and fonts require internet access.

Designer stdout contains JSON only, unless `--output` saves it to a file. Builder
progress/accounting goes to stderr. The Python functions remain
`generate_website_brief(description) -> str` (JSON) and `build_website(brief) -> str`
(HTML). The builder also saves `index.html`, `brief.json`, `desktop.png`, `mobile.png`,
`report.json`, and `run.json` under its output directory. Failed runs retain artifacts
for debugging; a file existing does not mean its run passed.

The designer makes one structured generation followed by Pydantic validation. The
builder chooses write/inspect/finish actions, retains conversation state, receives
screenshots and browser failures, and cannot finish without a passing inspection of
the current revision. Invalid actions and tool validation failures become feedback.
API failures and resource exhaustion stop the run; there are no hidden retries.
Superseded HTML drafts and old screenshots are removed from subsequent request
payloads while prior decisions and tool feedback are retained. A small `.env` token
budget can still stop a run after its first draft: the next request includes that
draft as input. Override a test run without editing `.env`, for example with
`MAX_TOKENS_PER_RUN=100000 python -m src.agent.web_builder --brief-file runs/brief.json`.

Browser checks cover document structure, required section IDs, desktop/mobile
overflow, JS exceptions, failed resources, and the brief's interactions. These are
smoke checks. They do not establish full accessibility, design quality, faithful
copy, or comprehensive behavior. The model evaluates screenshots subjectively;
checker accuracy still needs calibration on representative failures.

```bash
python -m unittest discover -s tests -v
RUN_BROWSER_TESTS=1 python -m unittest discover -s tests -v
```

No framework, deployment, backend, external shell tools, or automatic exercise-step
completion is included. No claim of an optimal architecture without comparative runs.
