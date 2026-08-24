# agent-engineering

Building and operating LLM/agent systems — the harness, the evaluation, the runtime.

This is the *building* side. It is distinct from wielding AI coding assistants effectively,
which is a different skill with different failure modes and gets its own domain if and when it
starts.

## Modules

| # | Module | State |
|---|--------|-------|
| 01 | [harness](./01-harness/) | in progress |

The harness is everything around the model that is written and controlled directly: the loop,
the tool definitions, the budgets, the gates, the validators. Not the prompt, and not the model.
A property enforced in the harness holds regardless of what the model decides; a property
requested in the prompt holds until the model decides otherwise.
