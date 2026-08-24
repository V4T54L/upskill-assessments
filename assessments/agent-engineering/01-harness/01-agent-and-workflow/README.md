# Task 01 — Build an agent and a workflow

**Domain:** agent-engineering · **Module:** 01-harness
**State:** open · **Started:** 2026-08-23

## The assignment, as given

Build my own agent and a workflow, to gain confidence and on-ground experience.

## How this task is being met

Six steps, in order, each gating the next. The order is deliberate: it builds the **cheap,
predictable thing first**, then the expensive autonomous one, then makes the case for which was
actually justified. Building the agent first would allow skipping the only question that matters.

| # | Step | Gate it must pass |
|---|------|-------------------|
| **00** | [Choose the problem and split it](./steps/00-choose-the-problem.md) | What independently checks the output can be named, before any code exists. |
| **01** | [Build the workflow](./steps/01-build-the-workflow.md) | Fixed control flow, no loop. Cost per run measured, not estimated. |
| **02** | [Build the minimal agent](./steps/02-build-the-minimal-agent.md) | The loop is hand-written, and its termination condition is not "the model stopped asking for tools". |
| **03** | [Verify it](./steps/03-verify-it.md) | A real checker, with its hit rate on real failures reported separately from its hit rate on real successes. |
| **04** | [Bound it](./steps/04-bound-it.md) | Step, token and wall-clock ceilings enforced in code. A wrong run's reach is bounded and can be stated. |
| **05** | [Compare, and write the memo](./steps/05-compare-and-write-the-memo.md) | Both architectures on the same job, measured. A recommendation someone else could act on. |

Steps 01–05 are stubbed on purpose. Their detail depends on what step 00 concludes, and writing
them now would mean fixing the design before it exists.

## Working order — the gate is real

```
  1. read the step and its acceptance criteria
  2. write approaches/NN-<slug>.md — the design, BEFORE any code
  3. get the approach reviewed → reviews/
  4. build it in src/
  5. get the code reviewed against the same criteria → reviews/
  6. append the measurement to /progress/ledger.md
```

**Step 2 is a gate, not paperwork.** No code is written until the approach doc has been
reviewed. A design defended in advance and then attacked is worth more than one
reverse-engineered from whatever got built, and it is far cheaper to change.

## What "acceptance criteria" means here

Criteria are pass/fail and checkable by someone who did not write the code. "Handles errors
gracefully" is not a criterion. "A tool that raises returns the error text to the model and the
run continues, demonstrated by a recorded trace" is.

If a criterion turns out to be wrong or impossible, change it in the step file and say why in the
progress entry. Silently failing a criterion and moving on is the one thing that makes this
record worthless.

## Environment

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

The API key comes from `.env` at the repository root. It is gitignored and must stay so — this
repository is public.
