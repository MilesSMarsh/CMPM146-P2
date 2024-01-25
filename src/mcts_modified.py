from mcts_node import MCTSNode
from p2_t3 import Board
from random import choice
from math import sqrt, log

num_nodes = 500
explore_faction = 2.

def traverse_nodes(node: MCTSNode, board: Board, state, bot_identity: int):
    """ Traverses the tree until the end criterion are met.
    e.g. find the best expandable node (node with untried action) if it exist,
    or else a terminal node

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 1 or 2

    Returns:
        node: A node from which the next stage of the search can proceed.
        state: The state associated with that node

    """
    # base case for recursion
    if board.is_ended(state):
        return node, state
    
    # Doesn't have child nodes but has untried actions (Leaf Node)
    if not node.child_nodes:
        if node.visits == 0:
            return node, state
        else:
            return expand_leaf(node, board, state)
            
    # recursion
    else:
        # find the best child node compared to the current node using the ucb function
        best_node = node
        highest_winrate = 0

        identity = (board.current_player(state) == bot_identity)
        
        for child in node.child_nodes.values():
            child_ucb = ucb(child, identity)
            if child_ucb >= highest_winrate:
                highest_winrate = child_ucb
                best_node = child

        # if best_node == node:
        #     return node, state
        
        # recursion using the predicted board of the child value
        new_state = board.next_state(state, best_node.parent_action)
        return traverse_nodes(best_node, board, new_state, identity)
       





def expand_leaf(node: MCTSNode, board: Board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node (if it is non-terminal).

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:
        node: The added child node
        state: The state associated with that node

    """
    for action in node.untried_actions:
        new_state = board.next_state(state, action)
        action_list = board.legal_actions(new_state)
        new_node = MCTSNode(node, action, action_list)
        node.child_nodes[action] = new_node
    return new_node, new_state




def rollout(board: Board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.
    
    Returns:
        state: The terminal game state

    """
    current_state = state
    while (not board.is_ended(current_state)):
        action_to_use = None
        
        for action in board.legal_actions(current_state):
            if action[2] == 1 and action[3] == 1:
                action_to_use = action

        if not action_to_use:
            action_to_use = choice(board.legal_actions(current_state))
        current_state = board.next_state(current_state, action_to_use)
    return current_state




def backpropagate(node: MCTSNode|None, won: bool):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """

    node.visits += 1
    if (won):
        node.wins += 1
    
    if (node.parent_action == None):
        return
    backpropagate(node.parent, won)




def ucb(node: MCTSNode, is_opponent: bool):
    """ Calcualtes the UCB value for the given node from the perspective of the bot

    Args:
        node:   A node.
        is_opponent: A boolean indicating whether or not the last action was performed by the MCTS bot
    Returns:
        The value of the UCB function for the given node
    """
    if node.visits == 0:
        return float('inf')

    # figure out whos turn it is
    if is_opponent:
        return 1 - (node.wins / node.visits) + explore_faction * sqrt(log(node.parent.visits)/ node.visits)
    else:
        return (node.wins / node.visits) + explore_faction * sqrt(log(node.parent.visits)/ node.visits)





def get_best_action(root_node: MCTSNode):
    """ Selects the best action from the root node in the MCTS tree

    Args:
        root_node:   The root node
    Returns:
        action: The best action from the root node
    
    """
    best_child = None
    highest_winrate = 0
    for child in root_node.child_nodes.values():
        child_winrate = (child.wins/child.visits)
        if child_winrate >= highest_winrate:
            highest_winrate = child_winrate
            best_child = child
    return best_child




def is_win(board: Board, state, identity_of_bot: int):
    # checks if state is a win state for identity_of_bot
    outcome = board.points_values(state)
    assert outcome is not None, "is_win was called on a non-terminal state"
    return outcome[identity_of_bot] == 1




def think(board: Board, current_state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        current_state:  The current state of the game.

    Returns:    The action to be taken from the current state

    """
    bot_identity = board.current_player(current_state) # 1 or 2
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(current_state))

    for _ in range(num_nodes):
        state = current_state
        node = root_node

        # Monte Carlo Tree Search 
        # selection and expansion
        node, state = traverse_nodes(node, board, state, bot_identity)

        # simulation
        possible_end_state = rollout(board, state)
        result = is_win(board, possible_end_state, bot_identity)

        # backpropagation
        backpropagate(node, result)
    
    
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    best_action = get_best_action(root_node).parent_action
    
    print(f"Action chosen: {best_action}")
    return best_action
