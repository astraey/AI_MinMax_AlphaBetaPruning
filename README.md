# Artificial-Intelligence P2

Joan Branch

fichero multiagents

preguntas 1 a 3


algoritmos minmax, Alpha-beta prunning y Expectimax

minmax:


Step 1: Build your game tree

Starting from the current board generate all possible moves your opponent can make. Then for each of those generate all the possible moves you can make. For Tic-Tac-Toe simply continue until no one can play. In other games you'll generally stop after a given time or depth.

This looks like a tree, draw it yourself on a piece of paper, current board at top, all opponent moves one layer below, all your possible moves in response one layer below etc.

Step 2: Score all boards at the bottom of the tree

For a simple game like Tic-Tac-Toe make the score 0 if you lose, 50 tie, 100 win.

Step 3: Propagate the score up the tree

This is where the min-max come into play. The score of a previously unscored board depends on its children and who gets to play. Assume both you and your opponent always choose the best possible move at the given state. The best move for the opponent is the move that gives you the worst score. Likewise, your best move is the move that gives you the highest score. In case of the opponent's turn, you choose the child with the minimum score (that maximizes his benefit). If it is your turn you assume you'll make the best possible move, so you choose the maximum.

Step 4: Pick your best move

Now play the move that results in the best propagated score among all your possible plays from the current position.

Try it on a piece of paper, if starting from a blank board is too much for you start from some advanced Tic-Tac-Toe position.

Using recursion: Very often this can be simplified by using recursion. The "scoring" function is called recursively at each depth and depending on whether or not the depth is odd or even it select max or min respectively for all possible moves. When no moves are possible it evaluates the static score of the board. Recursive solutions (e.g. the example code) can be a bit trickier to grasp.
