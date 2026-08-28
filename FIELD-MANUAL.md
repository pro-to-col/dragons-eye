# Field Manual

How the two of you work in here. Read it once you have cracked a door or two and
the terminal has stopped feeling like a threat.

---

## The rule that makes this worth doing

Anyone can find a password. You could find some of these by accident. That is not
the skill, and it is not what your handler is grading.

The skill is being able to **explain how you got in, to someone who wasn't there,
well enough that they could do it themselves.** That is what separates a person
who reverse-engineered something from a person who guessed and got lucky. So in
this repo, a mission is not done when the door opens. It is done when the work is
committed, reviewed, and merged.

That is not busywork. That is the actual job. I have watched people who could
break anything and explain nothing. They do not get to build the interesting
things. Do not be them.

---

## The loop, one mission at a time

You do every mission on its own branch. This keeps your unfinished work off the
main line and gives your handler one clean thing to review.

**1. Start the branch.** Name it after the mission.

```
git switch -c mission-04
```

**2. Do the work.** Crack the door in your terminal. Then, in
`writeups/mission-04/`, leave your evidence:

- `notes.md`: how you got in, in your own words. Not a novel. The real steps.
- any code you wrote: `keygen.py`, `solve.py`, patch notes. If you wrote it to
  win, it belongs here.

**3. Commit it.** A commit is a save point with a sentence attached. Write the
sentence like you mean it.

```
git add writeups/mission-04
git commit -m "mission 04: xor lock, xored the blob to recover the key"
```

**4. Open it for review.** Push the branch and open a pull request.

```
git push -u origin mission-04
```

Then, on GitHub, click **Compare & pull request**. The template will ask you a
few questions. Answer them honestly. "I brute forced it" is a real answer and a
fine one, as long as it is true.

---

## What your handler does

He reviews the pull request. He is holding the answer key, so understand going
in: he can tell the difference between *understood* and *lucky*. That is the
point. He is not there to catch you. He is there to find the one spot where you
almost got it and ask you the question that pushes you the rest of the way.

He will leave a comment. Something like: *"You wrote that you XORed the blob and
the key fell out. How did you know which byte to XOR with, instead of one of the
other 255?"* You go find out. You answer in the thread. He approves, and he merges
your branch into `main`.

Now your work is part of the record, permanently, with your name on the commit.
Next mission, new branch. Twelve times.

**He never types the answer into your terminal.** If he does, tell him he broke
the rules. The deal is he asks better questions, not that he does your reps.

---

## The robot that checks your homework

There is a small automated check wired into `.github/`. When you open a mission
pull request, it looks at your branch and confirms you actually left a writeup for
that mission, and that any script you committed at least runs without a syntax
error. Green check: you shipped a real artifact. Red X: you forgot something, and
it tells you exactly what.

That is your first taste of **continuous integration**, which is a fancy phrase
for "a robot that runs your checks so a human does not have to." Every serious
software team on earth has one. Yours checks that you did the writeup. Chase the
green. It is the same green you will chase in every job you ever have.

Your handler decides whether a red X actually blocks the merge or just nudges you.
Ask him to make it block. You will thank yourself.

---

## Why any of this

One day, and it is sooner than you think, you are going to build something nobody
assigned you. When that day comes, the reverse engineering will be a tool on your
belt and the way you work, branch, commit, explain, review, ship, will just be how
your hands move. That is what this repo is actually teaching you. The dragon is
just the excuse.
