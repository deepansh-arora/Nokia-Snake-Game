import pygame
import random
import sys
from collections import deque

CELL_SIZE = 20            
GRID_WIDTH = 30          
GRID_HEIGHT = 20         
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS_START = 8            
FPS_INCREASE_EVERY = 5   
FPS_INCREASE_BY = 1      


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (200, 0, 0)
GRAY = (40, 40, 40)


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def draw_cell(surface, pos, color):
    x, y = pos
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect)


def random_empty_cell(snake_set):
   
    while True:
        x = random.randrange(0, GRID_WIDTH)
        y = random.randrange(0, GRID_HEIGHT)
        if (x, y) not in snake_set:
            return (x, y)

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Nokia Snake')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('dejavusans', 18)

        self.reset()

    def reset(self):
        
        mid_x = GRID_WIDTH // 2
        mid_y = GRID_HEIGHT // 2
        self.snake = deque()
        self.snake.append((mid_x - 1, mid_y))
        self.snake.append((mid_x, mid_y))
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.snake_set = set(self.snake)

        self.apple = random_empty_cell(self.snake_set)
        self.score = 0
        self.fps = FPS_START
        self.game_over = False
        self.paused = False

    def handle_key(self, key):
        
        if key == pygame.K_UP or key == pygame.K_w:
            if self.direction != DOWN:
                self.next_direction = UP
        elif key == pygame.K_DOWN or key == pygame.K_s:
            if self.direction != UP:
                self.next_direction = DOWN
        elif key == pygame.K_LEFT or key == pygame.K_a:
            if self.direction != RIGHT:
                self.next_direction = LEFT
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            if self.direction != LEFT:
                self.next_direction = RIGHT
        elif key == pygame.K_SPACE:
            
            self.paused = not self.paused
        elif key == pygame.K_r:
            
            if self.game_over:
                self.reset()

    def update(self):
        if self.game_over or self.paused:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[-1]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        new_head = (new_head[0] % GRID_WIDTH, new_head[1] % GRID_HEIGHT)

        if new_head in self.snake_set:
            self.game_over = True
            return
        self.snake.append(new_head)
        self.snake_set.add(new_head)

        if new_head == self.apple:
            # Eat apple: increase score, place new apple, increase speed occasionally
            self.score += 1
            # Speed up each time score is a multiple of FPS_INCREASE_EVERY
            if self.score % FPS_INCREASE_EVERY == 0:
                self.fps += FPS_INCREASE_BY
            # Place new apple in empty cell
            self.apple = random_empty_cell(self.snake_set)
        else:
            # Remove tail
            tail = self.snake.popleft()
            self.snake_set.remove(tail)

    def draw_grid(self):
        for x in range(GRID_WIDTH):
            pygame.draw.line(self.screen, GRAY, (x * CELL_SIZE, 0), (x * CELL_SIZE, WINDOW_HEIGHT))
        for y in range(GRID_HEIGHT):
            pygame.draw.line(self.screen, GRAY, (0, y * CELL_SIZE), (WINDOW_WIDTH, y * CELL_SIZE))

    def draw(self):
        self.screen.fill(BLACK)

        draw_cell(self.screen, self.apple, RED)

        for i, cell in enumerate(self.snake):
            if i == len(self.snake) - 1:
                draw_cell(self.screen, cell, GREEN)
            else:
                draw_cell(self.screen, cell, DARK_GREEN)

        score_surf = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_surf, (6, 6))
        
        if self.game_over:
            over_surf = self.font.render('GAME OVER - Press R to restart', True, WHITE)
            rect = over_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(over_surf, rect)

        if self.paused and not self.game_over:
            pause_surf = self.font.render('PAUSED - Press Space to resume', True, WHITE)
            rect = pause_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(pause_surf, rect)

        pygame.display.flip()

    def run(self):
        # Main loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)

            if not self.game_over and not self.paused:
                self.update()

            self.draw()
            # Control speed using current fps
            self.clock.tick(self.fps)

if __name__ == '__main__':
    game = SnakeGame()
    try:
        game.run()
    except SystemExit:
        pass

