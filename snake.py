import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class Colors:
    WHITE = (255, 255, 255)
    RED = (200, 0, 0)
    BLUE1 = (0, 0, 255)
    BLUE2 = (0, 100, 255)
    BLACK = (0, 0, 0)

class GameConstants:
    BLOCK_SIZE = 20
    SPEED = 20

Point = namedtuple('Point', 'x, y')

class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.init_display()
        self.init_game_state()

    def init_display(self):
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

    def init_game_state(self):
        self.direction = Direction.RIGHT
        self.init_snake()
        self.score = 0
        self.food = None
        self.place_food()

    def init_snake(self):
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - GameConstants.BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * GameConstants.BLOCK_SIZE), self.head.y)]

    def place_food(self):
        x = random.randint(0, (self.w - GameConstants.BLOCK_SIZE) // GameConstants.BLOCK_SIZE) * GameConstants.BLOCK_SIZE
        y = random.randint(0, (self.h - GameConstants.BLOCK_SIZE) // GameConstants.BLOCK_SIZE) * GameConstants.BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self.place_food()

    def is_collision(self):
        return self.head_in_boundary() or self.head_in_snake()

    def head_in_boundary(self):
        return (self.head.x > self.w - GameConstants.BLOCK_SIZE or
                self.head.x < 0 or
                self.head.y > self.h - GameConstants.BLOCK_SIZE or
                self.head.y < 0)

    def head_in_snake(self):
        return self.head in self.snake[1:]

    def move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += GameConstants.BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= GameConstants.BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += GameConstants.BLOCK_SIZE
        elif direction == Direction.UP:
            y -= GameConstants.BLOCK_SIZE
        self.head = Point(x, y)

    def update_ui(self):
        self.display.fill(Colors.BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, Colors.BLUE1, pygame.Rect(pt.x, pt.y, GameConstants.BLOCK_SIZE, GameConstants.BLOCK_SIZE))
            pygame.draw.rect(self.display, Colors.BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, Colors.RED, pygame.Rect(self.food.x, self.food.y, GameConstants.BLOCK_SIZE, GameConstants.BLOCK_SIZE))

        score_text = font.render(f"Score: {self.score}", True, Colors.WHITE)
        self.display.blit(score_text, [0, 0])
        pygame.display.flip()

    def play_step(self):
        self.handle_events()

        self.move(self.direction)
        self.snake.insert(0, self.head)

        game_over = False
        if self.is_collision():
            game_over = True
            return game_over, self.score

        self.update_score_or_pop()

        self.update_ui()
        self.clock.tick(GameConstants.SPEED)

        return game_over, self.score

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            self.handle_key_events(event)

    def handle_key_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.direction = Direction.LEFT
            elif event.key == pygame.K_RIGHT:
                self.direction = Direction.RIGHT
            elif event.key == pygame.K_UP:
                self.direction = Direction.UP
            elif event.key == pygame.K_DOWN:
                self.direction = Direction.DOWN

    def update_score_or_pop(self):
        if self.head == self.food:
            self.score += 1
            self.place_food()
        else:
            self.snake.pop()

def run_game():
    game = SnakeGame()

    while True:
        game_over, score = game.play_step()

        if game_over:
            break

    print('Final Score', score)

    pygame.quit()

if __name__ == '__main__':
    run_game()
