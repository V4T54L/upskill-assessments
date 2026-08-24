# upskill-assessments

A working record of a structured upskilling programme: the assignments, the design decisions
taken **before** the code, the reviews they survived, and what the measurements actually said.

Each domain gets its own directory; each is built the same way and held to the same standard.

## Domains

| Domain | What it covers | State |
|--------|----------------|-------|
| [agent-engineering](./assessments/agent-engineering/) | Building and operating LLM/agent systems — harness, evaluation, runtime. | in progress |

More are added as they start — system design, Go, agentic coding, UI/UX. Directories are created
when work begins, not reserved in advance.

## How work is done here

```
  1. TASK        read the assignment and its acceptance criteria
  2. APPROACH    write the design BEFORE any code
  3. REVIEW      the approach is critiqued and must pass
  4. BUILD       write the code
  5. REVIEW      the code is critiqued against the same criteria
  6. MEASURE     run it, record real numbers in progress/ledger.md
```

**Step 2 is a gate, not a formality.** No code is written for a step until its approach doc has
been reviewed. A design defended in advance and then attacked is worth more than one
reverse-engineered from whatever got built, and it is far cheaper to change.

## Layout

```
assessments/<domain>/<NN-module>/<NN-task>/
├── README.md      the assignment as given, and the plan for meeting it
├── steps/         the assignment broken into ordered, individually-gated pieces
├── approaches/    the design for each step, written before its code
├── reviews/       critique of the approaches and of the code
└── src/           the implementation, self-contained with its own dependency manifest

progress/ledger.md   append-only, spans every domain — the trajectory in one place
```

See [`assessments/README.md`](./assessments/README.md) for the conventions.

## Ground rules

- **Every claim carries its measurement.** "It's fast", "it works", "it's cheap" are not results.
  A number without the run that produced it is an opinion with a decimal point.
- **Never report a lone accuracy number** for anything that judges correctness. Report how often
  it catches real successes *and* how often it catches real failures, separately. A checker that
  approves everything scores well on a mostly-passing dataset while having never once caught a
  failure.
- **Record the model id and the date on every result.** Findings are bound to the model that
  produced them and to the day it was running.
- **An unmeasured limit is not a limit.** Rate limits, token budgets and step ceilings belong in
  the code as enforcement, not in the prompt as a request.
- **The ledger is append-only.** A record that can be tidied retroactively converges on a
  flattering story, and the failures are the part worth keeping.

## Setup

Per-task, because domains here do not share a runtime. Each task directory carries its own
dependency manifest and its own README.

The API key is read from `.env` at this root:

```bash
cp .env.example .env    # then fill it in
```

⚠️ **This repository is public.** `.env` is gitignored and must stay that way. Nothing committed
here should contain an API key, a customer name, or anything from an employer's codebase.
