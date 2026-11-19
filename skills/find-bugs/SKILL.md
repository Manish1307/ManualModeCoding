---
name: find-bugs
description: >
  This skill should be used when the user asks to "find bugs", "review this code for bugs",
  "audit this code", "what could go wrong in this code", "check for errors", or "is this code safe"
  and wants a report without changes. It produces a severity-ranked list of real defects, each with
  a concrete failure scenario and a suggested fix, and never edits the code. Works for any language.
metadata:
  version: "0.1.0"
---

# Find bugs (review only)

Review code and report real defects. Do not edit any file. To fix the findings afterwards, use the
harden-code skill.

## Workflow

1. Identify the language and framework. Read the target code and enough of its surroundings
   (callers, helpers, configuration) to know how data enters and leaves it.
2. Work through `${CLAUDE_PLUGIN_ROOT}/skills/harden-code/references/bug-checklist.md`. For Power
   Pages, Dataverse, Liquid or Power Automate code also use
   `${CLAUDE_PLUGIN_ROOT}/skills/harden-code/references/power-pages.md`.
3. For each candidate defect, confirm it before reporting:
   - Trace the path: which input or state reaches the faulty line?
   - Write the failure scenario in one sentence: "When X, Y happens instead of Z."
   - When cheap, prove it: run the code with that input, or run
     `${CLAUDE_PLUGIN_ROOT}/skills/harden-code/scripts/check_syntax.py` for syntax errors.
   - Drop it if no reachable path exists. Style preferences are not bugs.
4. Rank by severity: Critical (security, data loss, credentials), High (wrong results or crashes on
   realistic input), Medium (edge cases, limits, encoding), Low (misleading code that will cause bugs
   later).

## Report format

Start with one line: how many findings by severity, or "No defects found" with what was checked.

Then one entry per finding, most severe first:

- **Severity**, file and line
- **What's wrong**: one sentence
- **When it fails**: the concrete scenario
- **Fix**: a short code snippet or instruction
- **Confidence**: Confirmed (reproduced or traced end to end) or Likely (traced, not run)

Finish with:

- **Checked**: the categories and files reviewed.
- **Not checked**: anything out of reach (live services, other files, runtime configuration).

Never say the code is "bug-free". Say "No defects found in the checked categories" instead.

If the session offers a structured findings tool for code reviews, report through it as its
instructions say; otherwise use the format above.
