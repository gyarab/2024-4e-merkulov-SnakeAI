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
