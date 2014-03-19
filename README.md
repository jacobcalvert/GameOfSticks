GameOfSticks
=========================================
This is a project for a Computer Science class
at the University of Alabama. For an introduction
to the Game of Sticks, see the PDF document. The
approach I took essentially involved in creating
a base class that 'ran' the game, and subsequently
subclassing the different modes I would need to
support. This worked rather efficiently as I only
needed to override a few methods for each type.
The game includes an AI component which was designed
according to the project spec.

Game Modes
=========================================

* Human vs. Human - self explanatory, you choose the umber of sticks
and play against a friend.

* Human vs. AI - you have the option of playing against a naive AI or
having the AI trained against itself for a set number of games. The default
training loops is set to 10^5 (100,000). This completes in a few seconds.

* AI vs AI - you can watch the AI play against itself.