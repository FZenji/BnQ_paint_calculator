import pygame
import sys
import random

# Define constants
WIDTH = 800
COLS, ROWS = 10, 8
CELL_SIZE = WIDTH // COLS
HEIGHT = CELL_SIZE * ROWS
NOS_MINES = 10
BOARDER = 10

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
RED = (224, 22, 46)
DARK_BLUE = (56, 22, 224)
AQUA = (29, 171, 140)

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

# Function to initialize the game board
def initialize_board():
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    # Randomly place mines on the board
    for _ in range(NOS_MINES):
        row, col = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
        while board[row][col] == -1:
            row, col = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
        board[row][col] = -1
        # Increment the surrounding cells
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if 0 <= i < ROWS and 0 <= j < COLS and board[i][j] != -1:
                    board[i][j] += 1
    return board

# Function to draw the game board
def draw_board(board, revealed, flagged):
    for row in range(ROWS):
        for col in range(COLS):
            cell_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if revealed[row][col]:
                pygame.draw.rect(screen, WHITE, cell_rect)
                if board[row][col] > 0:
                    font = pygame.font.Font(None, 36)
                    number = str(board[row][col])
                    match number:
                        case '2':
                            font_colour = GREEN
                        case '3':
                            font_colour = PURPLE
                        case '4':
                            font_colour = YELLOW
                        case '5':
                            font_colour = ORANGE
                        case '5':
                            font_colour = RED
                        case '5':
                            font_colour = DARK_BLUE
                        case '5':
                            font_colour = AQUA
                        case _:
                            font_colour = BLUE
                    text = font.render(number, True, font_colour)
                    text_rect = text.get_rect(center=cell_rect.center)
                    screen.blit(text, text_rect)
                elif board[row][col] == -1:
                    pygame.draw.circle(screen, BLACK, cell_rect.center, CELL_SIZE // 2 - BOARDER)
            elif flagged[row][col]:
                colour = GRAY if (row + col) % 2 == 0 else DARK_GRAY
                pygame.draw.rect(screen, colour, cell_rect)
                pygame.draw.polygon(screen, RED, [(col * CELL_SIZE + CELL_SIZE // 3 - 2, (row + 1) * CELL_SIZE - BOARDER), 
                                                  (col * CELL_SIZE + CELL_SIZE // 3 - 2, row * CELL_SIZE + BOARDER), 
                                                  (col * CELL_SIZE + CELL_SIZE // 3 + 2, row * CELL_SIZE + BOARDER),
                                                  (col * CELL_SIZE + CELL_SIZE - BOARDER, row * CELL_SIZE + CELL_SIZE // 3),
                                                  (col * CELL_SIZE + CELL_SIZE // 3 + 2, row * CELL_SIZE + 2 * (CELL_SIZE // 3)),
                                                  (col * CELL_SIZE + CELL_SIZE // 3 + 2, (row + 1) * CELL_SIZE - 5)])

            else:
                colour = GRAY if (row + col) % 2 == 0 else DARK_GRAY
                pygame.draw.rect(screen, colour, cell_rect)
                # if revealed[row][col]:
                #     pygame.draw.rect(screen, WHITE, cell_rect)

# Function to draw the replay button
def draw_replay_button():
    font = pygame.font.Font(None, 50)
    replay_text = font.render("Replay", True, WHITE)
    replay_rect = replay_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    pygame.draw.rect(screen, BLACK, replay_rect)
    screen.blit(replay_text, replay_rect)

# Main game loop
def main():
    clock = pygame.time.Clock()
    game_over = False
    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
    board = initialize_board()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if 0 <= row < ROWS and 0 <= col < COLS:
                    if event.button == 1 and not revealed[row][col]:
                        # Left click to reveal cell
                        revealed[row][col] = True
                        flagged[row][col] = False
                        if board[row][col] == -1:
                            print("Game Over!")
                            game_over = True
                    elif event.button == 3 and not revealed[row][col]:
                        # Right click to flag/unflag cell
                        flagged[row][col] = not flagged[row][col]

        if not game_over:
            screen.fill(BLACK)
            # draw_checkerboard()
            draw_board(board, revealed, flagged)
        else:
            # screen.fill(BLACK)
            # show_mines()
            draw_replay_button()
        
        pygame.display.flip()
        clock.tick(30)

# Run the game
if __name__ == "__main__":
    main()
