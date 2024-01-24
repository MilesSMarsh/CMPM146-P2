
from mcts_node import MCTSNode
from p2_t3 import Board
from random import choice
from math import sqrt, log

num_nodes = 100
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
    if(len(node.child_nodes) == 0):
        #print(len(node.child_nodes))
        return node, state
    # recursion
    else:

        # figure out whos turn it is
        if board.current_player(state) == bot_identity:
            identity = 0
        else:
            identity = 1

        # find the best child node using the ucb function
        # print("when does this happen?")
        best_node = get_best_action(node)

        # recursion using the predicted board of the child value
        state = board.next_state(state, best_node.parent_action)
        return traverse_nodes(best_node, board, state, bot_identity)
        #return the better of the parent or child nodes based on ucb winrate?




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
    # print("Child Node Added")
    action = choice(node.untried_actions)
    new_state = board.next_state(state, action)
    action_list = board.legal_actions(new_state)
    new_node = MCTSNode(node, action, action_list)
    node.child_nodes[action] = new_node
    node.untried_actions.remove(action)
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
        action = choice(board.legal_actions(current_state))
        current_state = board.next_state(current_state, action)
    return current_state




def backpropagate(node: MCTSNode|None, won: bool):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    current_node = node
    if current_node.parent == None:
        current_node.visits += 1
        
    while current_node.parent != None:
        current_node.visits += 1
        if won:
            current_node.wins += 1
        current_node = current_node.parent




def ucb(node: MCTSNode): #is_opponent: bool
    """ Calcualtes the UCB value for the given node from the perspective of the bot

    Args:
        node:   A node.
        is_opponent: A boolean indicating whether or not the last action was performed by the MCTS bot
    Returns:
        The value of the UCB function for the given node
    """
    # print(node.parent.visits)
    if node.parent.visits != 0:
        value = (node.wins / node.visits) + explore_faction * sqrt(log(node.parent.visits)/ node.visits)
        return value
    else:
        return 0




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
        if ucb(child) >= highest_winrate:
            highest_winrate = ucb(child)
            best_child = child
    #print("UCB OF GET BEST ACTION: ", ucb(best_child))
    return best_child
    #returns possible Nonetype




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
        # print("iterate")
        state = current_state
        node = root_node

        # Do MCTS - This is all you!
        # ...
        # selection
        node, state = traverse_nodes(node, board, state, bot_identity)
        # expansion
        if node.untried_actions:
            # print("has untried action")
            node, state = expand_leaf(node, board, state)
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
