import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

class GameState(Enum):
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

BLOCK_SIZE = 20
SPEED = 10

class GameLogic:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, Point(self.head.x-BLOCK_SIZE, self.head.y), Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
        self.state = GameState.PLAYING

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        game_over = False
        if self.state == GameState.PLAYING:
            self._move(self.direction)
            self.snake.insert(0, self.head)

            game_over = False
            if self._is_collision():
                self.state = GameState.GAME_OVER
                game_over = True

            if self.head == self.food:
                self.score += 1
                self._place_food()
            else:
                self.snake.pop()

        return game_over, self.score

    def _is_collision(self):
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        if self.head in self.snake[1:]:
            return True
        return False

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        self.head = Point(x, y)

class GameUI:
    def __init__(self, game_logic, w=640, h=480):
        self.game_logic = game_logic
        self.w = w
        self.h = h
        pygame.init()
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('arial.ttf', 25)

    def draw(self):
        self.display.fill((0,0,0))

        for pt in self.game_logic.snake:
            pygame.draw.rect(self.display, (0,255,0), pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, (255,255,255), pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, (255,0,0), pygame.Rect(self.game_logic.food.x, self.game_logic.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = self.font.render("Score: " + str(self.game_logic.score), True, (255,255,255))
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def get_user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.game_logic.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.game_logic.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.game_logic.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.game_logic.direction = Direction.DOWN
                elif event.key == pygame.K_p:
                    self.game_logic.state = GameState.PAUSED
                elif event.key == pygame.K_r:
                    self.game_logic.state = GameState.PLAYING
                elif event.key == pygame.K_n and self.game_logic.state == GameState.GAME_OVER:
                    self.game_logic = GameLogic()

    def main_loop(self):
        while True:
            self.get_user_input()
            game_over, score = self.game_logic.play_step()
            self.draw()
            self.clock.tick(SPEED)
            if game_over:
                print('Final Score', score)
                pygame.quit()
                quit()
        pygame.quit()

if __name__ == '__main__':
    game_logic = GameLogic()
    game_ui = GameUI(game_logic)
    game_ui.main_loop()
