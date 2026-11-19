# code-hardener

A Claude plugin that makes code more reliable and easier to read, and proves it did not break
anything.

It finds real bugs, adds error handling where failures can actually happen, cleans up AI-sounding
code so it matches your project's own style, verifies the behaviour is unchanged, and shows a
side-by-side diff. Your files are changed only after you approve.

> No tool can guarantee code is bug-free. This plugin reports exactly what it checked and how, and
> says plainly what it could not verify.

## Skills

| Skill | Ask Claude something like | What it does |
|---|---|---|
| **harden-code** | "Harden this file", "add exception handling", "make this production ready" | Finds bugs, adds error handling, simplifies, verifies, shows a diff, applies on approval. |
| **find-bugs** | "Find bugs in this code", "audit this function" | Review only. Severity-ranked findings, each with a failure scenario and a fix. Never edits. |
| **humanize-code** | "Rewrite this like a normal programmer", "match our coding style" | Rewrites code to follow your codebase's conventions, behaviour unchanged, with a diff. |

## What "verified" means here

For every change the plugin runs, where available:

1. **Syntax check** for the language (`node --check`, `py_compile`, `bash -n`, `php -l`, `tsc`,
   and inline `<script>` blocks inside HTML and Liquid templates).
2. **Your project's own tests and linters**.
3. **Behaviour equivalence**: old and new code run on the same inputs (a test harness, or a headless
   browser with mocked APIs for front-end code) and their output compared.
4. **Forced failures** for each error handler that was added.

Anything that could not run is listed as "not verified".

## Languages

Any language. Detailed guidance is included for JavaScript (ES5/jQuery and modern), TypeScript,
Python, C#/.NET, Java, Go, PowerShell, T-SQL and shell, plus Microsoft Power Pages, Dataverse Web API,
Liquid and Power Automate.

## Included scripts

- `skills/harden-code/scripts/check_syntax.py FILE...`: picks the right syntax checker per file and
  reports PASSED / FAILED / SKIPPED (never "passed" when the checker is missing).
- `skills/harden-code/scripts/diff_report.py BEFORE AFTER -o out.html`: side-by-side HTML diff.

Both need only Python 3 (standard library). Language checkers are used if installed.

## Install

Claude Code (2.1.275 or later), after you publish this repository on GitHub:

```
/plugin install code-hardener --marketplace Manish1307/ManualModeCoding
```

Claude app: install the `code-hardener.plugin` file from the GitHub release.

## Example

> Harden `src/orders.js`. Use `src/customers.js` as the style reference.

Claude reads both files, lists the bugs it found, writes `orders.hardened.js` and
`orders-comparison.html`, reports what was verified, and asks before replacing `src/orders.js`.

## Contributing

Issues and pull requests are welcome, especially new language guides in
`skills/harden-code/references/error-handling.md` and checkers in `check_syntax.py`.

## License

MIT. See [LICENSE](LICENSE).
