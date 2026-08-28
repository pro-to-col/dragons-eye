# The Dragon's Eye: Field Office

Twelve locked programs, the book that teaches you to open them, and the Eye that
tells you when you got one right. No answers live in this repo. Just the doors,
the tools, and the place where you two work.

This is not a folder of files. It is a **field office**. The crackmes teach you
reverse engineering. Git teaches you how to be an engineer. You are going to
learn both here, and the second one is the one that pays you back for thirty
years.

---

## Rung one: get in the door (tonight)

Brand new Chromebook? Open **[COLD-BOOT.html](COLD-BOOT.html)** first. It walks
the whole machine setup and ends by pulling this repo down. Then come back.

Already set up? Here is the entire loop:

```
uname -m                                  # x86_64  or  aarch64  -> that is your <arch>
chmod +x missions/<arch>/*                # only needed if you unzipped instead of cloned
./missions/<arch>/m01_helloghost          # knock on door one. it is locked. good.
python3 checker/theeye.py 1               # when you are in, prove it to the Eye
python3 checker/theeye.py                 # see the whole board and your shards
```

Read the course (`book/Gillbert-and-the-Dragons-Eye.html`) to learn the reaches.
Crack a door, claim a shard, repeat. Twelve shards spell a phrase. Feed it to
`./missions/<arch>/final_gate` to finish the whole thing.

Mission 6 wants a keygen, not a password. Mission 11 wants three answers. The
Eye knows and will ask you the right way. Wiped and starting fresh?
`python3 checker/theeye.py reset`.

---

## Rung two: ship your work like an engineer

Finding the password is not the mission. **Shipping the work** is the mission.
Every door you open, you leave three things behind:

1. **The crack**: how you got in.
2. **The writeup**: in your own words, in `writeups/`. See the readme in there.
3. **The code**, when there is any: your keygen for mission 6, a solver script,
   your patch notes for the anti-debug ones.

You do that on a **branch per mission**, and you open a **pull request**. Your
handler reviews it, asks you the one question that proves you actually understood
it, and merges it in. That review loop is the whole point of using git for real.
The full ritual is in **[FIELD-MANUAL.md](FIELD-MANUAL.md)**. Read it once you have
a mission or two under your belt.

Track the whole campaign in **[MISSIONS.md](MISSIONS.md)**.

---

## What is in here

| Folder | What it is |
|---|---|
| `COLD-BOOT.html` | First-boot setup. Open in a browser. |
| `setup.sh` / `setup-ghidra.sh` | Provision the machine. `setup.sh` installs the base tools and checks them; `setup-ghidra.sh` installs Ghidra and its Java later, when the book says it is time. |
| `book/` | The course. Open `Gillbert-and-the-Dragons-Eye.html` in a browser. Works offline. |
| `missions/` | The twelve locked programs, three practice labs, and `final_gate`. Two builds: `x86_64/` (Intel) and `arm64/` (ARM). You use one. |
| `checker/` | **The Eye.** Checks an answer, never reveals one. |
| `writeups/` | Yours. One writeup per mission. Your portfolio starts here. |
| `FIELD-MANUAL.md` | How the two of you work in this repo. The branch-and-review loop. |
| `MISSIONS.md` | The campaign board. Twelve doors, check them off. |
| `.github/` | The pull request template and the robot that checks your homework. |

---

## When something looks broken

- **"cannot execute binary file" / "Exec format error"**: wrong architecture.
  Re-check `uname -m` and use the other `missions/` folder.
- **"Permission denied" running a mission**: run the `chmod +x` line above.
- **`python3: command not found`**: the Linux base tools are missing. COLD-BOOT
  has the one install line that fixes it.
- **The Eye can't find `fingerprints.json`**: run it from the top of the repo:
  `python3 checker/theeye.py`.

Properly stuck, tried the hint ladder in the book, still nothing? That is what
your handler is for. He has the map. He will not hand you the answer. He will get
you unstuck.

Now go open a door.
