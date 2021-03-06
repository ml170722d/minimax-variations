import math
import random

from agents import Agent
from minimax import Minimax, MinimaxAB, Expectimax, MinimaxN


# Example agent, behaves randomly.
# ONLY StudentAgent and his descendants have a 0 id. ONLY one agent of this type must be present in a game.
# Agents from bots.py have successive ids in a range from 1 to number_of_bots.
class StudentAgent(Agent):
    def __init__(self, position, file_name):
        super().__init__(position, file_name)
        self.id = 0

    @staticmethod
    def kind():
        return '0'

    # Student shall override this method in derived classes.
    # This method should return one of the legal actions (from the Actions class) for the current state.
    # state - represents a state object.
    # max_levels - maximum depth in a tree search. If max_levels eq -1 than the tree search depth is unlimited.
    def get_next_action(self, state, max_levels):
        actions = self.get_legal_actions(state)  # equivalent of state.get_legal_actions(self.id)
        chosen_action = actions[random.randint(0, len(actions) - 1)]
        # Example of a new_state creation (for a chosen_action of a self.id agent):
        # new_state = state.apply_action(self.id, chosen_action)
        return chosen_action


class MinimaxAgent(StudentAgent):

    def get_next_action(self, state, max_levels):
        node = Minimax.MaxNode(state)
        alg = Minimax()

        score, node = alg.run(node, max_levels, self.get_id())
        return node.get_direction()


class MinimaxABAgent(StudentAgent):

    def get_next_action(self, state, max_levels):
        node = MinimaxAB.MaxNode(state)
        alg = MinimaxAB()

        score, node = alg.run(node, max_levels, self.get_id(), -math.inf, math.inf)
        return node.get_direction()


class ExpectAgent(StudentAgent):

    def get_next_action(self, state, max_levels):
        node = Expectimax.MaxNode(state)
        alg = Expectimax()

        score, node = alg.run(node, max_levels, self.get_id())
        return node.get_direction()


class MaxNAgent(StudentAgent):

    def get_next_action(self, state, max_levels):
        node = MinimaxN.MaxNode(state)
        alg = MinimaxN()

        score, node = alg.run(node, max_levels, self.get_id(), self.get_id())
        return node.get_direction()
