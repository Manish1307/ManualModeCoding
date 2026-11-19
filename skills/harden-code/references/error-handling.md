# Error handling by language

Rules that apply everywhere: handle only failures that can happen; catch the narrowest type; do
something useful in every handler (recover, retry with a limit, or surface a clear message and log the
detail); always restore UI/resources; never swallow.

## JavaScript (browser, ES5 / jQuery)

```js
// Promise chain at the boundary of a user action
$("#btnSave").prop("disabled", true);
saveRecord(payload)
  .then(function () { showToast("Saved.", "success"); })
  .catch(function (err) {
    console.error("Save failed:", err);
    showToast(err && err.message ? err.message : "Could not save. Please try again.", "error");
  })
  .then(function () { $("#btnSave").prop("disabled", false); }); // runs on both paths
```

- `$.ajax` returns a jqXHR: use `.done/.fail/.always`, or wrap in a Promise. Read `xhr.status` and
  `xhr.responseJSON` for the message.
- Use `.then(ok, fail)` to handle one step's failure without catching earlier ones.
- Guard optional DOM: `if (!document.getElementById("x")) return;`.
- Validate external JSON shape before use: `Array.isArray(rows) ? rows : []` only when an empty result
  is a valid outcome; otherwise reject with a clear error.
- Escape for HTML (`esc()` / `textContent`) and for OData strings (`value.replace(/'/g, "''")`).
- `localStorage`/`sessionStorage` can throw (quota, privacy mode): wrap in `try/catch`.

## JavaScript / TypeScript (modern, Node)

```ts
async function loadUser(id: string): Promise<User> {
  const res = await fetch(`/api/users/${encodeURIComponent(id)}`);
  if (!res.ok) throw new HttpError(res.status, await res.text());
  return parseUser(await res.json()); // throws ValidationError on bad shape
}

try {
  const user = await loadUser(id);
  render(user);
} catch (err) {
  if (err instanceof HttpError && err.status === 404) return renderNotFound();
  logger.error({ err, id }, "loadUser failed");
  throw err; // let the framework's error boundary handle the rest
}
```

- `fetch` does not reject on 4xx/5xx: check `res.ok`.
- Use `AbortController` for timeouts. Use `finally` for cleanup.
- In Node, handle `error` events on streams and sockets. Never leave a promise without a handler.
- TypeScript: narrow `unknown` errors (`err instanceof Error ? err.message : String(err)`).

## Python

```python
try:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    log.warning("Config %s missing, using defaults", path)
    data = DEFAULTS
except json.JSONDecodeError as e:
    raise ConfigError(f"{path} is not valid JSON: {e}") from e
```

- Catch specific exceptions; never bare `except:`. Use `raise ... from e` to keep the cause.
- Use context managers for files, locks, connections. `requests`: set `timeout=` and call
  `raise_for_status()`.

## C# / .NET

```csharp
try
{
    using var response = await client.GetAsync(url, ct);
    response.EnsureSuccessStatusCode();
    return await response.Content.ReadFromJsonAsync<Order>(cancellationToken: ct)
        ?? throw new InvalidDataException("Empty order payload");
}
catch (HttpRequestException ex) when (ex.StatusCode == HttpStatusCode.NotFound)
{
    return null;
}
```

- `using` / `await using` for disposables. Use exception filters (`when`). Pass `CancellationToken`.
- Dataverse plugins: throw `InvalidPluginExecutionException` with a user-safe message; trace detail with
  `ITracingService`. Never let a raw exception reach the user.

## Java

- try-with-resources for `AutoCloseable`. Catch checked exceptions where they can be handled; wrap in a
  domain exception otherwise (`throw new ServiceException("...", e)`). Do not catch `Throwable`.

## Go

```go
f, err := os.Open(path)
if err != nil {
    return fmt.Errorf("open config %s: %w", path, err)
}
defer f.Close()
```

- Check every `err`. Wrap with `%w`. Use `errors.Is/As`. Do not panic for expected failures.

## PowerShell

- `$ErrorActionPreference = 'Stop'` or `-ErrorAction Stop` so `try/catch` sees non-terminating errors.
  Catch specific types (`[System.Net.WebException]`). Use `finally` to clean up.

## SQL (T-SQL)

```sql
BEGIN TRY
    BEGIN TRANSACTION;
    -- statements
    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
    THROW;
END CATCH;
```

- Parameterise queries. Use `XACT_ABORT ON` for multi-statement transactions.

## Shell (bash)

- `set -euo pipefail`; quote variables; `trap 'cleanup' EXIT`; check commands that may legitimately
  fail with `if ! cmd; then ...; fi`.
