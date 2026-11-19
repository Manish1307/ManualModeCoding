#!/usr/bin/env python3
"""Write a side-by-side HTML comparison of two versions of a file.

Usage: diff_report.py BEFORE AFTER [-o OUTPUT.html] [--title TEXT] [--context N]
Without --context the whole file is shown; with it, only N lines around each change.
"""
import argparse
import difflib
import html
import sys

STYLE = """
body{font-family:Segoe UI,Arial,sans-serif;margin:16px;color:#222}
h1{font-size:18px;margin:0 0 6px}
.meta{margin:0 0 12px;color:#555;font-size:13px}
.key span{display:inline-block;padding:2px 8px;margin-right:6px;border-radius:4px;font-size:12px}
table.diff{border-collapse:collapse;width:100%;font-family:Consolas,Menlo,monospace;font-size:12px}
table.diff td{padding:1px 6px;vertical-align:top;white-space:pre-wrap;word-break:break-word}
table.diff th{background:#eee;padding:6px;font-size:13px;text-align:left}
td.diff_header{color:#999;text-align:right;background:#fafafa;width:34px}
td.diff_next{display:none}
.diff_add{background:#dcf5dc}.diff_chg{background:#fff1c2}.diff_sub{background:#fbdcdc}
"""


def read_lines(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read().splitlines()


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("before")
    ap.add_argument("after")
    ap.add_argument("-o", "--output", default="comparison.html")
    ap.add_argument("--title", default=None)
    ap.add_argument("--context", type=int, default=None)
    args = ap.parse_args(argv)

    try:
        a, b = read_lines(args.before), read_lines(args.after)
    except OSError as e:
        print(f"Cannot read input: {e}", file=sys.stderr)
        return 1

    sm = difflib.SequenceMatcher(None, a, b)
    added = removed = changed = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "insert":
            added += j2 - j1
        elif tag == "delete":
            removed += i2 - i1
        elif tag == "replace":
            changed += max(i2 - i1, j2 - j1)

    table = difflib.HtmlDiff(tabsize=2, wrapcolumn=100).make_table(
        a, b, "Before", "After",
        context=args.context is not None, numlines=args.context or 0)
    title = args.title or f"{args.before} vs {args.after}"
    page = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'><title>" + html.escape(title) + "</title>"
        "<style>" + STYLE + "</style></head><body>"
        "<h1>" + html.escape(title) + "</h1>"
        f"<p class='meta'>Before: {len(a)} lines. After: {len(b)} lines. "
        f"About {added} added, {removed} removed, {changed} changed.</p>"
        "<p class='key'><span class='diff_add'>added</span><span class='diff_chg'>changed</span>"
        "<span class='diff_sub'>removed</span></p>" + table + "</body></html>"
    )
    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(page)
    except OSError as e:
        print(f"Cannot write {args.output}: {e}", file=sys.stderr)
        return 1
    print(f"Wrote {args.output} ({added} added, {removed} removed, {changed} changed)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
