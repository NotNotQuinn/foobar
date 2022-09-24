# foobar
[Google FooBar](https://foobar.withgoogle.com/) Challenges that I encountered.

This file is the only one that doesn't appear in the actual foobar site, which is a web-based cli sim.
For each challenge it seems there is a 7 day time limit, for challenges starting in level 4 the time limit is increased to 360 hours (15 days).

I did most of my solutions in python (2.7, which is the only version availible) and used https://www.pythonsandbox.com/ to test my trivial solutions, but ended up installing python 2.7 on my machine because the website doesn't show output until the program finishes, and some of my solutions took a while to run before optimizing them.

## CLI

Typing `help` shows the following message:

```
Use the following shell commands:

cd        - change directory [dir_name]
cat       - print file [file_name]
deleteme  - delete all of your data associated with foobar
edit      - open file in editor [file_name]
feedback  - provide feedback on foobar
less      - print a file a page at a time [file_name]
ls        - list directory contents [dir_name]
request   - request new challenge
status    - print progress
submit    - submit final solution file for assessment [file_name]
verify    - runs tests on solution file [file_name]

Keyboard help:

Ctrl + S  - save the open file [when editor is focused]
Ctrl + E  - close the editor [when editor is focused]

Toggle between the editor and terminal using ESC followed by TAB, then activate with ENTER.
```

## Jobs?

After reaching this point I was able to request my solutions be looked at by a recruiter (so long as I agreed to the [Applicant and Candidate Privacy Policy](https://careers.google.com/privacy-policy/)):

```
Level 1: 100% [==========================================]
Level 2: 100% [==========================================]
Level 3: 100% [==========================================]
Level 4:   0% [..........................................]
Level 5:   0% [..........................................]
```

Each "level" isn't just one problem. For example level 3 had 3 problems for me, and level 4 has 2 problems.

## `journal.txt`

This file seems to grow in length as you progress in the challenges, and has messages that have shown up in the cli. I would assume this contains all story messages.
When you initially start it contains only this:


> Success! You've managed to infiltrate Commander Lambda's evil organization, and finally earned yourself an entry-level position as a Minion on their space station. From here, you just might be able to subvert Commander Lambda's plans to use the LAMBCHOP doomsday device to destroy Bunny Planet. Problem is, Minions are the lowest of the low in the Lambda hierarchy. Better buck up and get working, or you'll never make it to the top...

## Copyright

I normally try to keep most of my work open-source and free to use under copyleft licenses, but that is not the case here:

> Challenges are copyright their respective owner(s), solutions are Copyright (c) QuinnDT and you may not use them as solutions to your own FooBar challenges.
