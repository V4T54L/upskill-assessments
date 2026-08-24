# assessments

One directory per **domain**. Inside a domain, one per **module**. Inside a module, one per
**task**. Directories are created when work on them starts, not in advance.

```
assessments/<domain>/<NN-module>/<NN-task>/
├── README.md        the assignment as given, and the plan for meeting it
├── steps/           the assignment broken into ordered, individually-gated pieces
├── approaches/      the design for each step, written BEFORE its code
├── reviews/         critique of the approaches and of the code
└── src/             the implementation, self-contained
```

## Why code lives inside the task

Each task is a self-contained project with its own dependency manifest — `requirements.txt`,
`go.mod`, `package.json`, whatever the language wants. Domains here will not share a runtime,
and a single top-level source root would have to pretend they do.

The cost is repetition across tasks. That is the intended trade: a task you can `cd` into and
run without reading three levels of parent configuration is worth more than deduplicated setup.

## Numbering

Modules and tasks are zero-padded and ordered (`01-`, `02-`). Steps within a task likewise.
Numbers are assigned when the work starts and never reused — a task that is abandoned keeps its
number and gets a closing note, because a gap in the sequence is a fact worth preserving.

## Progress

Per-task detail lives in the task. The **trajectory** lives in one place: `progress/ledger.md`
at the repository root, append-only, spanning every domain. Split ledgers make it impossible to
answer "what has actually been built and measured", which is the question this repository exists
to answer.
