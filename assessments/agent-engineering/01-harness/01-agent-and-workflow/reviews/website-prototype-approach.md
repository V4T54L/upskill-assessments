# Implementation approach review

2026-10-28. Self-review before implementation; not an independent assessment.

- A model's finish message alone cannot establish success. Require a passing
  browser inspection of the current HTML revision.
- A per-request token cap alone does not bound a multi-turn conversation. Count
  the entire accumulated input and reserve output before each generation.
- Infinite JavaScript can hang browser evaluation. Run inspection in a separate
  process that can be terminated at the remaining run deadline.
- A fixture-generated selector list can conceal missing behavior. Acceptance
  checks must come from the initial brief, not from the builder's finished HTML.
- The existing text-only helper cannot provide vision or usage metadata. Add a
  bounded JSON session while preserving generate(prompt) compatibility.
- Screenshots and smoke checks cannot prove good design. Report this limitation
  and do not mark the exercise or checker calibration complete.

Proceed with these requirements; measure rather than claim optimality.
