---
name: harden-code
description: >
  This skill should be used when the user asks to "harden this code", "make this code bug free",
  "add error handling", "add exception handling", "improve this code", "make this production ready",
  "fix the bugs in this file", or "clean up and verify this code". It finds real defects, adds error
  handling where failures can actually happen, simplifies the code, verifies behaviour is unchanged,
  and shows a side-by-side diff that is applied only after the user approves. Works for any language.
metadata:
  version: "0.1.0"
---

# Harden code

Improve a piece of code so it fails less, fails clearly when it must, and is easier to read, without
changing what it does except where a confirmed bug is being fixed. Deliver a before/after comparison
and a verification result, and change the user's file only after they approve.

Never promise "bug-free" or "zero errors". Report exactly what was checked, how, and what was not
checked. Confidence comes from evidence, not from the claim.

## Inputs

- Code: a pasted snippet, an attached file, or a path in the workspace / connected folder.
- Optional: a file the team wrote by hand, to copy its style (see the humanize-code skill).
- Optional: scope. Default is the whole snippet or file the user pointed at. For a large file, ask
  which part matters most before rewriting more than ~400 lines.

## Workflow

### 1. Understand before touching

1. Identify the language, runtime and framework from the code and its surroundings (imports, globals
   such as `$`, `Xrm`, `{% %}` Liquid tags, file extension).
2. Read the code around the target: callers, the helpers it uses, configuration, and how data enters
   and leaves. Do not rewrite a function whose callers have not been read.
3. Write down, privately, the current contract of each changed unit: inputs, outputs, side effects,
   thrown errors, DOM/IDs/CSS classes/API names it relies on. These must survive the rewrite.
4. If the language is Power Pages / Dataverse portal code, also read `references/power-pages.md`.

### 2. Find defects

Work through `references/bug-checklist.md` against the code. For each finding record:
severity (Critical / High / Medium / Low), the line, a concrete failure scenario (input or state that
triggers it, and what goes wrong), and the fix. Drop anything without a concrete failure scenario:
style preferences are not bugs.

Treat these as Critical and stop to tell the user before continuing: secrets or credentials in
client-side code, user-controlled values reaching SQL/HTML/shell/URLs unescaped, authorization done
only in the browser, and data-loss paths (delete/overwrite without a guard).

### 3. Plan the error handling

Read `references/error-handling.md` for the language. Then apply these rules:

- Add handling only where a failure can really happen: network/API calls, file and database I/O,
  parsing external data, user input, optional DOM elements, third-party calls, numeric edge cases.
- Every handler must do something useful: recover with a stated fallback, retry a transient failure
  with a limit, or surface a clear message and log the detail. Never swallow an error silently.
- Catch the narrowest error type the language allows. Re-throw what cannot be handled here.
- Keep one user-facing message per failure; put technical detail in the log, not in the UI.
- Clean up resources (`finally`, `using`, `with`, `defer`) and re-enable UI controls on every path.
- Do not wrap code that cannot fail. Defensive layers for impossible states are noise.

### 4. Rewrite

- Preserve every public name, ID, CSS class, API field, message text and output format unless the
  user asked to change it or a listed bug requires it.
- Fix the confirmed bugs from step 2. Keep each fix minimal and traceable to its finding.
- Simplify: split functions that do several jobs, remove duplication with small helpers, replace
  nested ternaries and very long lines, use early returns. Keep the language level the project uses
  (for example ES5 with `var` if the file uses it; do not introduce a build step).
- Before adding a helper name, search the file/project to confirm the name is free.
- Comments explain *why*, not *what*. Remove comments that narrate the code.

### 5. Verify

Read `references/verification.md` and run every check available for the language:

1. Syntax/compile check. Use `scripts/check_syntax.py <file>`; it picks the right checker per
   extension (including `<script>` blocks inside HTML and Liquid templates).
2. The project's own linter, type checker and tests, when present.
3. Behaviour equivalence: run the old and new version on the same inputs and compare outputs (unit
   harness, or a headless browser for DOM code with mocked APIs). Cover the normal path, empty input,
   and each error path that was added.
4. If a check cannot run (missing runtime, needs live credentials), say so in the report. Never
   report a check as passed that did not run.

If verification shows a difference that is not one of the intended bug fixes, fix the rewrite and
verify again.

### 6. Report and ask

Generate the comparison with `scripts/diff_report.py <before> <after> -o <name>-comparison.html`
and send it to the user. Then give a short report:

- **Bugs fixed**: one line each, with severity and the failure scenario.
- **Error handling added**: where, and what happens now when it fails.
- **Cleanup**: the main structural changes.
- **Verification**: each check and its result; anything not verified and why.
- **Behaviour changes**: only the intended ones (bug fixes). If none, say "none".

End by asking whether to apply the changes. Do not modify the user's file before they say yes.
Write the rewritten version to a separate output file and send it, so the user can review it.

### 7. Apply (after approval)

1. Re-read the target file. If it changed since step 1, stop and re-run on the new version.
2. Replace only the reviewed block or file. Keep line endings and encoding.
3. Re-run the syntax check on the written file and confirm the size/marker the user can look for.

## Output files

- `<name>.hardened.<ext>`: the rewritten code.
- `<name>-comparison.html`: side-by-side diff (green added, yellow changed, red removed).

## Additional resources

- `references/bug-checklist.md`: defect categories to check, by severity.
- `references/error-handling.md`: idiomatic patterns per language.
- `references/verification.md`: how to check syntax, run tests and prove equivalence per language.
- `references/power-pages.md`: Power Pages, Dataverse Web API, Liquid and Power Automate specifics.
- `scripts/check_syntax.py`: syntax checker for many languages, including script blocks in HTML.
- `scripts/diff_report.py`: side-by-side HTML diff report.
