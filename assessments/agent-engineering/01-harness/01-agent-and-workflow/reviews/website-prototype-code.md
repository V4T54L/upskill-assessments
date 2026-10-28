# Website prototype code review and validation

2026-10-28; self-review, not an independent assessment.

Findings resolved during implementation:

- Expected filter text may already exist before filtering. Rejecting its initial
  presence falsely failed a correct menu. Compare the visible container state
  before/after instead; still require the specified result substring.
- Playwright text assertions default to textContent, which includes CSS-hidden
  children. Use innerText for visible state assertions. Added a hide-in-place
  filtering fixture and a static/no-op negative fixture.
- Repeated full drafts inflate repair costs. Keep the latest complete HTML and
  latest screenshots, while retaining prior decisions and tool feedback.
- Finish without inspection, or after modifying a verified file, is invalid.
  Regression tests cover both gates and exhaustion without completion.

Evidence:

- Full suite: 12 tests passed in 47.606s, including four real browser fixtures.
  Working fixtures accepted: 2/2. Broken/static fixtures rejected: 2/2. Every
  browser fixture covers 1440x1000 and 390x844. This tiny sample does not estimate
  checker accuracy on arbitrary generated sites. Eight offline tests were rerun
  after adding HTML-history compaction coverage.
- Gemini model: gemini-3.5-flash-lite. Designer: 1 generation, 3,018 reported
  input/output tokens, 10.71s. An initial DNS failure was retried explicitly.
- First builder run stopped after 6,927 tokens because the local budget could
  not accommodate the next accumulated input. A subsequent run stopped at
  98,261 tokens after repeated repairs triggered by the checker issues above.
  Its page passed browser checks, but its agent run correctly remained failed
  because no completion decision fit the remaining budget.
- Final run with corrected checker: write_html -> inspect -> finish, one HTML
  revision, 25,634 reported input/output tokens, 80.01s. All desktop/mobile
  structure, overflow, JS/resource and two interaction checks passed. Ceiling:
  8 steps, 60,000 tokens, 180 seconds. The user's .env was not changed.
- Local artifacts: runs/validation-20261028/brief.json and
  runs/validation-20261028/site-final/{index.html,report.json,run.json,desktop.png,mobile.png}.

Remaining limitations: screenshots cover viewport-sized initial views, not every
scroll position/state; full accessibility and content fidelity are not established;
CDNs require network access; browser inspection depends on Playwright/Chromium or
installed Chrome. Provider usage can differ from preflight token reservations.
No comparative architecture benchmark or exercise-step completion is claimed.
