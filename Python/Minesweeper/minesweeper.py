import pygame
import sys
import random
import math
import json
import unittest

# Initialise Pygame
pygame.init()

# Define constants
FRAMERATE = 30
WIDTH = 1080
HEIGHT = 950
BOARDER = 10
BOARDER_THICKNESS = 4
SHAKE_DURATION = 4
SHAKE_AMOUNT = BOARDER // 3
TITLE_FONT = pygame.font.Font('Python/Minesweeper/vgasys.ttf', 50)
TITLE_FONT_SMALL = pygame.font.Font('Python/Minesweeper/vgasys.ttf', 40)
FONT = pygame.font.Font(None, 36)

# Define Images
TIMER_IMG = pygame.transform.scale(pygame.image.load('Python/Minesweeper/timer.png'), (30, 30))
TIMER_IMG_LARGE = pygame.transform.scale(pygame.image.load('Python/Minesweeper/timer.png'), (100, 100))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
DARK_GRAY = (169, 169, 169)

BLUE = (25, 118, 210)
GREEN = (56, 141, 60)
PURPLE = (123, 31, 162)
YELLOW = (252, 186, 3)
ORANGE = (253, 142, 24)
BRIGHT_RED = (224, 22, 46)
RED = (210, 47, 47)
DARK_BLUE = (56, 22, 224)
AQUA = (29, 171, 140)

BROWN = (215, 184, 153)
LIGHT_BROWN = (229, 194, 159)
LIGHT_GREEN = (142, 204, 57)
LIGHTER_GREEN = (167, 217, 72)
DARK_GREEN = (135, 175, 58)
DARKER_GREEN = (60, 79, 22)
LIGHT_BLUE = (74, 192, 253)
LIGHTER_BLUE = (125, 211, 255)
HOVER_LIGHT_GREEN = (185, 221, 119)
HOVER_LIGHTER_GREEN = (191, 225, 125)

# Define Palettes
GRAY_PALETTE = [GRAY, DARK_GRAY]
BROWN_PALETTE = [LIGHT_BROWN, BROWN, LIGHT_BROWN, BROWN]
GREEN_PALETTE = [LIGHTER_GREEN, LIGHT_GREEN, HOVER_LIGHTER_GREEN, HOVER_LIGHT_GREEN]
BLUE_PALETTE = [LIGHT_BLUE, LIGHTER_BLUE]
CHOSEN_PALETTES = [GREEN_PALETTE, BROWN_PALETTE, DARK_GREEN, LIGHT_BLUE]

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper Reloaded")

# Function to initialise the game board
def initialise_board(clicked_row, clicked_col):
    """
    Initialises a Minesweeper game board with mines randomly placed.

    Args:
        rows (int): Number of rows in the Minesweeper board.
        cols (int): Number of columns in the Minesweeper board.
        mines (int): Number of mines to be placed on the board.

    Returns:
        board (list): A 2D List containing the Initialised board.

    Initialises a 2D list to represent the Minesweeper board with zeros (no mines).
    Randomly places the specified number of mines on the board.
    Calculates and sets the number of neighboring mines for each cell.
    Initialises a 2D list to indicate whether each cell is revealed (initially all set to False).
    Returns the Initialised board and the revealed state.
    """
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    # Randomly place mines on the board, avoiding the clicked cell
    for _ in range(NOS_MINES):
        row, col = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
        # Stops mines being placed in the same location
        while board[row][col] == -1 or (row in range(clicked_row - 1, clicked_row + 2) and col in range(clicked_col - 1, clicked_col + 2)):
            row, col = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
        board[row][col] = -1
        # Increment the surrounding cells
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if 0 <= i < ROWS and 0 <= j < COLS and board[i][j] != -1:
                    board[i][j] += 1
    return board

