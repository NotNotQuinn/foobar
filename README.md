# foobar
[Google FooBar](https://foobar.withgoogle.com/) Challenges that I encountered.

This file is the only one that doesn't appear in the actual foobar site, which is a web-based cli sim.
For each challenge it seems there is a 7 day time limit.

I did most of my solutions in python (2.7, which is the only version availible) and used https://www.pythonsandbox.com/ to test my solutions easily.

## CLI

Typing `help` shows the following message:

```
Use the following shell commands:

cd		  - change directory [dir_name]
cat		  - print file [file_name]
deleteme  - delete all of your data associated with foobar
edit	  - open file in editor [file_name]
feedback  - provide feedback on foobar
less	  - print a file a page at a time [file_name]
ls		  - list directory contents [dir_name]
request	  - request new challenge
status	  - print progress
submit	  - submit final solution file for assessment [file_name]
verify	  - runs tests on solution file [file_name]

Keyboard help:

Ctrl + S  - save the open file [when editor is focused]
Ctrl + E  - close the editor [when editor is focused]

Toggle between the editor and terminal using ESC followed by TAB, then activate with ENTER.
```


## `journal.txt`

This file seems to grow in length as you progress in the challenges, and has messages that have shown up in the cli. I would assume this contains all story messages.
When you initially start it contains only this:


> Success! You've managed to infiltrate Commander Lambda's evil organization, and finally earned yourself an entry-level position as a Minion on their space station. From here, you just might be able to subvert Commander Lambda's plans to use the LAMBCHOP doomsday device to destroy Bunny Planet. Problem is, Minions are the lowest of the low in the Lambda hierarchy. Better buck up and get working, or you'll never make it to the top...

