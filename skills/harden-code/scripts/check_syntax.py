#!/usr/bin/env python3
"""Syntax-check source files with the right tool for each extension.

Usage: check_syntax.py FILE [FILE ...]
Exit code: 0 if every file that could be checked passed, 1 if any check failed.
Files whose checker is not installed are reported as SKIPPED, never as passed.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

LIQUID = re.compile(r"\{%.*?%\}|\{\{.*?\}\}", re.S)
SCRIPT = re.compile(r"<script\b([^>]*)>(.*?)</script>", re.S | re.I)
NON_JS_TYPES = re.compile(r'type\s*=\s*["\'](?!text/javascript|application/javascript|module)[^"\']+["\']', re.I)


def run(cmd, label):
    tool = cmd[0]
    if not shutil.which(tool):
        return "SKIPPED", f"{label}: '{tool}' is not installed"
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return "FAILED", f"{label}: checker timed out"
    if p.returncode == 0:
        return "PASSED", label
    out = (p.stderr or p.stdout).strip()
    return "FAILED", f"{label}\n{out}"


def blank_liquid(text):
    # Replace Liquid tags with spaces of the same length so line numbers stay correct.
    return LIQUID.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)


def check_html(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        text = blank_liquid(f.read())
    blocks = [(m.start(2), m.group(2)) for m in SCRIPT.finditer(text)
              if not NON_JS_TYPES.search(m.group(1)) and "src=" not in m.group(1).lower() and m.group(2).strip()]
    if not blocks:
        return [("PASSED", f"{path}: no inline scripts")]
    results = []
    for start, code in blocks:
        line = text.count("\n", 0, start) + 1
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as tmp:
            tmp.write(code)
        try:
            status, msg = run(["node", "--check", tmp.name], f"{path}: <script> at line {line}")
            results.append((status, msg.replace(tmp.name, f"{path}:<script@{line}>")))
        finally:
            os.unlink(tmp.name)
    return results


def check_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            json.load(f)
        return [("PASSED", f"{path}: valid JSON")]
    except (OSError, ValueError) as e:
        return [("FAILED", f"{path}: {e}")]


CHECKERS = {
    (".js", ".mjs", ".cjs"): lambda p: [run(["node", "--check", p], p)],
    (".ts", ".tsx"): lambda p: [run(["tsc", "--noEmit", "--allowJs", "--skipLibCheck", p], p)],
    (".html", ".htm", ".liquid"): check_html,
    (".py",): lambda p: [run([sys.executable, "-m", "py_compile", p], p)],
    (".json",): check_json,
    (".sh", ".bash"): lambda p: [run(["bash", "-n", p], p)],
    (".ps1", ".psm1"): lambda p: [run(["pwsh", "-NoProfile", "-Command",
                                        f"$e=$null;[void][System.Management.Automation.Language.Parser]::ParseFile('{p}',[ref]$null,[ref]$e);if($e){{$e|%{{$_.ToString()}};exit 1}}"], p)],
    (".php",): lambda p: [run(["php", "-l", p], p)],
    (".rb",): lambda p: [run(["ruby", "-c", p], p)],
    (".go",): lambda p: [run(["gofmt", "-e", "-l", p], p)],
}


def check(path):
    if not os.path.isfile(path):
        return [("FAILED", f"{path}: file not found")]
    ext = os.path.splitext(path)[1].lower()
    for exts, fn in CHECKERS.items():
        if ext in exts:
            return fn(path)
    return [("SKIPPED", f"{path}: no syntax checker for '{ext}' (build or test the project instead)")]


def main(argv):
    if not argv:
        print(__doc__.strip())
        return 2
    failed = False
    for path in argv:
        for status, msg in check(path):
            print(f"[{status}] {msg}")
            failed = failed or status == "FAILED"
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
