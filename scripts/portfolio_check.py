#!/usr/bin/env python3
"""
Portfolio check  -  the robot that checks your homework.

On a mission branch or pull request it confirms two things:
  1. you left a writeup for the mission your branch is named after
  2. any python you committed alongside it at least compiles

It never reads answers or fingerprints. It only checks that you shipped the work.

  exit 0  ->  green, you shipped
  exit 1  ->  you forgot something, and it says what

See FIELD-MANUAL.md, "the robot that checks your homework."
"""
import glob
import os
import py_compile
import re
import subprocess
import sys


def branch_name():
    # pull requests set GITHUB_HEAD_REF; pushes set GITHUB_REF_NAME
    for var in ("GITHUB_HEAD_REF", "GITHUB_REF_NAME"):
        v = os.environ.get(var)
        if v:
            return v
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True
        ).strip()
    except Exception:
        return ""


def mission_num(branch):
    m = re.search(r"(?:mission|m)[-_/]?0*([0-9]{1,2})", branch or "", re.I)
    if m:
        n = int(m.group(1))
        if 1 <= n <= 12:
            return n
    return None


def find_writeup(n):
    for d in ("writeups/mission-%02d" % n, "writeups/mission-%d" % n):
        if os.path.isdir(d):
            notes = os.path.join(d, "notes.md")
            if os.path.isfile(notes):
                return d, notes
            mds = sorted(glob.glob(os.path.join(d, "*.md")))
            if mds:
                return d, mds[0]
    for f in ("writeups/mission-%02d.md" % n, "writeups/mission-%d.md" % n):
        if os.path.isfile(f):
            return "writeups", f
    return None, None


def main():
    branch = branch_name()
    n = mission_num(branch)
    if n is None:
        print("[the eye] branch '%s' is not a mission branch. nothing to check. "
              "carry on." % (branch or "?"))
        return 0

    tag = "mission-%02d" % n
    folder, notes = find_writeup(n)
    if not notes:
        print("[the eye] RED. i don't see a writeup for %s." % tag)
        print("          make writeups/%s/notes.md and tell me how you got in," % tag)
        print("          then commit it and push again.")
        return 1

    try:
        text = open(notes, encoding="utf-8", errors="replace").read().strip()
    except Exception as e:
        print("[the eye] RED. couldn't read %s: %s" % (notes, e))
        return 1

    if len(text) < 120:
        print("[the eye] AMBER. %s exists but it's thin (%d chars)." % (notes, len(text)))
        print("          three real sentences minimum: how did you get in, and "
              "what clicked?")
        return 1

    broken = []
    scripts = sorted(glob.glob(os.path.join(folder, "**", "*.py"), recursive=True))
    for py in scripts:
        try:
            py_compile.compile(py, doraise=True)
        except py_compile.PyCompileError as e:
            last = (str(e).splitlines() or ["syntax error"])[-1]
            broken.append((py, last))
    if broken:
        print("[the eye] RED. code in %s doesn't compile:" % folder)
        for py, err in broken:
            print("          %s: %s" % (py, err))
        return 1

    extra = (" and %d script(s) that compile" % len(scripts)) if scripts else ""
    print("[the eye] GREEN. %s: writeup present (%d chars)%s. shipped."
          % (tag, len(text), extra))
    return 0


if __name__ == "__main__":
    sys.exit(main())
