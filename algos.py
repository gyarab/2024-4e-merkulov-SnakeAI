import heapq
from dataclasses import dataclass, field

from game_state import GameState


def dfs(game_state: GameState, apple_position: tuple[int, int], n_rows: int, n_cols: int):
    if game_state.head_position == apple_position:
        return True, game_state

    for neighbor in game_state.neighbors(n_rows, n_cols):
        neighbor.predecessor = game_state
        is_found, new_game_state = dfs(neighbor, apple_position, n_rows, n_cols)
        if is_found:
            return True, new_game_state

    return False, None


def depth_limited_dfs(game_state: GameState, apple_position: tuple[int, int], n_rows: int, n_cols: int,
                      depth_limit: int, current_depth: int = 0):
    if game_state.head_position == apple_position:
        return True, game_state

    if current_depth == depth_limit:
        return False, None

    for neighbor in game_state.neighbors(n_rows, n_cols):
        neighbor.predecessor = game_state
        is_found, new_game_state = depth_limited_dfs(neighbor, apple_position, n_rows, n_cols,
                                                     current_depth=current_depth + 1, depth_limit=depth_limit)
        if is_found:
            return True, new_game_state

    return False, None


def iterative_deepening_dfs(game_state: GameState, apple_position: tuple[int, int], n_rows: int, n_cols: int):
    for depth_limit in range(1, 100):
        is_found, final_game_state = depth_limited_dfs(game_state, apple_position, n_rows, n_cols,
                                                       depth_limit=depth_limit)

        if is_found:
            assert final_game_state is not None
            return is_found, final_game_state

    return False, None


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    state: GameState = field(compare=False)


def heuristic(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Calculate the Manhattan distance heuristic."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(game_state: GameState, apple_position: tuple[int, int], n_rows: int, n_cols: int):
    open_set = []
    heapq.heappush(open_set, PrioritizedItem(0, game_state))
    came_from = {}

    # Use a tuple representation for g_score and f_score
    g_score = {(game_state.head_position, tuple(game_state.snake_positions)): 0}
    f_score = {(game_state.head_position, tuple(game_state.snake_positions)): heuristic(game_state.head_position,
                                                                                        apple_position)}

    while open_set:
        current = heapq.heappop(open_set).state

        if current.head_position == apple_position:
            return True, current  # Path found

        for neighbor in current.neighbors(n_cols, n_rows):
            tentative_g_score = g_score[(
            current.head_position, tuple(current.snake_positions))] + 1  # Assuming each move has a cost of 1

            neighbor_key = (neighbor.head_position, tuple(neighbor.snake_positions))

            if neighbor_key not in g_score or tentative_g_score < g_score[neighbor_key]:
                came_from[neighbor_key] = (current.head_position, tuple(current.snake_positions))
                g_score[neighbor_key] = tentative_g_score
                f_score[neighbor_key] = tentative_g_score + heuristic(neighbor.head_position, apple_position)

                if neighbor_key not in [(item.state.head_position, tuple(item.state.snake_positions)) for item in
                                        open_set]:
                    heapq.heappush(open_set, PrioritizedItem(f_score[neighbor_key], neighbor))

    return False, None  # No path found
