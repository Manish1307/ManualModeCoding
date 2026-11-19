---
name: humanize-code
description: >
  This skill should be used when the user asks to "make this code look human written",
  "rewrite this like a normal programmer", "remove the AI style from this code", "match our coding
  style", "clean up AI-generated code", or "make this read like the rest of the codebase". It
  rewrites code to follow the project's own conventions with plainer comments, names and structure,
  keeps behaviour identical, verifies it, and shows a before/after diff before applying.
metadata:
  version: "0.1.0"
---

# Humanize code

Rewrite code so it reads like an experienced developer on this team wrote it by hand. Behaviour must
not change. The goal is consistency with the codebase and plain, maintainable code; it is not a
promise that any tool will classify the result as human-written.

## Workflow

### 1. Learn the house style

1. Ask for, or find, one or two files the team wrote by hand in the same language and area. If none
   are available, use the conventional style for the language and say so.
2. Note, from those files: naming (camelCase, prefixes, abbreviations), function size, comment
   density and tone, string quotes, `var`/`let`/`const`, promise style, jQuery vs DOM APIs, how errors
   and messages are shown, indentation and line length.
3. Read `references/style-signals.md` for the common signs of generated code.

### 2. Rewrite

- Keep every public name, ID, CSS class, API field, message text, output format and edge-case
  behaviour, unless the user asks to change them.
- Remove the generated-code signals: narrating comments, ALL-CAPS emphasis, "e.g." chains, defensive
  checks for impossible states, layers of fallbacks nobody asked for, over-long names, nested
  ternaries, one-line functions that do five things.
- Split functions that do several jobs; extract small helpers only when they remove real
  duplication. Search the project before adding a helper name to avoid collisions.
- Keep one comment where a decision is not obvious from the code, written the way the team writes.
- Stay at the project's language level. Do not modernise syntax unless the project already uses it.
- On-screen text: shorter and plainer, but only change it when the user agreed to text changes.

### 3. Verify

Follow `${CLAUDE_PLUGIN_ROOT}/skills/harden-code/references/verification.md`: syntax check with
`${CLAUDE_PLUGIN_ROOT}/skills/harden-code/scripts/check_syntax.py`, the project's tests if any, and a
behaviour-equivalence run comparing old and new on the same inputs. Any difference in output means
the rewrite is wrong; fix it and run again.

### 4. Report and ask

1. Create the comparison:
   `python3 ${CLAUDE_PLUGIN_ROOT}/skills/harden-code/scripts/diff_report.py BEFORE AFTER -o <name>-comparison.html`
   and send it with the rewritten file.
2. Summarise the main changes in a few bullets with short before/after snippets for the biggest ones.
3. State the verification result, including anything not verified.
4. Ask before writing to the user's file. When approved, re-read the target first and stop if it
   changed since the review.
