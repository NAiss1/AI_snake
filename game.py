
import random
import pygame
from typing import List, Tuple
import numpy as np

from constants import (
    WIDTH, HEIGHT, CELL_SIZE,
    UP, DOWN, LEFT, RIGHT, DIRECTIONS,
    WHITE, GREEN, RED, BLACK, GRAY,
)

Position = Tuple[int, int]

class SnakeGame:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 22)
        self.reset()

    def reset(self):
        self.snake: List[Position] = [(5, 5)]
        self.direction = RIGHT
        self.walls   = self._generate_walls()
        self._spawn_food()
        self.score = 0
        self.frame_count = 0
        return self._get_state()

    def _generate_walls(self) -> List[Position]:
        walls: set[Position] = set()
        for _ in range(random.randint(3, 5)):
            x = random.randint(4, (WIDTH // CELL_SIZE) - 4)
            seg_len = random.randint(4, 8)
            y_start = random.randint(2, (HEIGHT // CELL_SIZE) - seg_len - 2)
            for dy in range(seg_len):
                walls.add((x, y_start + dy))
        return list(walls)

    def _spawn_food(self) -> None:
        while True:
            self.food = (
                random.randint(0, WIDTH // CELL_SIZE - 1),
                random.randint(0, HEIGHT // CELL_SIZE - 1),
            )
            if self.food not in self.snake and self.food not in self.walls:
                break

    def step(self, action: int):
        self.frame_count += 1
        if action == UP and self.direction != DOWN:
            self.direction = UP
        elif action == DOWN and self.direction != UP:
            self.direction = DOWN
        elif action == LEFT and self.direction != RIGHT:
            self.direction = LEFT
        elif action == RIGHT and self.direction != LEFT:
            self.direction = RIGHT

        x, y = self.snake[0]
        if self.direction == UP:
            y -= 1
        elif self.direction == DOWN:
            y += 1
        elif self.direction == LEFT:
            x -= 1
        else:
            x += 1
        x %= WIDTH // CELL_SIZE
        y %= HEIGHT // CELL_SIZE
        new_head: Position = (x, y)

        if new_head in self.snake or new_head in self.walls:
            return self._get_state(), -10, True  

        self.snake.insert(0, new_head)
        reward = 0
        if new_head == self.food:
            self.score += 1
            reward = 10
            self._spawn_food()
        else:
            self.snake.pop()
        return self._get_state(), reward, False

    def _get_state(self):
        head = self.snake[0]
        point_l = ((head[0] - 1) % (WIDTH // CELL_SIZE), head[1])
        point_r = ((head[0] + 1) % (WIDTH // CELL_SIZE), head[1])
        point_u = (head[0], (head[1] - 1) % (HEIGHT // CELL_SIZE))
        point_d = (head[0], (head[1] + 1) % (HEIGHT // CELL_SIZE))
        danger = [
            point_u in self.snake or point_u in self.walls,
            point_d in self.snake or point_d in self.walls,
            point_l in self.snake or point_l in self.walls,
            point_r in self.snake or point_r in self.walls,
        ]
        food_dir = [
            self.food[1] < head[1],
            self.food[1] > head[1],
            self.food[0] < head[0],
            self.food[0] > head[0],
        ]
        return tuple(danger + food_dir)

    def render(self, screen) -> None:
        screen.fill(BLACK)
        for wx, wy in self.walls:
            pygame.draw.rect(screen, GRAY, (wx * CELL_SIZE, wy * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for sx, sy in self.snake:
            pygame.draw.rect(screen, GREEN, (sx * CELL_SIZE, sy * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        fx, fy = self.food
        pygame.draw.rect(screen, RED, (fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        screen.blit(self.font.render(f"Score: {self.score}", True, WHITE), (10, 10))
        pygame.display.flip()
