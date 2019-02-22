
from solver import *
import Queue

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState.state == self.victoryCondition:
            return True

        self.visited[self.currentState] = True

        movables = self.gm.getMovables()
        current_state = self.currentState

        if movables:
            for movable in movables:
                self.gm.makeMove(movable)
                next_state = GameState(self.gm.getGameState(), current_state.depth + 1, movable)

                #self.visited[next_state] = False
                # if current_state.parent is not None and next_state.state == current_state.parent.state:
                #     #if making this move would result in the parent state
                #     self.gm.reverseMove(movable)
                #     continue
                # if next_state in self.visited:
                #     continue
                next_state.parent = current_state
                current_state.children.append(next_state)
                self.gm.reverseMove(movable)

            while current_state.nextChildToVisit < len(current_state.children):
                next_state = current_state.children[current_state.nextChildToVisit]
                if next_state not in self.visited:
                    current_state.nextChildToVisit += 1
                    self.visited[next_state] = True
                    self.gm.makeMove(next_state.requiredMovable)
                    self.currentState = next_state
                    break
                else:
                    current_state.nextChildToVisit += 1

        else:
            return False



class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        states = Queue()
        if self.currentState.state == self.victoryCondition:
            return True

        self.visited[self.currentState] = True

        movables = self.gm.getMovables()
        current_state = self.currentState

        if movables:
            for movable in movables:
                self.gm.makeMove(movable)
                next_state = GameState(self.gm.getGameState(), current_state.depth + 1, movable)
                next_state.parent = current_state
                current_state.children.append(next_state)
                states.put(next_state)
                self.gm.reverseMove()

            while states:
                

        else:
            return False
