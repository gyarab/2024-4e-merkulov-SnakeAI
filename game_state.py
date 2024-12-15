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

    def neighbors(self, width_x: int, height_y: int):
        x, y = self.head_position
        neck_x, neck_y = self.snake_positions[0]

        for direction_x, direction_y in next_moves:
            next_x, next_y = x + direction_x, y + direction_y

            invalid = False
            for neck_x, neck_y in self.snake_positions:
                if next_x == neck_x and next_y == neck_y:
                    invalid = True
                    break

            if invalid:
                continue

            if next_x < 0 or next_x >= width_x:
                continue

            if next_y < 0 or next_y >= height_y:
                continue

            new_snake_positions = [self.head_position] + self.snake_positions
            new_snake_positions.pop()
            yield GameState((next_x, next_y), new_snake_positions)

    def get_all_head_positions(self):
        positions = []
        current = self
        while current is not None:
            positions.append(current.head_position)
            current = current.predecessor
        return positions
