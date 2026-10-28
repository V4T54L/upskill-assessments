# Website prototype implementation

2026-10-28. The user explicitly requested implementation of the designer and
builder, following an earlier request for scaffolding only. This scope includes
the loop; it does not change the exercise instructions or close its steps.

Input is a topic/description, not a URL to crawl. Output is one self-contained
HTML page with Tailwind CDN, inline JavaScript, realistic mock content, and
asynchronous simulated interactions. CDN access is needed to render the page.

The designer is a fixed transformation: description -> JSON design brief ->
schema validation. The brief specifies visual tokens, content, responsive layout,
and executable interaction checks. No planner agent or extra model personas.

The builder chooses write_html, inspect, or finish in a hand-written loop. Tool
results and prior decisions are retained. Tools can only write index.html and
inspect that page; no shell or arbitrary file tools. Every write invalidates
verification. Finish requires a current passing browser report. Screenshots are
fed back to the model for visual judgement, which remains subjective.

Browser checks use Chromium at desktop/mobile widths, reject horizontal overflow
and JavaScript exceptions, and run the brief's interaction checks. Those checks
are fixed before the builder starts. They are useful smoke tests, not proof of
accessibility, visual quality, or semantic correctness; a flawed designer can
produce flawed acceptance checks. This design is wrong if those checks prove too
weak to catch representative broken pages, or repair adds no value over a fixed
generate-and-verify workflow. No claim of optimality without comparison runs.

Each run has request/step, generated-and-input token, and elapsed-time budgets.
Count content tokens before each request, reserve output tokens and a protocol
margin, disable SDK retries, and record actual usage. Provider-side tokenization
and request timeouts are not a transactional hard cost/real-time guarantee.
Browser work runs in a subprocess with the remaining time as its deadline.

Validation: offline schema and budget checks; scripted model decisions against
real browser fixtures for initial failure, repair, stale verification, and
interaction failures; then a small live end-to-end run if credentials/network
are available. Keep generated pages/reports under ignored runs/ directories.
