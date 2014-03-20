###################################################
# File:         GameModes.py
# Author:       Jacob Calvert
# Date:         03/14/2014
# Description:  This file contains the abstract
# definition of the game of sticks as well as three
# derived game modes that implement the various
# necessary functions.
# Hosted:       https://github.com/jacobcalvert/GameOfSticks.git
###################################################
import random
ALTERNATE_OP = 0             # see alternate AI operation method in AI.lost
AI_TRAINING_LOOPS = (10**5)  # number of training loops for Human vs AI. 10^5 = 100,000


class AbstractGoS:
    """
    AbstractGoS: this is the abstract class that defines the basic structure
    of the game of sticks. Methods that must be overridden for it to work are
    notify, get_player_choice, inform_of_sticks
    """
    PTYPE_HUMAN = 0  # player types - I'm using them like enums almost
    PTYPE_AI = 1

    def __init__(self, init_stick, p1_type=PTYPE_HUMAN, p2_type=PTYPE_HUMAN):
        self._p1 = {"type":p1_type,"name":""}
        self._p2 = {"type":p2_type,"name":""}
        self._initsticks = init_stick
        self.__next = self._p1  # we always start with player 1

    def game_loop(self, quiet=False):
        #  This is the meat of the game. This 'gameloop' is inherited by each game type and the appropriate methods
        #  are overridden. The basic flow is this. While there are still sticks on the board do the following:
        #       a) Inform the current player of the number of sticks left on the board
        #       b) Get that player's choice of sticks to take
        #       c) Check that number of sticks chosen for proper bounds and notify if not.
        #       d) If the (sticks left - sticks chosen) is 0 then notify the appropriate player that won, break loop
        #       e) Else reduce the stick pool by that amount, set the player variable to the next player and loop again
        #
        #  You will notice there is quiet variables for each method which default to 'False'. When set to true, these
        #  methods do not generate console output. This is used in the AI training. We set the quiet to True and run
        #  the gameloop N times to train it.
        sticks = self._initsticks
        player = self.__next = self._p1
        while sticks:

            self.inform_of_sticks(sticks, player,quiet)
            choice = self.get_player_choice(player)
            if sticks - choice < 0:
                self.notify({"msg-type":"error","msg":"Cannot make this choice"}, player,quiet)
            elif sticks - choice == 0:
                self.notify({"msg-type":"winner","who":self.next_player()}, player,quiet)
                break
            else:
                player = self.next_player()
                sticks -= choice
            print() if not quiet else None

    def notify(self, what, who=None, quiet=False):
        pass  # must be overridden

    def get_player_choice(self, player):
        return 0  # must be overridden

    def inform_of_sticks(self, num_sticks, who=None,quiet=False):
        pass  # must be overridden

    def next_player(self):
        if self.__next == self._p1:
            self.__next = self._p2
        else:
            self.__next = self._p1
        return self.__next


class HumanVHuman(AbstractGoS):

    """
    HumanVHuman: this class is derived from AbstractGoS and fills
    in the appropriate methods for a human vs human game of sticks
    """
    def __init__(self, init_sticks):
        AbstractGoS.__init__(self,init_sticks)
        self._p1["name"] = "Player 1"
        self._p2["name"] = "Player 2"

    def notify(self, what, who=None, quiet=False):
        if what["msg-type"] == "error":
            print (what["msg"])

        if what["msg-type"] == "winner":
            print (what["who"]["name"] + " has won!\n")

    def inform_of_sticks(self, num_sticks, who=None,quiet=False):
        print ("There are %d sticks on the table." % (num_sticks))

    def get_player_choice(self, player):
        num = 0
        while 1:
            num = int(input(player["name"] + " how many do you take [1,3]?"))
            if num in range(1, 4):
                break
            else:
                self.notify({"msg-type":"error","msg":"Choice must be integer between in [1,3]."})

        return num


