# Power Pages, Dataverse and Power Automate specifics

## Portal Web API (`/_api/...`)

- Writes need the anti-forgery token (`__RequestVerificationToken` header); use the project's wrapper
  (`webapi.safeAjax`, `CustomPost`, etc.) rather than raw `fetch` for POST/PATCH/DELETE.
- Every table and column used must be enabled in site settings (`Webapi/<table>/enabled`,
  `Webapi/<table>/fields`) and covered by a table permission for the user's web role. A 403 or an
  error code like 90040120 usually means a field is not in the allowed list; 90040102 a missing
  permission.
- Many-to-many expands (for example `powerpagecomponent_mspp_webrole_contact`) and virtual tables are
  often not supported. Prefer a cloud flow for those reads, with the Web API as a fallback.
- OData strings: escape `'` as `''`; `encodeURIComponent` the whole `$filter`. GUIDs in filters have
  no quotes. Lookups bind with `"field@odata.bind": "/entityset(guid)"`.
- Results are capped (`$top`, 5,000 rows). Follow `@odata.nextLink` when more may exist.
- Compare GUIDs after normalising (lower case, no braces) and emails after `trim().toLowerCase()`.

## Liquid

- `{{ }}` output is not HTML-escaped by default in every context: use `| escape` for user data, and
  never write user data into a `<script>` block without JSON encoding.
- Decisions that grant access (who may see a page or record) belong in Liquid/web roles/table
  permissions on the server, not in JavaScript.

## Cloud flows called from the portal

- HTTP-trigger URLs with a SAS signature are callable by anyone who has them. Keep them in one
  configuration snippet, validate inputs in the flow (for example allowed email domains), and return
  only the data the page needs.
- Never put client secrets or tokens in page code. Graph or other API calls with credentials belong
  in the flow (HTTP action with Active Directory OAuth, secret from Key Vault or a secret environment
  variable, Secure inputs/outputs on).
- Handle flow failure in the page: show a clear message, keep the UI usable, log `xhr.status`.
- The Response action must run after failed steps too (Configure run after) if partial results are
  expected.

## UI state

- Disable submit buttons during saves and re-enable them on every path (success, failure, validation
  return).
- Hide progress overlays in `finally`/`.always`.
- Re-render lists after writes from the server's data, not from local assumptions.
