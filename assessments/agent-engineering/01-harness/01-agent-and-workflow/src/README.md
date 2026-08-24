# src/

The implementation lives here. It is written by hand, on purpose.

## Why there is no scaffolding in this directory

The loop — the thing that decides whether to call a tool, dispatches it, feeds the result back,
and decides when to stop — is about fifty lines and it is the entire lesson. Generating it would
remove the only part of this exercise that teaches anything. A framework would hide the same
fifty lines behind a decorator.

So: no starter agent, no base classes, no framework. Start from an empty file.

## Suggested shape (not binding)

```
src/
├── workflow/     the fixed-control-flow version
├── agent/        the loop
├── tools/        what either one can call
└── shared/       provider client, config, budget accounting
```

Reorganise freely — but if the structure changes, say why in the progress entry. Layout is a
design decision like any other.