class AI:
    """
    AI: this class defines the AI component. The _bags variable is
    shared amongst all instances of AI objects so when the AI is being
    'trained' it is being trained by two instances learning with the
    same set of inputs.
    """
    _bags = [[1,2,3] for i in range(100)]
    DEFAULT_BAGS = [[1,2,3] for i in range(100)]

    def __init__(self, num_sticks, naive=False):
        self._sticks_left = num_sticks
        if naive:
            self._bags = self.DEFAULT_BAGS
        self._bag_hold = [None for i in range(num_sticks)]

    def notify(self, sticks):
        self._sticks_left = sticks

    def choose(self):
        if self._sticks_left == 1:
            return 1
        else:
            index = self._sticks_left - 1
            upper = (len(self._bags[index])-1) if self._sticks_left > 3 else self._sticks_left - 1
            stick_index = random.randint(0, upper)
            choice = self._bags[index][stick_index]
            self._bag_hold[index] = (choice)
            return choice

    def won(self):
        #  this will go through each holding bag and if the value is
        #  not None it will add that value to the AI's indexed bag from
        #  which the random 'balls' are chosen from.
        for i in range(len(self._bag_hold)):
            if self._bag_hold[i] is not None:
                self._bags[i].append(self._bag_hold[i])

    def lost(self):
        #  if ALTERNATE_OP != 1 then we simply disregard the balls we've
        #  placed in _bag_hold, however if it ALTERNATE_OP == 1 we will go
        #  to each _bag_hold location and remove all except the last instance of
        #  that number from _bags[i]. Essentially if in alternate operation mode, we
        #  we remove all but [1, 2, 3] in the losing move's index location. The default
        #  is ALTERNATE_OP = 0 and in this case _bag_hold is emptied at each instantiation
        #  of the AI.
        if ALTERNATE_OP:
            for i in range(len(self._bag_hold)):
                if self._bag_hold[i] is not None:
                    self._bags[i] = [x for x in self._bags[i] if x != self._bag_hold[i]]
                    self._bags[i].append(self._bag_hold[i])


class HumanVAI(AbstractGoS):
    """
    HumanVAI: this class is derived from AbstractGoS and fills
    in the appropriate methods for a human vs ai game of sticks
    """
    def __init__(self, init_sticks, train_ai=False):
        AbstractGoS.__init__(self, init_sticks, p2_type=AbstractGoS.PTYPE_AI)
        if train_ai:
            print("Training AI with %d games please wait..." % (AI_TRAINING_LOOPS))
            game = AIvAI(init_sticks)
            for i in range(AI_TRAINING_LOOPS):
                game.game_loop(quiet=True)

        self._p1["name"] = "Player 1"
        self._p2["name"] = "AI 1"
        self._ai = AI(init_sticks, naive=not train_ai)

    def notify(self, what, who=None, quiet=False):

        if what["msg-type"] == "error":
            print (what["msg"])

        if what["msg-type"] == "winner":
            if what["who"] == self._p2:
                self._ai.won()
            else:
                self._ai.lost()
            print (what["who"]["name"] + " has won!\n")

    def inform_of_sticks(self, num_sticks, who=None, quiet=False):
        if who == self._p2:
            self._ai.notify(num_sticks)
        print ("There are %d sticks on the table." % (num_sticks))

    def get_player_choice(self, player):
        num = 0
        if player == self._p2:
            num = self._ai.choose()
            print (player["name"] + " took %d sticks." % (num))
        else:
            while 1:
                num = int(input(player["name"] + " how many do you take [1,3]?"))
                if num in range(1, 4):
                    break
                else:
                    self.notify({"msg-type":"error","msg":"Choice must be integer between in [1,3]."}, player)

        return num


class AIvAI(AbstractGoS):
    """
    AIvAI: this class is derived from AbstractGoS and fills
    in the appropriate methods for a ai vs ai game of sticks
    """
    def __init__(self, init_sticks):
        AbstractGoS.__init__(self,init_sticks,p1_type=AbstractGoS.PTYPE_AI,p2_type=AbstractGoS.PTYPE_AI)
        self._p1["name"] = "AI 1"
        self._p2["name"] = "AI 2"
        self._ai1 = AI(init_sticks)
        self._ai2 = AI(init_sticks)
        self._qmode = False
    def notify(self, what, who=None, quiet=False):
        self._qmode = quiet
        if what["msg-type"] == "error":
            print (what["msg"]) if not quiet else None

        if what["msg-type"] == "winner":
            if what["who"] == self._p2:
                self._ai2.won()
                self._ai1.lost()
            else:
                self._ai1.won()
                self._ai2.lost()
            print (what["who"]["name"] + " has won!\n") if not quiet else None

    def inform_of_sticks(self, num_sticks, who=None, quiet=False):
        self._qmode = quiet
        print ("There are %d sticks on the table." % (num_sticks)) if not quiet else None
        if who == self._p2:
            self._ai2.notify(num_sticks)
        else:
            self._ai1.notify(num_sticks)

    def get_player_choice(self, player):
        num = 0
        if player == self._p2:
            num = self._ai2.choose()
            print (player["name"] + " took %d sticks." % (num)) if not self._qmode else None
        else:
            num = self._ai1.choose()
            print (player["name"] + " took %d sticks." % (num)) if not self._qmode else None
        return num


def get_game_mode(num):
    return{
            1: (HumanVHuman, None),
            2: (HumanVAI, False),
            3: (HumanVAI, True)
            }[num]
