# lab_strings : The Scavenger Hunt (practice)

**Status:** warm-up, not a scored mission. No shard. It is here so `strings` stops
feeling strange. This file is an example of the shape your real writeups should
take. Yours can be shorter.

## How I got in

There is no password on this one. The job is to find the readable text hidden in
the file. First I just ran it to see what it says:

    ./missions/x86_64/lab_strings

It printed a banner and said "Nine hidden things. Go get them." So the program
only shows a couple of them when it runs, and keeps the rest to itself. That is
the whole point of the lab: a string can live inside a program without the program
ever printing it.

So instead of running it, I read the file itself:

    strings missions/x86_64/lab_strings

That dumped a wall of text, most of it library junk. I filtered for the lines that
actually read like English:

    strings -n 8 missions/x86_64/lab_strings | less

## What the tool showed me

The planted lines were sitting right there in the dump, mixed into the noise. I
could tell the real ones from the junk because they read like sentences a person
wrote. There was also an obvious trap: one very long line that basically brags
about being long on purpose and admits it is useless. Good reminder that the
longest string is not the important one.

(I am not pasting the nine here. Finding them is the exercise, and future-me does
not need the list, future-me needs to remember the trick.)

## What clicked

`strings` reads the file on disk. Running the program only shows you what the
program *decides* to show. Two different views of the same file, and the gap
between them is where the interesting stuff hides. Every mission after this one is
some version of that gap.

## Time

About 15 minutes, most of it scrolling and muttering "is that one real."
