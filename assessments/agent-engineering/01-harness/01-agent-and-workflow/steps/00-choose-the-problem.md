# Task 00 — Choose the problem, and split it

**Status:** open
**Deliverable:** `approaches/00-choose-the-problem.md`
**Code written in this task:** none

---

## The assignment

Pick **one** real problem. Then argue, in writing, which parts of it are a **workflow** and
which — if any — genuinely need an **agent**.

The distinction that matters:

- A **workflow** is a system whose control flow *you* wrote. The steps are fixed, or branch in
  ways you enumerated in advance. Predictable, cheap, debuggable.
- An **agent** is an LLM that *directs its own control flow*: it decides which tool to call next
  and when it is finished. More capable, less predictable, and the expensive option — the
  transcript is re-sent every turn, so token cost grows with the square of the step count, not
  linearly.

An agent is justified only when **both** hold:

**(a) You genuinely cannot pre-write the control flow.** If you can draw every branch in advance,
you have proved it is a workflow. Build the workflow.

**(b) You can check the work against something better than the model's own opinion.** Without
that, autonomy does not buy correctness — it buys confidently wrong output, produced faster and
at higher cost. That is strictly worse than a workflow that fails loudly.

Most problems fail (a), (b), or both. **A well-argued "this should be a workflow" is a complete
and successful answer to this task**, and is worth more than an agent built to justify the word.

## Choosing well

Good candidates have all three of these:

- **You can tell right from wrong without asking a language model.** A test that runs, a schema
  that validates, a file that exists, a number that reconciles, a page that renders.
- **A wrong run is cheap.** Nothing irreversible, nothing anyone else sees, no production data.
- **You can get it working in a day.** The learning is in the harness, not the domain.

Avoid: summarisation, "research assistants", writing help, and anything whose output quality is a
matter of judgement. Not because they are unserious, but because they have no cheap independent
checker, which means task 03 will have nothing to measure and you will have learned nothing about
verification.

## What the approach doc must contain

Answer these in order. Each one blocks the next.

1. **The problem, in three sentences.** What goes in, what comes out, who would use it.

2. **The control-flow graph.** Draw it — ASCII is fine. Every step and every branch you can
   name in advance. Be honest about how much of it you *can* draw; that is the answer to (a),
   and it is usually more than expected.

3. **The split.** Which parts of that graph are fixed, and which genuinely cannot be enumerated?
   If everything is enumerable, say so and stop — you have a workflow, and that is the finding.

4. **🚧 The gate — fill in both blanks, concretely.**

   > *"Progress is checked by ___[1]___, which is independent of the agent because ___[2]___."*

   Blank [1] must be a specific mechanism you could point at in code, not a category. "Tests"
   is a category; "`pytest tests/test_extract.py`, exit code 0" is a mechanism.

   Blank [2] must explain why it cannot be talked into passing by the same thing that produced
   the output. A check the model performs on its own work fills neither blank.

   **If you cannot complete both blanks, do not proceed to task 02.** Either pick a different
   problem, or accept that the answer is "workflow" and say so.

5. **The checker's failure rate — how you would measure it.** You do not have to measure it yet.
   You do have to say what a false pass would look like, and how you would count them. A checker
   whose false-pass rate is unknown caps the accuracy of everything built on top of it at an
   unknown value — which is worse than a known-bad rate, because you will trust it.

6. **Blast radius.** List every side-effecting action the system will be able to take. For each:
   is it reversible, and what does a wrong run touch? Anything both irreversible and unverifiable
   does not get built in this repo.

7. **The cost sketch.** Rough token arithmetic for one run of each architecture, given the loop
   re-sends its whole transcript each step. Then check it against the current free-tier limits —
   requests per minute, requests per day, tokens per minute — and say whether your design can
   actually run inside them. If it cannot, that is a design constraint, not a surprise to be
   discovered at 3am.

## Acceptance criteria

- [ ] The control-flow graph is drawn, and the parts that cannot be enumerated in advance are
      explicitly marked as such.
- [ ] Both blanks in the gate are filled with a mechanism and a reason, or the doc concludes
      "workflow" and says why.
- [ ] The independent checker is something other than a language model judging its own output.
- [ ] Every side-effecting action is listed with its reversibility.
- [ ] Nothing both irreversible and unverifiable is in scope.
- [ ] The token arithmetic is shown, and checked against the current published free-tier limits.
- [ ] The recommendation is stated plainly, including "this should be a workflow" if that is
      where the reasoning lands.

## Out of scope

No code. No repository layout. No library choices. This task is the argument, and the argument
is easier to change now than after there is code resting on it.
