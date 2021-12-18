import math
from states import GameState


class Node:
    def __init__(self, state: GameState, direction: str = ''):
        self.state = state
        self.dir = direction
        pass

    def successors(self, agent_id: int) -> list:
        pass

    def get_state(self) -> GameState:
        return self.state

    # def get_type(self) -> Type:
    #     return self.type

    def get_direction(self) -> str:
        return self.dir

    def is_terminal(self, agent_id: int) -> bool:
        return True if len(self.state.get_legal_actions(agent_id)) == 0 else False

    def get_rival_ids(self, agent_id: int) -> list[int]:
        # all_agents = [agent.id for agent in self.state.agents]
        # all_agents.remove(agent_id)
        # return all_agents
        return [agent.id for agent in self.state.agents if agent_id != agent.get_id()]


class Minimax:
    class MaxNode(Node):
        def successors(self, agent_id: int):
            actions = self.state.get_legal_actions(agent_id)
            states_list = [self.state.apply_action(agent_id, act) for act in actions]
            successors = [Minimax.MinNode(states_list[i], actions[i]) for i in range(len(states_list))]
            return successors

    class MinNode(Node):
        def successors(self, agent_id: int):
            actions = self.state.get_legal_actions(agent_id)
            states_list = [self.state.apply_action(agent_id, act) for act in actions]
            successors = [Minimax.MaxNode(states_list[i], actions[i]) for i in range(len(states_list))]
            return successors

    @staticmethod
    def eval(node: Node, agent_id: int) -> float:
        curr_agent_eval = len(node.get_state().get_legal_actions(agent_id))
        rival_ids = node.get_rival_ids(agent_id)
        rival_agent_eval = sum(len(node.get_state().get_legal_actions(rival_id)) for rival_id in rival_ids)
        rival_agent_eval = rival_agent_eval / len(rival_ids)
        return 10 * (curr_agent_eval - rival_agent_eval)

    @staticmethod
    def is_terminal(node: Node, curr_agent_id: int) -> bool:
        return node.is_terminal(curr_agent_id)

    def run(self, node: Node, depth: int, curr_agent_id: int) -> (float, Node):
        if self.is_terminal(node, curr_agent_id) or depth == 0:
            return self.eval(node, curr_agent_id), node

        if isinstance(node, Minimax.MaxNode):
            # MAX
            score = -math.inf
            n = None
            for s in node.successors(curr_agent_id):
                tmp, n_tmp = self.run(s, depth - 1, curr_agent_id)
                if score < tmp:
                    score = tmp
                    n = s

            return score, n
        else:
            # MIN
            score = math.inf
            n = None
            rival_id = node.get_rival_ids(curr_agent_id)
            for s in node.successors(rival_id[0]):
                tmp, n_tmp = self.run(s, depth - 1, curr_agent_id)
                if score > tmp:
                    score = tmp
                    n = s

            return score, n


class MinimaxAB(Minimax):

    def run(self, node: Node, depth: int, curr_agent_id: int, alpha: float, beta: float) -> (float, Node):
        if self.is_terminal(node, curr_agent_id) or depth == 0:
            return self.eval(node, curr_agent_id), node

        if isinstance(node, Minimax.MaxNode):
            # MAX
            score = -math.inf
            n = None
            for s in node.successors(curr_agent_id):
                tmp, n_tmp = self.run(s, depth - 1, curr_agent_id, alpha, beta)
                if score < tmp:
                    score = tmp
                    n = s
                alpha = max(alpha, score)
                if alpha >= beta:
                    print('ab cut')
                    break

            return score, n
        else:
            # MIN
            score = math.inf
            n = None
            rival_id = node.get_rival_ids(curr_agent_id)
            for s in node.successors(rival_id[0]):
                tmp, n_tmp = self.run(s, depth - 1, curr_agent_id, alpha, beta)
                if score > tmp:
                    score = tmp
                    n = s
                alpha = max(alpha, score)
                if alpha >= beta:
                    print('ab cut')
                    break

            return score, n


class Expectimax(Minimax):
    class MaxNode(Node):
        def successors(self, agent_id: int) -> list:
            actions = self.state.get_legal_actions(agent_id)
            states_list = [self.state.apply_action(agent_id, act) for act in actions]
            successors = [Expectimax.ChanceNode(states_list[i], actions[i]) for i in range(len(states_list))]
            return successors

    class ChanceNode(Node):
        def successors(self, agent_id: int) -> list:
            actions = self.state.get_legal_actions(agent_id)
            states_list = [self.state.apply_action(agent_id, act) for act in actions]
            successors = [Expectimax.MaxNode(states_list[i], actions[i]) for i in range(len(states_list))]
            return successors

    def run(self, node: Node, depth: int, curr_agent_id: int) -> (float, Node):
        if self.is_terminal(node, curr_agent_id) or depth == 0:
            return self.eval(node, curr_agent_id), node

        if isinstance(node, Expectimax.MaxNode):
            # MAX
            score = -math.inf
            n = None
            for s in node.successors(curr_agent_id):
                tmp, n_tmp = self.run(s, depth - 1, curr_agent_id)
                if score < tmp:
                    score = tmp
                    n = s

            return score, n
        else:
            # CHANCE
            score = 0
            n = None
            rival_id = node.get_rival_ids(curr_agent_id)
            successors = node.successors(rival_id[0])
            for s in successors:
                prob = 1 / len(successors)
                tmp, n_tpm = self.run(s, depth - 1, curr_agent_id)
                score += prob * tmp
                n = node

            return score, n


class MinimaxN(Minimax):
    class MaxNode(Node):
        def successors(self, agent_id: int) -> list:
            actions = self.state.get_legal_actions(agent_id)
            states_list = [self.state.apply_action(agent_id, act) for act in actions]
            successors = [MinimaxN.MinNode(states_list[i], actions[i]) for i in range(len(states_list))]
            return successors

    class MinNode(Node):
        def successors(self, agent_id: int) -> list:
            actions = self.state.get_legal_actions(agent_id)
            states_list = [self.state.apply_action(agent_id, act) for act in actions]
            successors = None
            if self.is_last_player(agent_id):
                successors = [MinimaxN.MaxNode(states_list[i], actions[i]) for i in range(len(states_list))]
            else:
                successors = [MinimaxN.MinNode(states_list[i], actions[i]) for i in range(len(states_list))]
            return successors

        def is_last_player(self, agent_id: int) -> bool:
            return True if agent_id == len(self.state.agents) - 1 else False

    def run(self, node: Node, depth: int, curr_agent_id: int, next_agent_id: int) -> (float, Node):
        if self.is_terminal(node, curr_agent_id) or depth == 0:
            return self.eval(node, curr_agent_id), node

        if isinstance(node, MinimaxN.MaxNode):
            # MAX
            score = -math.inf
            n = None
            for s in node.successors(curr_agent_id):
                tmp, n_tmp = self.run(s, depth - 1, curr_agent_id, (curr_agent_id + 1) % len(node.get_state().agents))
                if score < tmp:
                    score = tmp
                    n = s

            return score, n
        else:
            # MIN
            score = math.inf
            n = None
            for s in node.successors(next_agent_id):
                tmp, n_tmp = self.run(s, depth - 1, curr_agent_id, (next_agent_id + 1) % len(node.get_state().agents))
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
