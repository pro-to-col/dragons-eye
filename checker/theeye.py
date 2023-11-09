#!/usr/bin/env python3
"""
THE EYE - answer checker for NULL QUEST vol.4

  python3 theeye.py          show the board
  python3 theeye.py 4        check your answer to mission 4
  python3 theeye.py reset    wipe your progress and start over

Nothing in this file spoils anything. The answers are stored as SHA-256
fingerprints, which is a one-way street. If you want to cheat you will have to
break a hash function, and honestly at that point you have earned it.
"""

import hashlib
import json
import os
import random
import signal
import sys

# so piping into head / less does not throw a wall of Python at a 12 year old
try:
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (AttributeError, ValueError):
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
SAVE = os.path.join(HERE, ".eye_progress")

SALT = b"null-quest-vol4-dragons-eye::"

def fp(text):
    return hashlib.sha256(SALT + text.strip().upper().encode()).hexdigest()

# mission number -> (title, what to type at the prompt)
MISSIONS = {
    1:  ("HELLO, GHOST",   "password"),
    2:  ("HAYSTACK",       "master password"),
    3:  ("THE ROT GATE",   "password"),
    4:  ("THE XOR LOCK",   "password"),
    5:  ("STACK GHOST",    "password"),
    6:  ("KEYFORGE",       "keygen"),
    7:  ("THE BACK ROOM",  "hidden menu number"),
    8:  ("LIVE WIRE",      "password"),
    9:  ("COLD START",     "response code"),
    10: ("WATCHDOG",       "passphrase"),
    11: ("THREE LOCKS",    "three parts"),
    12: ("THE VAULT",      "vault phrase"),
}

SHARDS = {
    1: "N", 2: "U", 3: "L", 4: "L", 5: "Y", 6: "V",
    7: "S", 8: "L", 9: "U", 10: "C", 11: "A", 12: "S",
}

# real fingerprints, filled in by tools/seal_answers.py
FINGERPRINTS = json.loads(open(os.path.join(HERE, "fingerprints.json")).read()) \
    if os.path.exists(os.path.join(HERE, "fingerprints.json")) else {}


def load():
    if os.path.exists(SAVE):
        try:
            return set(json.load(open(SAVE)))
        except Exception:
            return set()
    return set()


def save(done):
    json.dump(sorted(done), open(SAVE, "w"))


def keygen_challenge(done):
    """Mission 06 is not a password, it is an algorithm. So we test the
       algorithm: here is a name you have never seen, produce its key."""
    random.seed()
    name = random.choice(["GILFOYLE", "DINESH", "ERLICH", "JIANYANG", "MONICA",
                          "RICHARD", "BIGHEAD", "HOOLI", "LURDURBEAR", "MOLLY",
                          "CHARLIE", "NULLY", "HENDIX", "DUNDERHEAD"])
    print("\n  KEYFORGE does not have a password. It has an algorithm.")
    print("  So: forge a licence key for this operator.\n")
    print("    OPERATOR NAME:  %s\n" % name)
    print("  (Run your keygen on that name. Paste the number it gives you.)")
    try:
        given = input("\n  KEY> ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return False
    k = 0x1505
    for c in name:
        k = ((k * 33) & 0xFFFFFFFF) ^ ord(c)
    k &= 0x7FFFFFFF
    if given.isdigit() and int(given) == k:
        return True
    print("\n  Not that one. Check your loop: does it mask to 32 bits every")
    print("  multiply, and does it mask the final answer with 0x7FFFFFFF?\n")
    return False


def three_locks():
    print("\n  THREE LOCKS wants three answers, one per lock.\n")
    try:
        a = input("  lock 1, the command line argument > ").strip().upper()
        b = input("  lock 2, the NULLY_KEY value        > ").strip().upper()
        c = input("  lock 3, the word you type          > ").strip().upper()
    except (EOFError, KeyboardInterrupt):
        print()
        return False
    return fp(a + "|" + b + "|" + c) == FINGERPRINTS.get("11", "")


def board(done):
    print()
    print("  " + "=" * 58)
    print("   NULL QUEST vol.4     T H E   D R A G O N ' S   E Y E")
    print("  " + "=" * 58)
    print()
    for n in range(1, 13):
        title = MISSIONS[n][0]
        _ = title
        if n in done:
            print("   [%s]  %02d  %-16s  shard: %s" % ("X", n, title, SHARDS[n]))
        else:
            print("   [ ]  %02d  %-16s  shard: ?" % (n, title))
    print()
    got = len(done)
    bar = "#" * got + "." * (12 - got)
    print("   progress  [%s]  %d of 12" % (bar, got))
    print()
    if got == 12:
        phrase = "".join(SHARDS[n] for n in range(1, 13))
        print("   Every shard recovered. The phrase reads:\n")
        print("        %s\n" % phrase)
        print("   Feed it to ./final_gate and finish this.\n")
    else:
        print("   Next:  python3 theeye.py %d\n" % min(set(range(1, 13)) - done))


def main():
    done = load()

    if len(sys.argv) == 1:
        board(done)
        return

    arg = sys.argv[1].lower()

    if arg == "reset":
        if os.path.exists(SAVE):
            os.remove(SAVE)
        print("\n  Progress wiped. Every door locked again.\n")
        return

    if not arg.isdigit() or not (1 <= int(arg) <= 12):
        print("\n  usage: python3 theeye.py [1-12 | reset]\n")
        return

    n = int(arg)
    title, prompt = MISSIONS[n]
    print("\n  MISSION %02d : %s" % (n, title))

    if n == 6:
        ok = keygen_challenge(done)
    elif n == 11:
        ok = three_locks()
    else:
        try:
            ans = input("\n  %s> " % prompt)
        except (EOFError, KeyboardInterrupt):
            print()
            return
        ok = fp(ans) == FINGERPRINTS.get(str(n), "")

    if ok:
        was_new = n not in done
        done.add(n)
        save(done)
        print("\n  " + "-" * 46)
        print("   CONFIRMED.  SHARD %02d IS YOURS:   %s" % (n, SHARDS[n]))
        print("  " + "-" * 46)
        if was_new and len(done) == 12:
            print("\n   That was the last one.\n")
        board(done)
    else:
        print("\n  Not it. That is not a failure, that is data.")
        print("  If you are properly stuck, mission %02d has a hint ladder in the\n"
              "  book, and THE GHIDRA FILES has the full walkthrough.\n" % n)


if __name__ == "__main__":
    main()
