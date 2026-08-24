# 01 — harness

The loop and everything around it: control flow, tool interface, termination, budgets,
verification, and the blast radius of a wrong run.

## Tasks

| # | Task | State |
|---|------|-------|
| 01 | [agent-and-workflow](./01-agent-and-workflow/) | open |

## The question this module keeps asking

Where does a given property live — in the prompt, or in the code? Anything that must hold
regardless of what the model outputs belongs in the harness. Everything the model is merely
*asked* to do is a preference, and preferences are not guarantees.
