from dataclasses import dataclass, field

next_moves = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0)
]


@dataclass
class GameState:
    head_position: tuple[int, int]
    snake_positions: list[tuple[int, int]] = field(default_factory=list)
    predecessor: "GameState | None" = None

    def neighbors(self, n_rows: int, n_cols: int):
        r, c = self.head_position
        neck_r, neck_c = self.snake_positions[0]

        for d_r, d_c in next_moves:
            next_r, next_c = r + d_r, c + d_c

            invalid = False
            for neck_r, neck_c in self.snake_positions:
                if next_r == neck_r and next_c == neck_c:
                    invalid = True
                    break

            if invalid:
                continue

            if next_r < 0 or next_r >= n_rows:
                continue

            if next_c < 0 or next_c >= n_cols:
                continue

            new_snake_positions = [self.head_position] + self.snake_positions
            new_snake_positions.pop()
            yield GameState((next_r, next_c), new_snake_positions)


def sort_snake_positions(game_state: GameState):
    current_head = game_state.head_position

    new_snake_positions: list[tuple[int, int]] = []
    while game_state.snake_positions:
        for i, position in enumerate(game_state.snake_positions):
            r, c = position
            if r == current_head[0] and abs(current_head[1] - c) == 1:
                new_snake_positions.append((r, c))
                break
            if c == current_head[1] and abs(current_head[0] - r) == 1:
                new_snake_positions.append((r, c))
                break
        else:
            raise ValueError(f"{game_state.snake_positions}, {current_head}")

        game_state.snake_positions.pop(i)
        current_head = (r, c)

    game_state.snake_positions = new_snake_positions


def load_unsorted_game_state(input_map: str):
    rows = input_map.strip().split("\n")
    n_rows = len(rows)
    n_cols = -1
    game_state = GameState(None)

    apple_r, apple_c = None, None

    for r, row in enumerate(rows):
        row = row.strip()
        if n_cols == -1:
            n_cols = len(row)

        for c, col in enumerate(row):
            if col == "0":
                game_state.head_position = (r, c)
            if col == "o":
                game_state.snake_positions.append((r, c))
            if col == "x":
                apple_r, apple_c = r, c

    return n_rows, n_cols, game_state, (apple_r, apple_c)


def load_logic(input_map: str):
    n_rows, n_cols, game_state, apple_position = load_unsorted_game_state(input_map)
    sort_snake_positions(game_state)

    return game_state, n_rows, n_cols, apple_position


def print_map(game_state: GameState, n_rows: int, n_cols: int, apple_position: tuple[int, int]):
    str_map = [["."] * n_cols for _ in range(n_rows)]

    r, c = game_state.head_position
    str_map[r][c] = "0"

    for r, c in game_state.snake_positions:
        str_map[r][c] = "o"

    r, c = apple_position
    str_map[r][c] = "x"

    for row in str_map:
        print("".join(row))


def print_path(game_state: GameState, apple_position: tuple[int, int], n_rows: int, n_cols: int):
    path = [game_state]

    while game_state.predecessor is not None:
        path = [game_state.predecessor] + path
        game_state = game_state.predecessor

    for game_state in path:
        print_map(game_state, n_rows, n_cols, apple_position)
        print()
        print("-" * 10)
        print()
