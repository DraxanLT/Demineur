import pygame
import sys
import csv
from grid import Grid
from random import sample
import time

def start_game(w, h, mines, difficulty_name):
    grid = Grid((w, h, mines))

    # Grid and window dimensions
    GridSize = 60
    CellCount = w
    WIDTH = w * GridSize + 200  # Ajout pour marges
    HEIGHT = h * GridSize + 200

    # Position to center the grid
    GRID_OFFSET_X = (WIDTH - w * GridSize) // 2
    GRID_OFFSET_Y = (HEIGHT - h * GridSize) // 2

    # Color
    WHITE = (255, 255, 255)
    GRAY = (192, 192, 192)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    LIGHT_BLUE = (136, 162, 193)

    # Dies for flags and clicked boxes
    flags = [[0] * CellCount for _ in range(CellCount)]
    clicked_cells = [[0] * CellCount for _ in range(CellCount)]

    # Pygame initialization
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Démineur")
    clock = pygame.time.Clock()

    # Fonts
    font = pygame.font.Font("font/Super Sense.ttf", 20)

    # Variables
    user_text = ""
    input_rect = pygame.Rect((WIDTH // 2) - 250, HEIGHT - 500, 500, 32)
    color_active = pygame.Color('lightskyblue3')

    valider_rect = pygame.Rect((WIDTH // 2) - 180, HEIGHT - 400, 200, 32)
    final_score = None
    now = time.time()



    # Game Status
    game_screen = True
    running = True

    # Load images
    image_flag = pygame.image.load("image/redflag.png").convert_alpha()
    image_flag = pygame.transform.scale(image_flag, (GridSize, GridSize))
    image_bomb = pygame.image.load("image/bombFR.png").convert_alpha()
    image_bomb = pygame.transform.scale(image_bomb, (GridSize, GridSize))
    title_image = pygame.image.load("image/title.png").convert_alpha()
    title_resized = pygame.transform.scale(title_image, (600, 100))
    background_image = pygame.image.load("image/Sans_titre_275_20241219155549.png").convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # Mining-related variables
    is_first_click = True  # Indicates if this is the first click
    mines_positions = grid.indice_mine()  # Load initial mine positions

    def draw_grid():
        # Draw the grid centered on the screen
        for x in range(CellCount):
            for y in range(CellCount):
                rect_x = GRID_OFFSET_X + x * GridSize
                rect_y = GRID_OFFSET_Y + y * GridSize
                rect = pygame.Rect(rect_x, rect_y, GridSize, GridSize)
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, BLACK, rect, 2)

    def reveal_cells(row, col):
        # Recursively reveal adjacent cells
        if row < 0 or row >= CellCount or col < 0 or col >= CellCount:
            return
        if clicked_cells[row][col] == 1 or (row, col) in mines_positions:
            return

        clicked_cells[row][col] = 1

        if grid.grid[row][col] > 0:
            return

        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            reveal_cells(row + dr, col + dc)

    def check_victory():
        # Check if all unmined squares have been revealed
        for row in range(CellCount):
            for col in range(CellCount):
                if (row, col) in mines_positions:
                    continue
                if clicked_cells[row][col] != 1:
                    return False
        return True

    def score():
        elapsed_time = time.time() - now  # Elapsed time in seconds
        return int(elapsed_time)


    def first_case(row, col, mines_positions):
        # function to generate a new grid with the new coordinates of mines
        if (row, col) in mines_positions:
            print(f"First click on the cell ({row}, {col}) contained a mine. Repositioning mines.")
            anciennes_mines = mines_positions.copy()
            mines_positions = sample(
                [(i, j) for i in range(CellCount) for j in range(CellCount) if (i, j) != (row, col)],len(mines_positions))  # Shuffle and select the same number of mines
            print(f"Old mines: {anciennes_mines}")
            print(f"New mines: {mines_positions}")
            grid.grid = grid.rebuild_grid(mines_positions)  # Rebuild the grid with the new mines
        return mines_positions




    while running:
        if game_screen:
            # Draw the background image
            screen.blit(background_image, (0, 0))
            screen.blit(font.render(f" score : {score()}", True, (255, 0, 0)), (10, 10))


            # Draw the title
            screen.blit(title_resized, ((WIDTH - 600) // 2, 0))

            # Draw the grid
            draw_grid()

            # Draw the contents of the boxes
            for row in range(CellCount):
                for col in range(CellCount):
                    x, y = GRID_OFFSET_X + col * GridSize, GRID_OFFSET_Y + row * GridSize

                    if flags[row][col]:
                        screen.blit(image_flag, (x, y))
                    elif clicked_cells[row][col]:
                        value = grid.grid[row][col]
                        if value == -1:
                            screen.blit(image_bomb, (x, y))
                        elif value > 0:
                            pygame.draw.rect(screen, BLUE, pygame.Rect(x, y, GridSize, GridSize))
                            pygame.draw.rect(screen, BLACK, pygame.Rect(x, y, GridSize, GridSize), 2)
                            text = font.render(str(value), True, WHITE)
                            screen.blit(text, (x + GridSize // 3, y + GridSize // 4))
                        else:
                            pygame.draw.rect(screen, BLUE, pygame.Rect(x, y, GridSize, GridSize))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    col = (mouse_x - GRID_OFFSET_X) // GridSize
                    row = (mouse_y - GRID_OFFSET_Y) // GridSize

                    if 0 <= row < CellCount and 0 <= col < CellCount:
                        if event.button == 3:  # Right click
                            flags[row][col] = 1 - flags[row][col]
                        elif event.button == 1:  # Left click
                            if is_first_click:
                                mines_positions = first_case(row, col, mines_positions)
                                is_first_click = False
                            if (row, col) in mines_positions:
                                print("Game Over")
                                for r, c in mines_positions:
                                    bomb_x = GRID_OFFSET_X + c * GridSize
                                    bomb_y = GRID_OFFSET_Y + r * GridSize
                                    screen.blit(image_bomb, (bomb_x, bomb_y))
                                pygame.display.flip()
                                running = False
                            else:
                                reveal_cells(row, col)

            if check_victory():
                print("Victory!")
                game_screen = False
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                if final_score is None:  # Check if the final score has not already been set
                    final_score = score()  # Set the final score

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if valider_rect.collidepoint(event.pos):
                        with open('stats.csv', mode='a', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            if user_text == "":
                                writer.writerow(["Anonyme", score(), difficulty_name, grid.grid])
                            else:
                                writer.writerow([user_text, score(), difficulty_name, grid.grid])
                        running = False

            screen.fill(LIGHT_BLUE)
            screen.blit(title_resized, ((WIDTH - 600) // 2, 20))
            score_text = font.render(f"VICTOIRE score : {final_score}, {difficulty_name}, {user_text}", True, (255, 0, 0))
            screen.blit(score_text, (WIDTH // 2 - 300, HEIGHT - 550))
            pygame.draw.rect(screen, color_active, input_rect, 2)
            text_surface = font.render(user_text, True, BLACK)
            screen.blit(text_surface, input_rect)
            pygame.draw.rect(screen, pygame.Color('red'), valider_rect)
            text = font.render("Valider", True, BLACK)
            screen.blit(text, (valider_rect.x + 50, valider_rect.y + 5))  # Center the text in the button

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
