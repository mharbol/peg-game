# Cracker Barrel Peg Game
Quick little Python program to backtrack and solve the Cracker Barrel peg game for an arbitrarily sized peg board.
Might come back and completely refactor it to be a full package with other geometries.
There are a lot of ways this project could go, but I am just going to leave it as is for now.
Minimal error checking on the arguments parser as this was mostly modeling the game for fun.
Simple enough to run the program, for example:

```bash
python peg_game.py 5
```

This should give an output of `Solution: 6 -> 1, 4 -> 6, 1 -> 4, 7 -> 2, 10 -> 3, 13 -> 4, 2 -> 7, 11 -> 4, 15 -> 13, 12 -> 14, 14 -> 5, 4 -> 6, 6 -> 1`.
