# Bug checklist

Check each category against the code. Record a finding only with a concrete failure scenario.

## Critical

- **Secrets in shipped code**: API keys, client secrets, passwords, connection strings or tokens in
  browser JavaScript, mobile apps, public repos or templates. Fix: move the call server-side (API,
  function, cloud flow) and tell the user to rotate the secret.
- **Injection**: user-controlled values concatenated into SQL, OData `$filter`, FetchXML, shell
  commands, file paths, HTML (`innerHTML`, `.html()`), URLs or regular expressions without escaping
  or parameterisation.
- **Client-only authorization**: permission checks done only in the browser, or identity taken from a
  query string / localStorage that the user can change.
- **Data loss**: delete or overwrite without confirmation, a guard, or a concurrency check; bulk
  operations that run on an empty filter (matching everything).

## High

- **Unhandled async failure**: promises without rejection handling, `async` without `try/catch` at
  the boundary, callbacks that ignore the error argument, fire-and-forget calls whose failure leaves
  state wrong.
- **Null / undefined / missing data**: optional DOM elements, empty API results, missing JSON fields,
  `[0]` on possibly empty arrays, division by zero.
- **Race conditions**: double submit (button not disabled), stale responses overwriting newer ones,
  shared mutable state between concurrent requests, check-then-act on remote data.
- **Wrong comparisons**: `==` vs `===`, comparing GUIDs/emails without normalising case and braces,
  floating-point equality, timezone-naive dates, off-by-one in ranges and pagination.
- **Resource leaks**: files, connections, streams, timers, event listeners or object URLs not released
  on every path.
- **Swallowed errors**: empty `catch`, catch-all that returns a default and hides a real failure,
  logging without surfacing anything to the caller.
- **Partial writes**: multi-step saves where a middle step fails and leaves inconsistent data with no
  rollback or retry.

## Medium

- **Pagination and limits**: assuming one page of results (`$top`, 5,000-row caps, `@odata.nextLink`).
- **Retry storms**: retrying non-transient errors or without a limit/backoff.
- **Encoding**: missing `encodeURIComponent`, wrong charset, unescaped quotes in OData strings (`'`
  must become `''`).
- **Locale and format**: parsing dates or numbers with the wrong culture; sorting with `<` instead of
  `localeCompare`.
- **Dead or unreachable code** that hides a logic error (a branch that can never run because an
  earlier condition already returned).
- **Inconsistent state after errors**: spinners left on, buttons left disabled, modals left open.

## Low

- Misleading names or comments that contradict the code.
- Duplicated logic that has already drifted between copies.
- Magic numbers that encode business rules without a name.

## Not bugs (do not report as bugs)

Formatting, naming taste, missing comments, "could use a newer syntax", or theoretical issues with no
reachable path. Mention them only as cleanup if the user asked for it.
