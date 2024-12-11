import pygame, sys, time, random
from graph import Graph

# Difficulty settings
difficulty = 5

# Game grid size
number_of_nodes = 16
number_of_nodes_on_side = 4

# Window size
frame_size_x = 500
frame_size_y = 500

# Cell size (larger than before)
cell_size = frame_size_x // number_of_nodes_on_side

# Checks for errors encountered
check_errors = pygame.init()
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# Initialise game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y + 50))  # Extra 50 px for UI space above

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
gray = pygame.Color(25, 25, 25)

# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

# Game variables
snake_pos = [(cell_size * 3), cell_size]
snake_body = [[(cell_size * 3), cell_size], [(cell_size * 3) - cell_size, cell_size],
              [(cell_size * 3) - (2 * cell_size), cell_size]]


def free_for_food():
    available_food_spawn_places = []
    for x in range(number_of_nodes_on_side):
        for y in range(number_of_nodes_on_side):
            position = [x * cell_size, y * cell_size]
            if position not in snake_body:
                available_food_spawn_places.append(position)
    return available_food_spawn_places


food_spawn_places = free_for_food()
food_pos = random.choice(food_spawn_places)
food_spawn = True

# Graph initialization
graph = Graph(number_of_nodes, cell_size, number_of_nodes_on_side)
number_of_snake_body_nodes = graph.game_to_graph(snake_body)
graph.initialize_graph(number_of_snake_body_nodes)
#graph.display_matrix()

# Hamiltonian cycle path (example for a 10x10 grid)
hamiltonian_cycle = graph.find_hamiltonian_cycle()
''''''
# Initialize direction index for Hamiltonian cycle
direction_index = graph.game_to_graph(snake_body)[0]

score = 0

show_grid = True  # Flag to toggle grid

# Button to toggle grid visibility (now in top-right corner)
button_rect = pygame.Rect(frame_size_x - 90, 10, 80, 30)  # Button moved to top-right corner


# Game Over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 30)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x / 2, frame_size_y / 4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (50, 10)  # Score moved to top-left corner
    game_window.blit(score_surface, score_rect)

def winning():
    font = pygame.font.SysFont('comicsans', 60, True)
    winning_surface = font.render('YOU WON', True, black)
    winning_rect = winning_surface.get_rect()
    winning_rect.midtop = (frame_size_x / 2, frame_size_y / 4)
    game_window.blit(winning_surface, winning_rect)  # Adjust position as needed
    pygame.display.update()  # Update the display to show the message

    # Keep the window open until the player closes it
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.delay(100)

# Main logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Mouse button click to toggle grid visibility
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                show_grid = not show_grid

    # Check if the snake has reached the winning length
    if len(snake_body) >= number_of_nodes - 1:
        print("Congratulations! You've completed the game!")
        running = False
        winning()  # End the game loop

    # Move the snake along the Hamiltonian cycle
    if direction_index < len(hamiltonian_cycle):
        snake_pos = list(hamiltonian_cycle[direction_index])
        direction_index += 1
    else:
        # If the snake has completed the cycle, reset to the beginning
        direction_index = 0
        snake_pos = list(hamiltonian_cycle[direction_index])
        direction_index += 1

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
        food_spawn_places = free_for_food()
    else:
        snake_body.pop()

    # Spawning food on the screen

    # Update the food spawning logic
    if not food_spawn:
        if food_spawn_places:
            food_pos = random.choice(food_spawn_places)
            food_spawn = True
        else:
            print("No valid food spawn places available.")

    # Fill the game window
    game_window.fill(black)

    # Draw grid if show_grid is True
    if show_grid:
        for x in range(0, frame_size_x, cell_size):
            pygame.draw.line(game_window, gray, (x, 50), (x, frame_size_y + 50))  # Grid starts below the UI
        for y in range(50, frame_size_y + 50, cell_size):
            pygame.draw.line(game_window, gray, (0, y), (frame_size_x, y))

    # Draw the snake body with black border
    for pos in snake_body:
        # Draw the black border (slightly larger rectangle)
        pygame.draw.rect(game_window, black, pygame.Rect(pos[0], pos[1] + 50, cell_size, cell_size))
        # Draw the green snake body inside the black border
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0] + 2, pos[1] + 52, cell_size - 4, cell_size - 4))

    # Draw the food
    pygame.draw.circle(game_window, red, (food_pos[0] + cell_size // 2, food_pos[1] + 50 + cell_size // 2),
                       cell_size // 2)

    # Draw the button to toggle grid
    pygame.draw.rect(game_window, blue, button_rect)
    button_font = pygame.font.SysFont('consolas', 20)
    button_text = button_font.render('Grid', True, white)
    game_window.blit(button_text, (button_rect.x + 10, button_rect.y + 5))

    # Game Over conditions
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - cell_size:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y - cell_size:
        game_over()
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    # Draw a line to separate UI from the grid
    pygame.draw.line(game_window, white, (0, 50), (frame_size_x, 50), 2)  # Separation line

    # Show score
    show_score(1, white, 'consolas', 15)

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second / Refresh Rate
    fps_controller.tick(difficulty)
    ''''''
