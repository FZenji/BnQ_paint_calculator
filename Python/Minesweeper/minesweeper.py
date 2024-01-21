import pygame
import sys
import random
import math
import time

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
FONT = pygame.font.Font(None, 36)

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
HOVER_LIGHT_GREEN = (185, 221, 119)
HOVER_LIGHTER_GREEN = (191, 225, 125)

# Define Palettes
GRAY_PALETTE = [GRAY, DARK_GRAY]
BROWN_PALETTE = [LIGHT_BROWN, BROWN]
GREEN_PALETTE = [LIGHTER_GREEN, LIGHT_GREEN, HOVER_LIGHTER_GREEN, HOVER_LIGHT_GREEN]
CHOSEN_PALETTES = [GREEN_PALETTE, BROWN_PALETTE]

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper Reloaded")

# Function to initialise the game board
def initialise_board(clicked_row, clicked_col):
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
def draw_board(board, revealed, flagged, game_over=False):
    for row in range(ROWS):
        for col in range(COLS):
            cell_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if revealed[row][col]:
                colour = CHOSEN_PALETTES[1][0] if (row + col) % 2 == 0 else CHOSEN_PALETTES[1][1]
                pygame.draw.rect(screen, colour, cell_rect)
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
                elif board[row][col] == -1 and not game_over:
                    pygame.draw.circle(screen, BLACK, cell_rect.center, CELL_SIZE // 2 - BOARDER)
            elif flagged[row][col]:
                colour = CHOSEN_PALETTES[0][0] if (row + col) % 2 == 0 else CHOSEN_PALETTES[0][1]
                pygame.draw.rect(screen, colour, cell_rect)
                pygame.draw.polygon(screen, RED, [(col * CELL_SIZE + CELL_SIZE // 3 - 2, (row + 1) * CELL_SIZE - BOARDER), 
                                                  (col * CELL_SIZE + CELL_SIZE // 3 - 2, row * CELL_SIZE + BOARDER), 
                                                  (col * CELL_SIZE + CELL_SIZE // 3 + 2, row * CELL_SIZE + BOARDER),
                                                  (col * CELL_SIZE + CELL_SIZE - BOARDER, row * CELL_SIZE + CELL_SIZE // 3),
                                                  (col * CELL_SIZE + CELL_SIZE // 3 + 2, row * CELL_SIZE + 2 * (CELL_SIZE // 3)),
                                                  (col * CELL_SIZE + CELL_SIZE // 3 + 2, (row + 1) * CELL_SIZE - 5)])

            else:
                hovered = cell_rect.collidepoint(pygame.mouse.get_pos())
                colour = CHOSEN_PALETTES[0][3 if hovered else 0] if (row + col) % 2 == 0 else CHOSEN_PALETTES[0][3 if hovered else 1]
                pygame.draw.rect(screen, colour, cell_rect)

def flood_fill(row, col, board, revealed, flagged):
    # if 0 < row < ROWS - 1 and 0 < col < COLS - 1 and board[row][col] != 0 and not revealed[row][col]:
    if not revealed[row][col]:
        if board[row][col] != 0:
            revealed[row][col] = True
            flagged[row][col] = False
            return
        else:
            revealed[row][col] = True
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
    cell_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    for i in range(SHAKE_DURATION * FRAMERATE):
        time.sleep(0.01)
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

def start_game():
    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for radius in range(math.ceil(math.dist((0, 0), ((WIDTH // 2, HEIGHT // 2)))), 0, -2):
        draw_board(board, revealed, flagged)
        pygame.draw.circle(screen, BLACK, (WIDTH // 2, HEIGHT // 2), radius)
        pygame.display.flip()
    return revealed, flagged, board

def show_leaderboard():
    pass

# Function to draw the main menu
def draw_menu():
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

    screen.blit(title_text, title_rect)
    screen.blit(play_text, play_rect)
    screen.blit(leaderboard_text, leaderboard_rect)

    return play_rect.inflate(250, 100), play_rect.move(0, 250).inflate(250, 100)

def draw_difficulty():
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

# Main game loop
def main():
    clock = pygame.time.Clock()
    game_over = True
    main_menu = True
    difficulty_select = False
    results = False
    setup = False

    # Globals
    global COLS, ROWS, CELL_SIZE, NOS_MINES

    # revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    # flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
    # board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

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
                                print("Game Over!")
                                game_over = True
                                # results = True
                                main_menu = True
                                end_game(row, col, board, revealed, flagged)
                        elif event.button == 3 and not revealed[row][col]:
                            # Right click to flag/unflag cell
                            flagged[row][col] = not flagged[row][col]
                        # Check if the game is won
                        if [cell for row in revealed for cell in row].count(False) == NOS_MINES and not game_over:
                            print("Game Won!")
                elif main_menu:
                    if play_rect.collidepoint(x, y):
                        difficulty_select = True
                        main_menu = False
                        # game_over = False
                        # revealed, flagged, board = start_game()
                    elif leaderboard_rect.collidepoint(x, y):
                        show_leaderboard()
                elif difficulty_select:
                    if easy.collidepoint(x, y):
                        COLS, ROWS = 10, 8
                        CELL_SIZE = WIDTH // COLS
                        NOS_MINES = 10
                        setup = True
                    elif medium.collidepoint(x, y):
                        COLS, ROWS = 18, 14
                        CELL_SIZE = WIDTH // COLS
                        NOS_MINES = 40
                        setup = True
                    elif hard.collidepoint(x, y):
                        COLS, ROWS = 24, 20
                        CELL_SIZE = WIDTH // COLS
                        NOS_MINES = 99
                        setup = True
                    if setup:
                        setup = False
                        game_over = False
                        difficulty_select = False
                        revealed, flagged, board = start_game()
                elif results:
                    pass
                else:
                    print("Nuar")
                

        if not game_over:
            screen.fill(BLACK)
            draw_board(board, revealed, flagged)
        elif main_menu:
            screen.fill(BLACK)
            play_rect, leaderboard_rect = draw_menu()
        elif difficulty_select:
            screen.fill(BLACK)
            easy, medium, hard = draw_difficulty()
        elif results:
            screen.fill(BLACK)
            pass
        else:
            print("NOOOO")
        
        pygame.display.flip()
        clock.tick(FRAMERATE)

# Run the game
if __name__ == "__main__":
    main()
