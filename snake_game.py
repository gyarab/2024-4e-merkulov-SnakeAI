#!/usr/bin/env python3
import copy
import random
import sys
import time

import pygame

from algos import *
from game_state import GameState
from graph import Graph

# Text variables
font = 'comicsans'
stopwatch_text = 'Stopwatch'
# Difficulty settings
difficulty = 40
prev_path = 0
# Game grid size
number_of_nodes = 100
number_of_nodes_on_side = 10


# Window size
frame_size_x = 900
frame_size_y = 900

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
snake_head = (cell_size * 3, cell_size)
snake_body = [
    # snake_head,
    (cell_size * 3 - cell_size, cell_size),
    (cell_size * 3 - 2 * cell_size, cell_size)
]
start_time = time.time()

def free_for_food():
    available_food_spawn_places = []
    for i in range(number_of_nodes_on_side):
        for j in range(number_of_nodes_on_side):
            position = (i * cell_size, j * cell_size)
            if position not in snake_body and position != snake_head:
                available_food_spawn_places.append(position)
    return available_food_spawn_places


def game_to_neighbors(snake_game_body):
    snake_neighbors_body = []
    if isinstance(snake_game_body, list):
        snake_body_for_neighbors = [(x // cell_size, y // cell_size) for x, y in snake_game_body]
        for i, j in snake_body_for_neighbors:
            snake_neighbors_body.append((i, j))
        return snake_neighbors_body
    else:
        x, y = snake_game_body
        i = x // cell_size
        j = y // cell_size
        snake_neighbors_body = (i, j)
        return snake_neighbors_body


def neighbors_to_snake_body(snake_neighbors_body):
    snake_body_game = []
    if isinstance(snake_neighbors_body, list):
        snake_body_from_neighbors = [(x * cell_size, y * cell_size) for x, y in snake_neighbors_body]
        for i, j in snake_body_from_neighbors:
            snake_body_game.append((i, j))
        return snake_body_game
    else:
        x, y = snake_neighbors_body
        i = x * cell_size
        j = y * cell_size
        snake_body_game = (i, j)
        return snake_body_game


def game_to_graph(snake_game_body):
    snake_graph_body = []
    if isinstance(snake_game_body, list):
        for x, y in snake_game_body:
            snake_graph_body.append(y * number_of_nodes_on_side + x)
        return snake_graph_body
    else:
        x, y = snake_game_body
        snake_graph_body = (y * number_of_nodes_on_side + x)
        return snake_graph_body

def graph_to_game(telo):
    x = (telo % number_of_nodes_on_side) * cell_size
    y = (telo // number_of_nodes_on_side) * cell_size
    return (x, y)


# food_spawn_places = free_for_food()
# food_pos = random.choice(food_spawn_places)
food_pos = (cell_size * 4, cell_size * 4)
food_spawn = True

hamiltonian_cylcle_order = [0] * number_of_nodes
n_snake_head = game_to_neighbors(snake_head)
n_snake_body = game_to_neighbors(snake_body)
n_food_pos = game_to_neighbors(food_pos)

game_state = GameState(head_position=n_snake_head, snake_positions=n_snake_body, predecessor=None)
path = a_star(game_state, n_food_pos, number_of_nodes_on_side, number_of_nodes_on_side, hamiltonian_cylcle_order)
final_tail_position = path.snake_positions[-1] if path.snake_positions else None
path_for_following = path.get_all_head_positions()
path_for_following.pop()
final_head_position = path_for_following[0]
final_tail = game_to_graph(final_tail_position)
final_head = game_to_graph(final_head_position)
path_for_following.reverse()

path_for_following = neighbors_to_snake_body(path_for_following)
food_pos = neighbors_to_snake_body(n_food_pos)

follow_hamiltonian_cycle = True

''''''
# Graph initialization
smaller_graph = Graph(number_of_nodes // 4, cell_size, number_of_nodes_on_side // 2)
smaller_graph.initialize_smaller_graph()
small_adjacency_list = copy.deepcopy(smaller_graph.adjacency_list)
spanning_tree = smaller_graph.spanning_tree()
nodes_for_smaller_nodes = smaller_graph.neighbor_nodes()
graph = Graph(number_of_nodes, cell_size, number_of_nodes_on_side)
hamiltonian_cycle = graph.hamiltonian_cycle(spanning_tree, number_of_nodes // 4, number_of_nodes_on_side // 2,
                                            nodes_for_smaller_nodes, small_adjacency_list)
order = 0
size = len(hamiltonian_cycle)
hamiltonian_cylcle_order = [0] * size
for node in hamiltonian_cycle:
    hamiltonian_cylcle_order[node] = order
    order += 1

hamiltonian_cycle = graph.graph_to_game(hamiltonian_cycle)
''''''
'''
number_of_snake_body_nodes = graph.game_to_graph(snake_body)
graph.initialize_graph(number_of_snake_body_nodes)
'''
'''
# Hamiltonian cycle path (example for a 10x10 grid)
hamiltonian_cycle = [
    (0, 0), (0, cell_size), (0, cell_size * 2), (0, cell_size * 3),
    (cell_size, cell_size * 3), (cell_size * 2, cell_size * 3), (cell_size * 3, cell_size * 3),
    (cell_size * 3, cell_size * 2), (cell_size * 2, cell_size * 2), (cell_size, cell_size * 2),
    (cell_size, cell_size), (cell_size * 2, cell_size), (cell_size * 3, cell_size),
    (cell_size * 3, 0), (cell_size * 2, 0), (cell_size, 0)
]
'''
'''
hamiltonian_cycle = [
    (0, 0), (150, 0), (300, 0), (450, 0), (600, 0), (750, 0), (750, 150), (750, 300),
    (750, 450), (750, 600), (750, 750), (600, 750), (450, 750), (300, 750), (150, 750),
    (0, 750), (0, 600), (0, 450), (0, 300), (150, 300), (300, 300), (450, 300), (450, 450),
    (300, 450), (150, 450), (150, 600), (300, 600), (450, 600), (600, 600), (600, 450),
    (600, 300), (600, 150), (450, 150), (300, 150), (150, 150), (0, 150)
]
hamiltonian_cylcle_order = [0, 1, 2, 3, 4, 5, 35, 34, 33, 32, 31, 6, 18, 19, 20, 21, 30, 7, 17, 24, 23, 22, 29, 8, 16,
                            25, 26, 27, 28, 9, 15, 14, 13, 12, 11, 10]
'''
# Initialize direction index for Hamiltonian cycle
''''''
for i in range(len(hamiltonian_cycle)):
    if hamiltonian_cycle[i] == snake_head:
        direction_index = i
        break
''''''
#direction_index = 0
score = 0
moves = 0

show_grid = True  # Flag to toggle grid
pause_game = False
# Button to toggle grid visibility (now in top-right corner)
button_rect = pygame.Rect(frame_size_x - 90, 10, 80, 30)  # Button moved to top-right corner
button_pause = pygame.Rect(frame_size_x - (frame_size_x // 2), 10, 80, 30)


# Game Over
def game_over():
    font = pygame.font.SysFont('comicsans', 60, True)
    winning_surface = font.render('YOU DIED', True, white)
    winning_rect = winning_surface.get_rect()
    winning_rect.center = (frame_size_x / 2, frame_size_y / 4)
    game_window.blit(winning_surface, winning_rect)  # Adjust position as needed
    pygame.display.update()  # Update the display to show the message
    print(str(stopwatch_text))
    print(str(score))
    print(str(moves))
    pygame.quit()
    sys.exit()

    ''''''
    # Keep the window open until the player closes it
    waiting = True
    while waiting:
        for winning_event in pygame.event.get():
            if winning_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.delay(100)
    ''''''
    '''
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
    '''


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (50, 10)  # Score moved to top-left corner
    game_window.blit(score_surface, score_rect)


def show_moves(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Moves made : ' + str(moves), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (300, 10)  # Score moved to top-left corner
    game_window.blit(score_surface, score_rect)


def winning():
    font = pygame.font.SysFont('comicsans', 60, True)
    winning_surface = font.render('YOU WON', True, black)
    winning_rect = winning_surface.get_rect()
    winning_rect.midtop = (frame_size_x / 2, frame_size_y / 4)
    game_window.blit(winning_surface, winning_rect)  # Adjust position as needed
    pygame.display.update()  # Update the display to show the message
    print(str(stopwatch_text))
    print(str(score))
    print(str(moves))
    pygame.quit()
    sys.exit()

    # Keep the window open until the player closes it
    ''''''
    waiting = True
    while waiting:
        for winning_event in pygame.event.get():
            if winning_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.delay(100)
    ''''''


def no_path():
    font = pygame.font.SysFont('comicsans', 60, True)
    winning_surface = font.render('NO PATH POSSIBLE EXISTS', True, white)
    winning_rect = winning_surface.get_rect()
    winning_rect.midtop = (frame_size_x / 2, frame_size_y / 4)
    game_window.blit(winning_surface, winning_rect)  # Adjust position as needed
    pygame.display.update()  # Update the display to show the message

    # Keep the window open until the player closes it
    waiting = True
    while waiting:
        for winning_event in pygame.event.get():
            if winning_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.delay(100)


def pause():
    # Keep the window open until the player closes it
    waiting = True
    while waiting:
        for pausing_event in pygame.event.get():
            if pausing_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif pausing_event.type == pygame.MOUSEBUTTONDOWN:
                if button_pause.collidepoint(pausing_event.pos):
                    waiting = False


def show_stopwatch():
    global stopwatch_text
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    stopwatch_text = f'{minutes:02}:{seconds:02}'

    font = pygame.font.SysFont('comicsans', 30)
    stopwatch_surface = font.render('Time: ' + stopwatch_text, True, white)
    stopwatch_rect = stopwatch_surface.get_rect()
    stopwatch_rect.topright = (frame_size_x - 200, 10)  # Top-right corner
    game_window.blit(stopwatch_surface, stopwatch_rect)


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
            elif button_pause.collidepoint(event.pos):
                pause_game = not pause_game

    if pause_game:
        pause()
        pause_game = False
    # Check if the snake has reached the winning length
    if len(snake_body) >= number_of_nodes - 1:
        print("Congratulations! You've completed the game!")
        running = False
        winning()  # End the game loop
    ''''''
    if follow_hamiltonian_cycle:
        # Move the snake along the Hamiltonian cycle
        if direction_index < len(hamiltonian_cycle):
            snake_head = hamiltonian_cycle[direction_index]
            direction_index += 1
            moves += 1
        else:
            # If the snake has completed the cycle, reset to the beginning
            direction_index = 0
            snake_head = hamiltonian_cycle[direction_index]
            direction_index += 1
            moves += 1
    else:
        ''''''
        ''''''
        if direction_index < len(path_for_following):
            snake_head = path_for_following[direction_index]
            direction_index += 1
            moves += 1
        ''''''
    # Snake body growing mechanism
    snake_body.insert(0, snake_head)
    if snake_head == food_pos:
        score += 1
        food_spawn = False
        food_spawn_places = free_for_food()
    else:
        if len(snake_body) >= 3:
            snake_body.pop()

    # Update the food spawning logic
    if not food_spawn:
        if food_spawn_places:
            food_pos = random.choice(food_spawn_places)
            food_spawn = True
            follow_hamiltonian_cycle = True
            '''
            n_snake_head = game_to_neighbors(snake_head)
            n_snake_body = game_to_neighbors(snake_body)
            n_food_pos = game_to_neighbors(food_pos)
            game_state = GameState(head_position=n_snake_head, snake_positions=n_snake_body, predecessor=None)
            path = a_star(game_state, n_food_pos, number_of_nodes_on_side, number_of_nodes_on_side,
                          hamiltonian_cylcle_order)
            if path is None:
                follow_hamiltonian_cycle = True
                for i in range(len(hamiltonian_cycle)):
                    if hamiltonian_cycle[i] == snake_head:
                        direction_index = i + 1
                        break
            else:
                final_tail_position = path.snake_positions[-1] if path.snake_positions else None
                path_for_following = path.get_all_head_positions()
                path_for_following.pop()
                final_head_position = path_for_following[0]
                final_tail = game_to_graph(final_tail_position)
                final_head = game_to_graph(final_head_position)
                path_for_following.reverse()
                tail = hamiltonian_cylcle_order[final_tail]
                head = hamiltonian_cylcle_order[final_head]
                
                path_for_following = neighbors_to_snake_body(path_for_following)
                food_pos = neighbors_to_snake_body(n_food_pos)
                snake_body = neighbors_to_snake_body(n_snake_body)
                snake_head = neighbors_to_snake_body(n_snake_head)
                direction_index = 0
                
                if tail > head:
                    if tail - head > len(snake_body) + 1:
                        follow_hamiltonian_cycle = True
                        direction_index = 0
                        path_to_check = game_to_graph(path_for_following)
                        path_for_following = neighbors_to_snake_body(path_for_following)
                        food_pos = neighbors_to_snake_body(n_food_pos)
                        snake_body = neighbors_to_snake_body(n_snake_body)
                        snake_head = neighbors_to_snake_body(n_snake_head)
                    else:
                        follow_hamiltonian_cycle = True
                        for i in range(len(hamiltonian_cycle)):
                            if hamiltonian_cycle[i] == snake_head:
                                direction_index = i + 1
                                break
                else:
                    if number_of_nodes - head + tail - 1 > len(snake_body) + 1:
                        follow_hamiltonian_cycle = False
                        direction_index = 0
                        path_to_check = game_to_graph(path_for_following)
                        path_for_following = neighbors_to_snake_body(path_for_following)
                        food_pos = neighbors_to_snake_body(n_food_pos)
                        snake_body = neighbors_to_snake_body(n_snake_body)
                        snake_head = neighbors_to_snake_body(n_snake_head)
                    else:
                        follow_hamiltonian_cycle = True
                        for i in range(len(hamiltonian_cycle)):
                            if hamiltonian_cycle[i] == snake_head:
                                direction_index = i + 1
                                break
                                '''
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

    # Draw the snake body with a black border
    for pos in range(len(snake_body)):
        x, y = snake_body[pos]
        y += 50  # Adjust for window offset

        # Draw the black border (slightly larger rectangle)
        # pygame.draw.rect(game_window, black, pygame.Rect(x, y, cell_size, cell_size))

        # Draw the snake head with 4 different orientations
        if pos == 0:
            next_x, next_y = snake_body[1] if len(snake_body) > 1 else (None, None)
            next_y = next_y + 50 if next_y is not None else None

            # Moving up
            if next_x == x and next_y > y:
                '''
                snake_head_up_img = pygame.image.load("images/snake_head_up.png")
                snake_head_up_img = pygame.transform.scale(snake_head_up_img, (cell_size - 6, cell_size - 3))
                game_window.blit(snake_head_up_img, (x + 3, y + 3))
                '''
                pygame.draw.rect(game_window, blue, pygame.Rect(x + 3, y + 3, cell_size - 6, cell_size - 3))
            # Moving down
            elif next_x == x and next_y < y:
                '''
                snake_head_down_img = pygame.image.load("images/snake_head_down.png")
                snake_head_down_img = pygame.transform.scale(snake_head_down_img, (cell_size - 6, cell_size - 3))
                game_window.blit(snake_head_down_img, (x + 3, y))
                '''
                pygame.draw.rect(game_window, blue, pygame.Rect(x + 3, y, cell_size - 6, cell_size - 3))
            # Moving left
            elif next_x > x and next_y == y:
                '''
                snake_head_left_img = pygame.image.load("images/snake_head_left.png")
                snake_head_left_img = pygame.transform.scale(snake_head_left_img, (cell_size - 3, cell_size - 6))
                game_window.blit(snake_head_left_img, (x + 3, y + 3))
                '''
                pygame.draw.rect(game_window, blue, pygame.Rect(x + 3, y + 3, cell_size - 3, cell_size - 6))
            # Moving right
            elif next_x < x and next_y == y:
                '''
                snake_head_right_img = pygame.image.load("images/snake_head_right.png")
                snake_head_right_img = pygame.transform.scale(snake_head_right_img, (cell_size - 3, cell_size - 6))
                game_window.blit(snake_head_right_img, (x, y + 3))
                '''
                pygame.draw.rect(game_window, blue, pygame.Rect(x, y + 3, cell_size - 3, cell_size - 6))
        else:

            # Body segment logic
            prev_x, prev_y = snake_body[pos - 1]
            next_x, next_y = snake_body[pos + 1] if pos + 1 < len(snake_body) else (None, None)
            prev_y += 50
            next_y = next_y + 50 if next_y is not None else None

            if next_x is not None:
                # Vertical segment
                if prev_x == x == next_x:
                    pygame.draw.rect(game_window, green, pygame.Rect(x + 3, y, cell_size - 6, cell_size))
                # Horizontal segment
                elif prev_y == y == next_y:
                    pygame.draw.rect(game_window, green, pygame.Rect(x, y + 3, cell_size, cell_size - 6))
                # Corner parts
                else:
                    # Bottom-left corner when prev is above
                    if prev_x == x and prev_y < y and next_x > x and next_y == y:
                        pygame.draw.rect(game_window, green, pygame.Rect(x + 3, y, cell_size - 3, cell_size - 3))
                        pygame.draw.rect(game_window, black, pygame.Rect(x + cell_size - 3, y, 3, 3))
                    # Bottom-right corner when prev is above
                    elif prev_x == x and prev_y < y and next_x < x and next_y == y:
                        pygame.draw.rect(game_window, green, pygame.Rect(x, y, cell_size - 3, cell_size - 3))
                        pygame.draw.rect(game_window, black, pygame.Rect(x, y, 3, 3))
                    # Top-left corner when prev is below
                    elif prev_x == x and prev_y > y and next_x > x and next_y == y:
                        pygame.draw.rect(game_window, green, pygame.Rect(x + 3, y + 3, cell_size - 3, cell_size - 3))
                        pygame.draw.rect(game_window, black, pygame.Rect(x + cell_size - 3, y + cell_size - 3, 3, 3))
                    # Top-right corner when prev is below
                    elif prev_x == x and prev_y > y and next_x < x and next_y == y:
                        pygame.draw.rect(game_window, green, pygame.Rect(x, y + 3, cell_size - 3, cell_size - 3))
                        pygame.draw.rect(game_window, black, pygame.Rect(x, y + cell_size - 3, 3, 3))
                    # Left-bottom corner when prev is on right
                    elif prev_x > x and prev_y == y and next_x == x and next_y < y:
                        pygame.draw.rect(game_window, green, pygame.Rect(x + 3, y, cell_size - 3, cell_size - 3))
                        pygame.draw.rect(game_window, black, pygame.Rect(x + cell_size - 3, y, 3, 3))
                    # Right-bottom corner when prev is on left
                    elif prev_x < x and prev_y == y and next_x == x and next_y < y:
                        pygame.draw.rect(game_window, green, pygame.Rect(x, y, cell_size - 3, cell_size - 3))
                        pygame.draw.rect(game_window, black, pygame.Rect(x, y, 3, 3))
                    # Left-top corner when prev is on right
                    elif prev_x > x and prev_y == y and next_x == x and next_y > y:
                        pygame.draw.rect(game_window, green, pygame.Rect(x + 3, y + 3, cell_size - 3, cell_size - 3))
                        pygame.draw.rect(game_window, black, pygame.Rect(x + cell_size - 3, y + cell_size - 3, 3, 3))
                    # Right-top corner when prev is on left
                    elif prev_x < x and prev_y == y and next_x == x and next_y > y:
                        pygame.draw.rect(game_window, green, pygame.Rect(x, y + 3, cell_size - 3, cell_size - 3))
                        pygame.draw.rect(game_window, black, pygame.Rect(x, y + cell_size - 3, 3, 3))
        if pos == len(snake_body) - 1:
            if prev_x == x and prev_y < y:  # Moving up
                pygame.draw.rect(game_window, green, pygame.Rect(x + 3, y, cell_size - 6, cell_size - 3))
            elif prev_x == x and prev_y > y:  # Moving down
                pygame.draw.rect(game_window, green, pygame.Rect(x + 3, y + 3, cell_size - 6, cell_size - 3))
            elif prev_x < x and prev_y == y:  # Moving left
                pygame.draw.rect(game_window, green, pygame.Rect(x, y + 3, cell_size - 3, cell_size - 6))
            elif prev_x > x and prev_y == y:  # Moving right
                pygame.draw.rect(game_window, green, pygame.Rect(x + 3, y + 3, cell_size - 3, cell_size - 6))

    # Draw the food
    pygame.draw.circle(game_window, red, (food_pos[0] + cell_size // 2, food_pos[1] + 50 + cell_size // 2),
                       cell_size // 2)

    # Draw the button to toggle grid
    pygame.draw.rect(game_window, blue, button_rect)
    button_font = pygame.font.SysFont(font, 30)
    button_text = button_font.render('Grid', True, white)
    game_window.blit(button_text, (button_rect.x + 10, button_rect.y + 5))

    #  Draw the button to pause the game
    pygame.draw.rect(game_window, blue, button_pause)
    button_font = pygame.font.SysFont(font, 30)
    button_text = button_font.render('Pause', True, white)
    game_window.blit(button_text, (button_pause.x + 10, button_pause.y + 5))


    # Draw a line to separate UI from the grid
    pygame.draw.line(game_window, white, (0, 50), (frame_size_x, 50), 2)  # Separation line

    # Show score
    show_score(1, white, font, 30)

    # Show number of moves
    show_moves(1, white, font, 30)

    if show_grid:
        for i in range(0, number_of_nodes):
            cycle_font = pygame.font.SysFont(font, 20)
            cycle_surface = cycle_font.render(str(hamiltonian_cylcle_order[i]), True, white)
            x, y = graph_to_game(i)
            cycle_rect = cycle_surface.get_rect(topleft=(x + cell_size - 20, y + 50 + cell_size - 20))
            game_window.blit(cycle_surface, cycle_rect)


    # Show time
    show_stopwatch()

    # Game Over conditions
    if snake_head[0] < 0 or snake_head[0] > frame_size_x - cell_size:
        game_over()
    if snake_head[1] < 0 or snake_head[1] > frame_size_y - cell_size:
        game_over()
    for block in snake_body[1:]:
        if snake_head == block:
            game_over()

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second / Refresh Rate
    fps_controller.tick(difficulty)
    ''''''
