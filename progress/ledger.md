# Progress ledger

Append-only. Newest last. Every entry carries a date, the domain, what was actually built or
measured, and the model id where a model was involved.

Corrections are appended, never applied in place.

---

## 2026-08-23 — repository opened

- **Domain:** — · **Task:** —
- Structure, working order and the step arc for `agent-engineering/01-harness/01-agent-and-workflow`
  set up. No code written, nothing measured.
- **Next:** step 00 — choose the problem and split it into the part that is a workflow and the
  part, if any, that genuinely needs an agent.

## 2026-10-28 — website designer and builder implementation

- **Domain:** agent-engineering · **Task:** 01-harness/01-agent-and-workflow
- User explicitly requested implementing both modules after earlier scaffold-only
  requests. Added a validated JSON design workflow, a bounded write/inspect/finish
  agent, shared Gemini usage accounting, browser verification, and usage docs.
  Layout follows the suggested workflow/, agent/, shared/ directories.
- **Model:** gemini-3.5-flash-lite. Final designer: 3,018 reported total tokens,
  10.71s, one generation. Final builder: 25,634 reported total tokens, 80.01s,
  three decisions, one HTML revision. Desktop/mobile checks and both interactions
  passed. Final builder ceiling: 8 decisions, 60,000 tokens, 180 seconds.
- **Failures retained:** initial DNS failure; builder budget stops at 6,927 and
  98,261 tokens. The latter exposed false failures for filtering hidden items.
  Corrected visible-text/state-change assertions and compacted obsolete drafts.
- **Checks:** 12 tests passed, including four real-browser fixtures. Two working
  fixtures accepted (2/2); two broken/static fixtures rejected (2/2), each on
  desktop and mobile. These are regression fixtures, not calibrated accuracy.
- Evidence and limitations: reviews/website-prototype-code.md within the task;
  ignored local artifacts under runs/validation-20261028/ in that task.
- **Next:** write the step-00 argument, calibrate independent checks on more
  representative failures, then compare the agent with a fixed build/verify
  workflow. No exercise step is marked complete by this implementation.
