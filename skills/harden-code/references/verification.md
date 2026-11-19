# Verification

Report every check honestly: passed, failed, or not run (with the reason).

## 1. Syntax / compile

Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/harden-code/scripts/check_syntax.py <file> [<file> ...]`.
It chooses a checker by extension and skips (with a message) when the tool is not installed:

| Extension | Checker |
|---|---|
| .js .mjs .cjs | `node --check` |
| .ts .tsx | `tsc --noEmit` (if installed) |
| .html .htm .liquid | every inline `<script>` block via `node --check`, after blanking Liquid `{% %}` / `{{ }}` |
| .py | `python -m py_compile` |
| .json | JSON parser |
| .sh | `bash -n` |
| .ps1 | PowerShell parser (if `pwsh` installed) |
| .php | `php -l` |
| .rb | `ruby -c` |
| .go | `gofmt -e` |
| .cs .java .sql | not checked by the script: build the project (`dotnet build`, `mvn -q compile`) or run the SQL in a transaction that is rolled back, if available |

Install a missing runtime only when it is quick (for example `npm i -g typescript`); otherwise report
"not run".

## 2. Project checks

Look for and run, when present: `npm test`, `npm run lint`, `pytest`, `dotnet test`, `mvn test`,
`go test ./...`, and the project's formatter in check mode. Run them before and after the change: a
test that already failed before is not caused by the rewrite, but say so.

## 3. Behaviour equivalence

Prove old and new behave the same on the same inputs.

- **Pure functions**: write a small harness that imports both versions and compares outputs for
  normal inputs, empty input, boundary values and each error path.
- **Browser / DOM code**: build two test pages (old and new) with the same mocked APIs and data, load
  both in a headless browser (Playwright/Chromium), drive the same clicks, and compare the rendered
  HTML and text of the affected regions. Mock network calls; never call live endpoints with real
  credentials.
- **Services**: run both against the same recorded requests or fixtures and compare responses.

Expected differences are only the intended bug fixes; list each one. Any other difference means the
rewrite is wrong: fix it and run again.

## 4. Error paths

For each handler that was added, force the failure in the harness (reject the mock, return 500,
remove the DOM element, pass malformed JSON) and confirm the documented outcome: message shown, state
restored, nothing left disabled or spinning, error logged.

## 5. What to say when something could not be verified

State it plainly, for example: "Not verified: the Dataverse calls run against mocks only; check one
real save in the dev environment." Never round "not run" up to "passed".
