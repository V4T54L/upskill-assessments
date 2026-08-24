# reviews

Critique of approach docs and of code, one file per review, named for what it reviewed
(`00-approach.md`, `02-code.md`).

A review here reports findings, not praise. It is written by someone whose job is to find what is
wrong with the work, and the useful output is a list of specific, checkable problems — each with
the concrete inputs or state that would make it fail. "Consider adding error handling" is not a
finding. "A tool raising inside the loop propagates and kills the run; the model never sees the
error and cannot adapt" is.

An empty findings list is a legitimate result and should be stated plainly rather than padded.

**Note:** this directory is public. It contains candid criticism of work in this repository and
nothing else — no assessment of the author, no learning history.
