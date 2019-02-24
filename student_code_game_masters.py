from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here

        if self.kb.kb_ask(parse_input("fact: (on disk4 ?X")) is False:
            disks = ["disk1", "disk2", "disk3"]
        else:
            disks = ["disk1", "disk2", "disk3", "disk4", "disk5"]
        peg1 = []
        peg2 = []
        peg3 = []
        for disk in disks:
            ask = parse_input("fact: (on " + disk + " ?X)")
            answer = self.kb.kb_ask(ask)
            if str(answer[0]) == "?X : peg1":
                print(disk)
                peg1.append(int(disk[-1]))
            elif str(answer[0]) == "?X : peg2":
                peg2.append(int(disk[-1]))
            elif str(answer[0]) == "?X : peg3":
                peg3.append(int(disk[-1]))

        return (tuple(peg1), tuple(peg2), tuple(peg3))
        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        game_state = self.getGameState()
        disk = str(movable_statement.terms[0])
        initial = str(movable_statement.terms[1])
        initial_num = int(initial[-1])
        target = str(movable_statement.terms[2])
        target_num = int(target[-1])

        self.kb.kb_retract(parse_input("fact: (on " + disk + " " + initial + ")"))
        self.kb.kb_add(parse_input("fact: (on " + disk + " " + target + ")"))

        #updates facts regarding state of target peg
        if not game_state[target_num-1]:
            self.kb.kb_retract(parse_input("fact: (empty " +target+ ")"))
        else:
            self.kb.kb_retract(
                parse_input("fact: (onTop disk" + str(game_state[target_num - 1][0]) + " " + target + ")"))

        self.kb.kb_add(parse_input("fact: (onTop " + disk + " " + target + ")"))
        self.kb.kb_retract(parse_input("fact: (onTop " + disk + " " + initial + ")"))

        #updates facts regarding state of initial peg
        game_state = self.getGameState()
        if not game_state[initial_num-1]:
            self.kb.kb_add(parse_input("fact: (empty " + initial + ")"))
        else:
            self.kb.kb_add(parse_input("fact: (onTop disk" + str(game_state[initial_num-1][0])+ " " +initial+ ")"))

        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here

        row1 = []
        row2 = []
        row3 = []
        for x in range(3):
            for y in range(3):
                ask = parse_input("fact: (pos ?X pos" + str(x+1) + " pos" + str(y+1) + ")")
                tile = str(self.kb.kb_ask(ask)[0])[-1]
                if tile == "y":
                    tile = -1
                print(tile)
                if y == 0:
                    row1.append(int(tile))
                elif y == 1:
                    row2.append(int(tile))
                elif y == 2:
                    row3.append(int(tile))

        return (tuple(row1), tuple(row2), tuple(row3))


        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        game_state = self.getGameState()

        tile = str(movable_statement.terms[0])
        initial_x = str(movable_statement.terms[1])
        initial_y = str(movable_statement.terms[2])
        target_x = str(movable_statement.terms[3])
        target_y = str(movable_statement.terms[4])

        self.kb.kb_retract(parse_input("fact: (pos " + tile + " " + initial_x + " " + initial_y + ")"))
        self.kb.kb_retract(parse_input("fact: (pos empty " + target_x + " " + target_y + ")"))
        self.kb.kb_add(parse_input("fact: (pos " + tile + " " + target_x + " " + target_y + ")"))
        self.kb.kb_add(parse_input("fact: (pos empty " + initial_x + " " + initial_y + ")"))

        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
