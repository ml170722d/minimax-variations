import math
import random
import enum

from agents import Agent
from states import GameState


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
        node = Node(state, Node.Type.MAX, '')
        alg = Minimax()

        score, node = alg.minimax(node, max_levels)
        return node.get_direction()


class MinimaxABAgent(StudentAgent):

    def get_next_action(self, state, max_levels):
        pass


class ExpectAgent(StudentAgent):

    def get_next_action(self, state, max_levels):
        pass


class MaxNAgent(StudentAgent):

    def get_next_action(self, state, max_levels):
        pass


class Node:
    class Type(enum.Enum):
        MAX = 'max'
        MIN = 'min'

    def __init__(self, state: GameState, node_type: Type, direction: str):
        self.type = node_type
        self.state = state
        self.dir = direction
        pass

    def successors(self, agent_id: int):
        actions = self.state.get_legal_actions(agent_id)
        states_list = [self.state.apply_action(agent_id, act) for act in actions]

        _type = Node.Type.MAX if self.type != Node.Type.MAX else Node.Type.MIN
        successors = [Node(states_list[i], _type, actions[i])
                      for i in range(len(states_list))]

        return successors

    def get_state(self) -> GameState:
        return self.state

    def get_type(self) -> Type:
        return self.type

    def get_direction(self) -> str:
        return self.dir

    def is_terminal(self, agent_id: int) -> bool:
        actions = self.state.get_legal_actions(agent_id)

        if len(actions) == 0:
            return True
        return False


class Minimax:
    #           |   id  |   role
    # ---------------------------
    # STUDENT   |   0   |   MAX
    # PROFESSOR |   1   |   MIN

    def eval(self, node: Node) -> int:
        student = len(node.state.get_legal_actions(0))
        professor = len(node.state.get_legal_actions(1))
        r = 0

        # if node.get_type() == Node.Type.MAX:
        #     r = (professor - student) * 10
        # else:
        #     r = (student - professor) * 10
        r = (student - professor) * 10

        # print_map(node.get_state())
        # print(node.get_type(), r)
        return r


    def is_terminal(self, node: Node, agent_id: int) -> bool:
        return node.is_terminal(agent_id)

    def minimax(self, node: Node, depth: int) -> (int, Node):
        # print_map(node.get_state())
        # print('type:', 'MAX' if node.get_type() != Node.Type.MAX else 'MIN', f'on depth {depth}')

        if self.is_terminal(node, 0 if node.get_type() == Node.Type.MAX else 1) or depth == 0:
            return self.eval(node), node

        if node.get_type() == Node.Type.MAX:
            # MAX
            score = -math.inf
            n = None
            for s in node.successors(0):
                tmp, n_tmp = self.minimax(s, depth - 1)
                # score = max(score, tmp)
                if score < tmp:
                    score = tmp
                    n = s

            return score, n
        else:
            # MIN
            score = math.inf
            n = None
            for s in node.successors(1):
                tmp, n_tmp = self.minimax(s, depth - 1)
                # score = min(score, tmp)
                if score > tmp:
                    score = tmp
                    n = s

            return score, n


def print_map(state: GameState):
    print('---------------')
    for row in state.char_map:
        print(row)
    print('---------------')
    pass
