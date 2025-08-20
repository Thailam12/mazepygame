import pygame
import random

# Cài đặt
CELL_SIZE = 20
MAZE_SIZE = 15
WIDTH = HEIGHT = CELL_SIZE * MAZE_SIZE

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze 20x20")

clock = pygame.time.Clock()

# Mê cung: mỗi ô có 4 cạnh [top, right, bottom, left]
maze = [[[True, True, True, True] for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]
visited = [[False for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]

def generate_maze(x, y):
    visited[y][x] = True
    dirs = [(0, -1, 0), (1, 0, 1), (0, 1, 2), (-1, 0, 3)]  # (dx, dy, wall index)
    random.shuffle(dirs)
    for dx, dy, wall in dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < MAZE_SIZE and 0 <= ny < MAZE_SIZE and not visited[ny][nx]:
            # Xóa tường giữa 2 ô
            maze[y][x][wall] = False
            maze[ny][nx][(wall + 2) % 4] = False
            generate_maze(nx, ny)

generate_maze(0, 0)

# Người chơi
player_x, player_y = 0, 0

def draw_maze():
    win.fill((255, 255, 255))
    for y in range(MAZE_SIZE):
        for x in range(MAZE_SIZE):
            px, py = x * CELL_SIZE, y * CELL_SIZE
            walls = maze[y][x]
            if walls[0]: pygame.draw.line(win, (0,0,0), (px, py), (px+CELL_SIZE, py))       # top
            if walls[1]: pygame.draw.line(win, (0,0,0), (px+CELL_SIZE, py), (px+CELL_SIZE, py+CELL_SIZE)) # right
            if walls[2]: pygame.draw.line(win, (0,0,0), (px, py+CELL_SIZE), (px+CELL_SIZE, py+CELL_SIZE)) # bottom
            if walls[3]: pygame.draw.line(win, (0,0,0), (px, py), (px, py+CELL_SIZE))       # left

    # Vẽ người chơi
    pygame.draw.rect(win, (0, 0, 255), (player_x * CELL_SIZE + 4, player_y * CELL_SIZE + 4, CELL_SIZE - 8, CELL_SIZE - 8))
    # Vẽ đích
    pygame.draw.rect(win, (0, 255, 0), (MAZE_SIZE * CELL_SIZE - CELL_SIZE + 4, MAZE_SIZE * CELL_SIZE - CELL_SIZE + 4, CELL_SIZE - 8, CELL_SIZE - 8))

    pygame.display.update()

# Game loop
running = True
while running:
    clock.tick(60)
    draw_maze()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not maze[player_y][player_x][0]:
                player_y -= 1
            elif event.key == pygame.K_RIGHT and not maze[player_y][player_x][1]:
                player_x += 1
            elif event.key == pygame.K_DOWN and not maze[player_y][player_x][2]:
                player_y += 1
            elif event.key == pygame.K_LEFT and not maze[player_y][player_x][3]:
                player_x -= 1

    player_x = max(0, min(MAZE_SIZE - 1, player_x))
    player_y = max(0, min(MAZE_SIZE - 1, player_y))

    # Kiểm tra thắng
    if player_x == MAZE_SIZE - 1 and player_y == MAZE_SIZE - 1:
        print("Bạn đã thoát khỏi mê cung!")
        running = False

pygame.quit()