# Function to draw the game board
def draw_board(board, revealed, flagged, game_over=False, game_won=False, start_time=pygame.time.get_ticks()):
    """
    Draws the Minesweeper game board on the screen.

    Args:
        board (list): 2D list representing the Minesweeper board.
        revealed (list): 2D list indicating whether each cell is revealed.
        flagged (list): 2D list indicating whether each cell is flagged.
        game_over (bool, optional): Boolean indicating whether the game is over. Defaults to False.
        game_won (bool, optional): Boolean indicating whether the game is won. Defaults to False.
        start_time (int, optional): The time when the game started. Defaults to the current time using pygame.time.get_ticks().

    Returns:
        None

    Draws cells based on their state (revealed, flagged, or mine) and displays numbers or mines accordingly.
    Handles color-coding and hover effects for cells.
    Calls draw_hud to display the Flags left and Timer.
    """
    for row in range(ROWS):
        for col in range(COLS):
            cell_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if revealed[row][col]:
                # Create checkerboard pattern
                colour = CHOSEN_PALETTES[1][0] if (row + col) % 2 == 0 else CHOSEN_PALETTES[1][1]
                pygame.draw.rect(screen, colour, cell_rect)
                # Colour the numbers, depending on how many mines are near
                if board[row][col] > 0:
                    number = str(board[row][col])
                    match number:
                        case '2':
                            font_colour = GREEN
                        case '3':
                            font_colour = RED
                        case '4':
                            font_colour = DARK_BLUE
                        case '5':
                            font_colour = ORANGE
                        case '6':
                            font_colour = AQUA
                        case '7':
                            font_colour = BLACK
                        case '8':
                            font_colour = GRAY
                        case _:
                            font_colour = BLUE
                    text = FONT.render(number, True, font_colour)
                    text_rect = text.get_rect(center=cell_rect.center)
                    screen.blit(text, text_rect)
                # Draw mines
                elif board[row][col] == -1 and not game_over:
                    pygame.draw.circle(screen, CHOSEN_PALETTES[2] if game_won else BLACK, cell_rect.center, CELL_SIZE // 2 - BOARDER)
            # Draw Flags
            elif flagged[row][col]:
                # Checkerboard pattern
                colour = CHOSEN_PALETTES[0][0] if (row + col) % 2 == 0 else CHOSEN_PALETTES[0][1]
                # Flag polygon
                pygame.draw.rect(screen, colour, cell_rect)
                pygame.draw.polygon(screen, RED, [(col * CELL_SIZE + CELL_SIZE // 3 - 2, (row + 1) * CELL_SIZE - BOARDER), 
                                                  (col * CELL_SIZE + CELL_SIZE // 3 - 2, row * CELL_SIZE + BOARDER), 
                                                  (col * CELL_SIZE + CELL_SIZE // 3 + 2, row * CELL_SIZE + BOARDER),
                                                  (col * CELL_SIZE + CELL_SIZE - BOARDER, row * CELL_SIZE + CELL_SIZE // 3),
                                                  (col * CELL_SIZE + CELL_SIZE // 3 + 2, row * CELL_SIZE + 2 * (CELL_SIZE // 3)),
                                                  (col * CELL_SIZE + CELL_SIZE // 3 + 2, (row + 1) * CELL_SIZE - 5)])

            else:
                # Hover effect
                hovered = cell_rect.collidepoint(pygame.mouse.get_pos())
                colour = CHOSEN_PALETTES[0][2 if hovered else 0] if (row + col) % 2 == 0 else CHOSEN_PALETTES[0][3 if hovered else 1]
                pygame.draw.rect(screen, colour, cell_rect)
    draw_hud(flagged, start_time)

# Function to draw the HUD (Flags left, and timer)
def draw_hud(flagged, start_time):
    """
    Draws the Heads-Up Display (HUD) for the Minesweeper game.

    Args:
        flagged (list): A 2D list representing flagged cells.
        start_time (int): The starting time of the game.

    Draws the HUD displaying the number of remaining flags, and the game timer.
    """
    # Define variables
    flag_size = 30
    offset_y = (HEIGHT - ROWS * CELL_SIZE) // 2 - (flag_size // 2) + 5
    offset_x = 50
    # Count how many flags are placed
    nos_flags = [i for row in flagged for i in row].count(True)
    flag_text = FONT.render(f"{NOS_MINES - nos_flags}", True, WHITE)
    flag_rect = flag_text.get_rect(center=(WIDTH // 3, ROWS * CELL_SIZE + (HEIGHT - ROWS * CELL_SIZE) // 2))
    pygame.draw.polygon(screen, RED, [(WIDTH // 3 - offset_x + flag_size // 3 - 2, HEIGHT - offset_y), 
                                      (WIDTH // 3 - offset_x + flag_size // 3 - 2, HEIGHT - offset_y - flag_size), 
                                      (WIDTH // 3 - offset_x + flag_size // 3 + 2, HEIGHT - offset_y - flag_size),
                                      (WIDTH // 3 - offset_x + flag_size, HEIGHT - offset_y - flag_size + flag_size // 3),
                                      (WIDTH // 3 - offset_x + flag_size // 3 + 2, HEIGHT - offset_y - flag_size + 2 * (flag_size // 3)),
                                      (WIDTH // 3 - offset_x + flag_size // 3 + 2, HEIGHT - offset_y + 5)])

    # Draw timer
    timer_text = FONT.render(f"{(pygame.time.get_ticks() - start_time) / 1000:.1f}", True, WHITE)
    timer_rect = timer_text.get_rect(center=(2 * (WIDTH // 3), ROWS * CELL_SIZE + (HEIGHT - ROWS * CELL_SIZE) // 2))

    timer_img_rect = pygame.Rect(2 * (WIDTH // 3) - offset_x - 25, HEIGHT - offset_y - flag_size + 2, flag_size, flag_size)

    screen.blit(flag_text, flag_rect)
    screen.blit(timer_text, timer_rect)
    screen.blit(TIMER_IMG, timer_img_rect)

# Function to handle recursive flood fill
def flood_fill(row, col, board, revealed, flagged):
    """
    Recursively performs flood fill on the Minesweeper board.

    Args:
        row (int): The row index of the starting tile.
        col (int): The column index of the starting tile.
        board (list): A 2D list representing the Minesweeper game board.
        revealed (list): A 2D list indicating whether each cell is revealed.
        flagged (list): A 2D list indicating whether each cell is flagged.

    Recursively reveals connected tiles on the board using flood fill algorithm.
    Stops recursion on revealed or flagged tiles and tiles with non-zero mine count.
    """
    # Only move to tiles that are not revealed, this stops an infinite recursive path
    if not revealed[row][col]:
        # If the tile is not 0, stop recursing and return
        if board[row][col] != 0:
            revealed[row][col] = True
            flagged[row][col] = False
            return
        # Otherwise keep recursing, making sure to mark the tiles already visisted
        else:
            revealed[row][col] = True
            flagged[row][col] = False
            if row < ROWS - 1:
                flood_fill(row + 1, col, board, revealed, flagged)
            if row > 0:
                flood_fill(row - 1, col, board, revealed, flagged)
            if col < COLS - 1:
                flood_fill(row, col + 1, board, revealed, flagged)
            if col > 0:
                flood_fill(row, col - 1, board, revealed, flagged)
            if row < ROWS - 1 and col < COLS - 1:
                flood_fill(row + 1, col + 1, board, revealed, flagged)
            if row < ROWS - 1 and col > 0:
                flood_fill(row + 1, col - 1, board, revealed, flagged)
            if row > 0 and col < COLS - 1:
                flood_fill(row - 1, col + 1, board, revealed, flagged)
            if row > 0 and col > 0:
                flood_fill(row - 1, col - 1, board, revealed, flagged)

# Function to play the explosion animation
def end_game(row, col, board, revealed, flagged):
    """
    Initiates the end-game animation for a Minesweeper cell explosion.

    Args:
        row (int): The row index of the cell to explode.
        col (int): The column index of the cell to explode.
        board (list): A 2D list representing the Minesweeper game board.
        revealed (list): A 2D list indicating whether each cell is revealed.
        flagged (list): A 2D list indicating whether each cell is flagged.

    Initiates an explosion animation at the specified cell position.
    The animation includes shaking, explosions, and a circular fade-out effect.
    """
    cell_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    for i in range(SHAKE_DURATION * FRAMERATE):
        pygame.time.delay(10)
        x_shake, y_shake = random.randint(-SHAKE_AMOUNT, SHAKE_AMOUNT), random.randint(-SHAKE_AMOUNT, SHAKE_AMOUNT)
        draw_board(board, revealed, flagged, game_over=True)
        pygame.draw.circle(screen, BLACK, cell_rect.move(x_shake, y_shake).center, CELL_SIZE // 2 - BOARDER)
        if i % 10 == 0:
            x_off, y_off = random.randint(-(CELL_SIZE // 4), CELL_SIZE // 4), random.randint(-(CELL_SIZE // 4), CELL_SIZE // 4)
        pygame.draw.circle(screen, ORANGE, cell_rect.move(x_off, y_off).center, CELL_SIZE // 4 - BOARDER)
        pygame.draw.circle(screen, RED, cell_rect.move(x_off, y_off).center, CELL_SIZE // 5 - BOARDER)
        pygame.display.flip()

    cell_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    max_radius = max([
            math.dist(cell_rect.center, (WIDTH, HEIGHT)), 
            math.dist(cell_rect.center, (0, HEIGHT)),
            math.dist(cell_rect.center, (0, 0)),
            math.dist(cell_rect.center, (WIDTH, 0))
        ])
    for radius in range(int(CELL_SIZE // 2 - BOARDER), math.ceil(max_radius)):
        pygame.draw.circle(screen, BLACK, cell_rect.center, radius)
        pygame.display.flip()

# Function to show a win animation
def win_game(board, revealed, flagged, end_time):
    """
    Initiates the win-game animation for a Minesweeper game.

    Args:
        board (list): A 2D list representing the Minesweeper game board.
        revealed (list): A 2D list indicating whether each cell is revealed.
        flagged (list): A 2D list indicating whether each cell is flagged.
        end_time (int): The timestamp when the game was won.

    Initiates an animation where all non-mine cells are revealed and a
    colorful celebration occurs, including expanding circles and a fading screen.
    """
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] != -1:
                board[row][col] = 0
                flagged[row][col] = False
    max_radius = CELL_SIZE // 2 - BOARDER
    for row in range(ROWS):
        for col in range(COLS):
            cell_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            revealed[row][col] = True
            draw_board(board, revealed, flagged, game_won=True, start_time=end_time)
            if board[row][col] == -1:
                pygame.draw.circle(screen, BLACK, cell_rect.center, max_radius)
                for radius in range(max_radius):
                    pygame.time.delay(int((0.5/max_radius) * 1000))
                    pygame.draw.circle(screen, CHOSEN_PALETTES[2], cell_rect.center, radius)
                    pygame.display.flip()
            pygame.display.flip()
    for y in range(HEIGHT):
        pygame.time.delay(int(1/HEIGHT) * 1000)
        pygame.draw.rect(screen, CHOSEN_PALETTES[3], pygame.Rect(0, 0, WIDTH, y))
        pygame.display.flip()

# Function to initialise a new Minesweeper game.
def start_game():
    """
    Initialises a new Minesweeper game.

    Returns:
        tuple: A tuple containing the initial state of the game.
            The tuple includes:
                - revealed (list): A 2D list indicating whether each cell is revealed.
                - flagged (list): A 2D list indicating whether each cell is flagged.
                - board (list): A 2D list representing the Minesweeper game board.
                - start_time (int): The timestamp when the game started.

    Initialises a new Minesweeper game by creating empty game board, setting up initial
    revealed and flagged states, and gradually revealing the board with a circular animation.
    """
    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for radius in range(math.ceil(math.dist((0, 0), ((WIDTH // 2, HEIGHT // 2)))), 0, -2):
        draw_board(board, revealed, flagged)
        pygame.draw.circle(screen, BLACK, (WIDTH // 2, HEIGHT // 2), radius)
        pygame.display.flip()
    start_time = pygame.time.get_ticks()
    return revealed, flagged, board, start_time

# Function to write times to json after a game win
def write_to_json(total_time):
    """
    Writes the total time of a completed Minesweeper game to a JSON file.

    Args:
        total_time (int): The total time in milliseconds taken to complete the game.

    Opens the 'times.json' file, reads the existing data, appends the total time to
    the appropriate difficulty level, and writes the updated data back to the file.
    """
    with open('Python/Minesweeper/times.json', 'r+') as file:
        file_data = json.load(file)
        file_data[DIFFICULTY].append(total_time / 1000)
        file.seek(0)
        json.dump(file_data, file, indent=2)

# Function to read json files when accessing leaderboard
def read_json():
    """
    Reads the Minesweeper leaderboard data from a JSON file.

    Opens the 'times.json' file, reads the data, and sorts the times for each
    difficulty level in ascending order. It pads the list with empty strings to
    ensure a fixed size of 10 entries.

    Returns:
        dict: A dictionary containing difficulty levels as keys and sorted lists
              of completion times as values, padded to a maximum of 10 entries.
    """
    with open('Python/Minesweeper/times.json', 'r') as file:
        file_data = json.load(file)
        for key, value in file_data.items():
            file_data[key].sort()
            file_data[key] = value + [''] * (10 - len(value) if len(value) <= 10 else 0)
    return file_data

# Function to draw the main menu
def draw_menu():
    """
    Draws the main menu of Minesweeper Reloaded.

    Renders the title, "Minesweeper Reloaded," as well as options to play, view
    the leaderboard, and quit the game. The menu highlights the selected option
    on mouse hover.

    Returns:
        Tuple[pygame.Rect, pygame.Rect, pygame.Rect]: Rectangles representing the
        clickable areas for Play, Leaderboard, and Quit options, respectively.

    Notes:
        The function assumes a global variable `screen` is available.

    Example:
        play_rect, leaderboard_rect, quit_rect = draw_menu()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if play_rect.collidepoint(event.pos):
                    # Handle Play button click
                elif leaderboard_rect.collidepoint(event.pos):
                    # Handle Leaderboard button click
                elif quit_rect.collidepoint(event.pos):
                    # Handle Quit button click
    """
    title_text = TITLE_FONT.render("Minesweeper Reloaded", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 75))

    play_text = TITLE_FONT.render("Play", True, WHITE)
    play_rect = play_text.get_rect(center=(WIDTH // 2, 250))
    hovered = play_rect.inflate(250, 100).collidepoint(pygame.mouse.get_pos())
    if hovered:
        pygame.draw.rect(screen, (100, 100, 100), play_rect.inflate(250, 100))
    pygame.draw.rect(screen, ((225, 225, 225) if hovered else (255, 255, 255)), play_rect.inflate(250, 100), 4)

    leaderboard_text = TITLE_FONT.render("Leaderboard", True, WHITE)
    leaderboard_rect = leaderboard_text.get_rect(center=(WIDTH // 2, 500))
    hovered = play_rect.move(0, 250).inflate(250, 100).collidepoint(pygame.mouse.get_pos())
    if hovered:
        pygame.draw.rect(screen, (100, 100, 100), play_rect.move(0, 250).inflate(250, 100))
    pygame.draw.rect(screen, ((225, 225, 225) if hovered else (255, 255, 255)), play_rect.move(0, 250).inflate(250, 100), 4)

    quit_text = TITLE_FONT.render("Quit", True, WHITE)
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, 750))
    hovered = play_rect.move(0, 500).inflate(250, 100).collidepoint(pygame.mouse.get_pos())
    if hovered:
        pygame.draw.rect(screen, (100, 100, 100), play_rect.move(0, 500).inflate(250, 100))
    pygame.draw.rect(screen, ((225, 225, 225) if hovered else (255, 255, 255)), play_rect.move(0, 500).inflate(250, 100), 4)

    screen.blit(title_text, title_rect)
    screen.blit(play_text, play_rect)
    screen.blit(leaderboard_text, leaderboard_rect)
    screen.blit(quit_text, quit_rect)

    return play_rect.inflate(250, 100), play_rect.move(0, 250).inflate(250, 100), quit_rect.inflate(250, 100)

# Function to draw the select difficulty menu
def draw_difficulty():
    """
    Draws the difficulty selection menu of Minesweeper Reloaded.

    Renders the title, "Select Difficulty," and options to choose Easy, Medium,
    or Hard difficulty. The menu highlights the selected option on mouse hover.

    Returns:
        Tuple[pygame.Rect, pygame.Rect, pygame.Rect]: Rectangles representing the
        clickable areas for Easy, Medium, and Hard difficulty options, respectively.

    Notes:
        The function assumes a global variable `screen` is available.

    Example:
        easy_rect, medium_rect, hard_rect = draw_difficulty()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if easy_rect.collidepoint(event.pos):
                    # Handle Easy difficulty selection
                elif medium_rect.collidepoint(event.pos):
                    # Handle Medium difficulty selection
                elif hard_rect.collidepoint(event.pos):
                    # Handle Hard difficulty selection
    """
    title_text = TITLE_FONT.render("Select Difficulty", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 75))

    easy_text = TITLE_FONT.render("Easy", True, WHITE)
    easy_rect = easy_text.get_rect(center=(WIDTH // 2, 250))
    hovered = easy_rect.inflate(250, 100).collidepoint(pygame.mouse.get_pos())
    if hovered:
        pygame.draw.rect(screen, (100, 100, 100), easy_rect.inflate(250, 100))
    pygame.draw.rect(screen, ((225, 225, 225) if hovered else (255, 255, 255)), easy_rect.inflate(250, 100), 4)

    medium_text = TITLE_FONT.render("Medium", True, WHITE)
    medium_rect = medium_text.get_rect(center=(WIDTH // 2, 500))
    hovered = easy_rect.move(0, 250).inflate(250, 100).collidepoint(pygame.mouse.get_pos())
    if hovered:
        pygame.draw.rect(screen, (100, 100, 100), easy_rect.move(0, 250).inflate(250, 100))
    pygame.draw.rect(screen, ((225, 225, 225) if hovered else (255, 255, 255)), easy_rect.move(0, 250).inflate(250, 100), 4)

    hard_text = TITLE_FONT.render("Hard", True, WHITE)
    hard_rect = hard_text.get_rect(center=(WIDTH // 2, 750))
    hovered = easy_rect.move(0, 500).inflate(250, 100).collidepoint(pygame.mouse.get_pos())
    if hovered:
        pygame.draw.rect(screen, (100, 100, 100), easy_rect.move(0, 500).inflate(250, 100))
    pygame.draw.rect(screen, ((225, 225, 225) if hovered else (255, 255, 255)), easy_rect.move(0, 500).inflate(250, 100), 4)

    screen.blit(title_text, title_rect)
    screen.blit(easy_text, easy_rect)
    screen.blit(medium_text, medium_rect)
    screen.blit(hard_text, hard_rect)

    return easy_rect.inflate(250, 100), medium_rect.inflate(250, 100), hard_rect.inflate(250, 100)

# Function to draw the retry screen
def draw_game_lost():
    """
    Draws the game over screen with the option to retry.

    Renders the title, "Game Over!" and a "Retry" option. The function highlights
    the "Retry" option on mouse hover.

    Returns:
        pygame.Rect: Rectangle representing the clickable area for the "Retry" option.

    Notes:
        The function assumes a global variable `screen` is available.

    Example:
        retry_rect = draw_game_lost()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and retry_rect.collidepoint(event.pos):
                # Handle retrying the game after a loss
    """
    title_text = TITLE_FONT.render("Game Over!", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 75))

    retry_text = TITLE_FONT.render("Retry", True, WHITE)
    retry_rect = retry_text.get_rect(center=(WIDTH // 2, 250))
    hovered = retry_rect.inflate(250, 100).collidepoint(pygame.mouse.get_pos())
    if hovered:
        pygame.draw.rect(screen, (100, 100, 100), retry_rect.inflate(250, 100))
    pygame.draw.rect(screen, ((225, 225, 225) if hovered else (255, 255, 255)), retry_rect.inflate(250, 100), 4)

    screen.blit(title_text, title_rect)
    screen.blit(retry_text, retry_rect)
    
    return retry_rect.inflate(250, 100)

# Function to draw the game won screen with final time
def draw_game_won(total_time):
    """
    Draws the game won screen with congratulations, final time, and a "Play Again" option.

    Args:
        total_time (float): The total time taken to complete the game, in milliseconds.

    Returns:
        pygame.Rect: Rectangle representing the clickable area for the "Play Again" option.

    Notes:
        The function assumes global variables `screen`, `TIMER_IMG_LARGE`, and `WHITE` are available.

    Example:
        play_again_rect = draw_game_won(total_time)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and play_again_rect.collidepoint(event.pos):
                # Handle restarting the game after a win
    """
    title_text = TITLE_FONT.render("Congratulations!", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 75))

    timer_img_rect = pygame.Rect(WIDTH // 2 - 50 - 100, HEIGHT // 2 - 50 - 100, 100, 100)
    
    time_text = TITLE_FONT.render(f"{(total_time / 1000):.1f}", True, WHITE)
    time_rect = title_text.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 - 95))

    again_text = TITLE_FONT.render("Play Again", True, WHITE)
    again_rect = again_text.get_rect(center=(WIDTH // 2, 750))
    hovered = again_rect.inflate(250, 100).collidepoint(pygame.mouse.get_pos())
    if hovered:
        pygame.draw.rect(screen, (100, 100, 100), again_rect.inflate(250, 100))
    pygame.draw.rect(screen, ((225, 225, 225) if hovered else (255, 255, 255)), again_rect.inflate(250, 100), 4)

    screen.blit(title_text, title_rect)
    screen.blit(TIMER_IMG_LARGE, timer_img_rect)
    screen.blit(time_text, time_rect)
    screen.blit(again_text, again_rect)
    
    return again_rect.inflate(250, 100)

# Function to draw the leaderboards
def draw_leaderboard(file_data):
    """
    Draws the leaderboard screen with rankings, difficulty levels, and corresponding completion times.

    Args:
        file_data (dict): A dictionary containing time data for different difficulty levels.

    Returns:
        pygame.Rect: Rectangle representing the clickable area for the "Back" option.

    Notes:
        The function assumes global variables `screen`, `WIDTH`, `WHITE`, `TITLE_FONT`, `TITLE_FONT_SMALL`,
        and other relevant constants are available.

    Example:
        back_rect = draw_leaderboard(file_data)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and back_rect.collidepoint(event.pos):
                # Handle going back to the main menu
    """
    offset_x = 75
    title_text = TITLE_FONT.render("Leaderboard", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 75))

    nos_text = TITLE_FONT.render("#", True, WHITE)
    nos_rect = nos_text.get_rect(center=(WIDTH // 8 - 25, 200))

    numbers_text = TITLE_FONT_SMALL.render(f"{'\n'.join([f' {str(i + 1)}' if i != 9 else str(i + 1) for i in range(10)])}", True, WHITE)
    numbers_rect = numbers_text.get_rect(center=(WIDTH // 8 - 25, 475))

    easy_text = TITLE_FONT.render("Easy", True, WHITE)
    easy_rect = easy_text.get_rect(center=(WIDTH // 5 + offset_x, 200))

    medium_text = TITLE_FONT.render("Medium", True, WHITE)
    medium_rect = medium_text.get_rect(center=(WIDTH // 2 + offset_x, 200))

    hard_text = TITLE_FONT.render("Hard", True, WHITE)
    hard_rect = hard_text.get_rect(center=(4 * (WIDTH // 5) + offset_x - 25, 200))

    pygame.draw.line(screen, WHITE, (WIDTH // 8 - 75, 235), (7 * (WIDTH // 8) + 75, 235), 4)
    pygame.draw.line(screen, WHITE, (WIDTH // 8 + 25, 150), (WIDTH // 8 + 25, 700), 4)
    pygame.draw.line(screen, WHITE, (WIDTH // 3 + offset_x, 150), (WIDTH // 3 + offset_x, 700), 4)
    pygame.draw.line(screen, WHITE, (2 * (WIDTH // 3) + offset_x, 150), (2 * (WIDTH // 3) + offset_x, 700), 4)

    back_text = TITLE_FONT.render("Back <-", True, WHITE)
    back_rect = back_text.get_rect(center=(WIDTH // 2, 850))
    hovered = back_rect.inflate(250, 100).collidepoint(pygame.mouse.get_pos())
    if hovered:
        pygame.draw.rect(screen, (100, 100, 100), back_rect.inflate(250, 100))
    pygame.draw.rect(screen, ((225, 225, 225) if hovered else (255, 255, 255)), back_rect.inflate(250, 100), 4)

    easy_times_text = TITLE_FONT_SMALL.render('\n'.join([(f"{round(float(file_data['easy'][i]), 1) if file_data['easy'][i] != '' else '':^10}").rjust(3) for i in range(10)]), True, WHITE)
    easy_times_rect = easy_times_text.get_rect(center=(WIDTH // 5 + offset_x, 475))

    medium_times_text = TITLE_FONT_SMALL.render('\n'.join([(f"{round(float(file_data['medium'][i]), 1) if file_data['medium'][i] != '' else '':^10}").rjust(3) for i in range(10)]), True, WHITE)
    medium_times_rect = medium_times_text.get_rect(center=(WIDTH // 2 + offset_x, 475))

    hard_times_text = TITLE_FONT_SMALL.render('\n'.join([(f"{round(float(file_data['hard'][i]), 1) if file_data['hard'][i] != '' else '':^10}").rjust(3) for i in range(10)]), True, WHITE)
    hard_times_rect = hard_times_text.get_rect(center=(4 * (WIDTH // 5) + offset_x - 25, 475))

    screen.blit(title_text, title_rect)
    screen.blit(nos_text, nos_rect)
    screen.blit(numbers_text, numbers_rect)
    screen.blit(easy_times_text, easy_times_rect)
    screen.blit(medium_times_text, medium_times_rect)
    screen.blit(hard_times_text, hard_times_rect)
    screen.blit(easy_text, easy_rect)
    screen.blit(medium_text, medium_rect)
    screen.blit(hard_text, hard_rect)
    screen.blit(back_text, back_rect)

    return back_rect.inflate(250, 100)

# Main game loop
def main():
    """
    Main game loop handling events, game states, and screen updates.

    Notes:
        The function assumes global variables and constants, such as `screen`, `WIDTH`, `HEIGHT`, `WHITE`,
        `FRAMERATE`, `CELL_SIZE`, `NOS_MINES`, `DIFFICULTY`, `COLS`, `ROWS`, and other relevant variables, 
        are available.
    """
    clock = pygame.time.Clock()
    game_over = True
    main_menu = True
    difficulty_select = False
    game_won = False
    game_lost = False
    setup = False
    leaderboard = False

    # Globals
    global COLS, ROWS, CELL_SIZE, NOS_MINES, DIFFICULTY

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if not game_over:
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        if event.button == 1 and not revealed[row][col]:
                            # If it is the first click, generate the mines
                            if not any([any(row) for row in revealed]):
                                board = initialise_board(row, col)
                            # Left click to reveal cell, use flood fill recursion
                            flood_fill(row, col, board, revealed, flagged)
                            if board[row][col] == -1:
                                game_over = True
                                game_lost = True
                                end_game(row, col, board, revealed, flagged)
                        elif event.button == 3 and not revealed[row][col]:
                            # Right click to flag/unflag cell
                            if flagged[row][col]:
                                flagged[row][col] = not flagged[row][col]
                            # Cannot place more flags than there are mines
                            elif not flagged[row][col] and [i for row in flagged for i in row].count(True) < NOS_MINES:
                                flagged[row][col] = not flagged[row][col]
                        # Check if the game is won
                        if [cell for row in revealed for cell in row].count(False) == NOS_MINES and not game_over:
                            # Calculate time taken
                            end_time = pygame.time.get_ticks()
                            total_time = end_time - start_time
                            # Write the time to json
                            write_to_json(total_time)
                            game_over = True
                            game_won = True
                            # Play win animation
                            win_game(board, revealed, flagged, end_time)
                # On the main menu
                elif main_menu:
                    if play_rect.collidepoint(x, y):
                        difficulty_select = True
                        main_menu = False
                    elif leaderboard_rect.collidepoint(x, y):
                        leaderboard = True
                        file_data = read_json()
                        main_menu = False
                    elif quit_rect.collidepoint(x, y):
                        pygame.quit()
                        sys.exit()
                # On the difficulty select screen
                elif difficulty_select:
                    if easy.collidepoint(x, y):
                        COLS, ROWS = 10, 8
                        CELL_SIZE = WIDTH // COLS
                        NOS_MINES = 10
                        DIFFICULTY = "easy"
                        setup = True
                    elif medium.collidepoint(x, y):
                        COLS, ROWS = 18, 14
                        CELL_SIZE = WIDTH // COLS
                        NOS_MINES = 40
                        DIFFICULTY = "medium"
                        setup = True
                    elif hard.collidepoint(x, y):
                        COLS, ROWS = 24, 20
                        CELL_SIZE = WIDTH // COLS
                        NOS_MINES = 99
                        DIFFICULTY = "hard"
                        setup = True
                    if setup:
                        setup = False
                        game_over = False
                        difficulty_select = False
                        revealed, flagged, board, start_time = start_game()
                # On the retry screen
                elif game_lost:
                    if retry.collidepoint(x, y):
                        game_lost = False
                        main_menu = True
                # On the game won screen
                elif game_won:
                    if again.collidepoint(x, y):
                        game_won = False
                        main_menu = True
                # On the leaderboard screen
                elif leaderboard:
                    if back.collidepoint(x, y):
                        leaderboard = False
                        main_menu = True
                # Catch no screen error
                else:
                    print("Error setting flags")
                
        if not game_over:
            screen.fill(BLACK)
            draw_board(board, revealed, flagged, start_time=start_time)
        elif main_menu:
            screen.fill(BLACK)
            play_rect, leaderboard_rect, quit_rect = draw_menu()
        elif difficulty_select:
            screen.fill(BLACK)
            easy, medium, hard = draw_difficulty()
        elif game_lost:
            screen.fill(BLACK)
            retry = draw_game_lost()
        elif game_won:
            screen.fill(LIGHT_BLUE)
            again = draw_game_won(total_time)
        elif leaderboard:
            screen.fill(BLACK)
            back = draw_leaderboard(file_data)
        else:
            print("Error handling flags")
        
        # Main display update and clock tick
        pygame.display.flip()
        clock.tick(FRAMERATE)

# Testing class
class TestMinesweeper(unittest.TestCase):
    """
    A testing class for Minesweeper functionality.

    Attributes:
        ROWS (int): The number of rows in the Minesweeper board.
        COLS (int): The number of columns in the Minesweeper board.
        NOS_MINES (int): The number of mines in the Minesweeper board.

    Example:
        unittest.main()

    """
    def test_board(self):
        """
        Test the initialization of the Minesweeper board.

        This test ensures that the Minesweeper board is correctly initialised with the specified number of
        rows, columns, and mines. It checks the dimensions of the board and each row.

        Returns:
            None

        Example:
            self.test_board()

        """
        global ROWS, COLS, NOS_MINES
        ROWS = 8
        COLS = 10
        NOS_MINES = 10
        board = initialise_board(0, 0)
        self.assertEqual(len(board), ROWS)
        for row in board:
            self.assertEqual(len(row), COLS)

# Run the game
if __name__ == "__main__":
    # unittest.main()
    main()
