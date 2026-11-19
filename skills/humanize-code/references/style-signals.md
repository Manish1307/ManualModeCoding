# Signals of generated code, and what to do with them

| Signal | Example | Rewrite |
|---|---|---|
| Comment above every function restating its name | `// Loads the users` above `loadUsers()` | Delete it. |
| Long explanatory comment blocks | 4-line comment explaining why a filter exists | One line with the reason, or nothing if the code is clear. |
| Emphasis in comments | `NOT`, `IS`, `ALWAYS`, `NEVER`, `!!!` | Plain case. Keep a hard rule only where breaking it is a real bug. |
| "e.g." and parenthetical chains | `(e.g. just created (via Add))` | Drop the example unless it is the only way to understand the code. |
| Section banners everywhere | `// ---- HELPERS ----` for 10-line files | Keep banners only if the project uses them. |
| Over-long names | `loadDcContactsFromRolesFlowWithFallback` | Name the result, not the mechanism: `loadDcContacts`. |
| Defensive checks for impossible states | `if (!arr || !Array.isArray(arr) || arr.length === undefined)` on a value the code just built | Remove. Keep checks on external data. |
| Fallback chains nobody asked for | try A, then B, then C, then D | Keep the fallbacks that have a real failure behind them; document why in one line. |
| Everything in one expression | nested ternaries, 200-character lines | Early returns and named intermediate variables. |
| Identical micro-helpers | three functions that each wrap one call | Inline them, or merge into one helper. |
| Chatty user messages | "Please note that the operation could not be completed at this time." | "Couldn't save. Try again." |
| Emoji and decorative logging | `console.log('✅ Success!')` | Plain log lines with context, or none. |
| Uniform formatting that differs from the file | different quote style, indentation or `let` in a `var` file | Match the surrounding file. |

Keep what helps the next developer: a comment explaining a non-obvious business rule, a link to the
ticket or API doc, and names that match the domain language the team uses.
