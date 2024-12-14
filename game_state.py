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
