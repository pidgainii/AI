#!/usr/bin/env python3
from typing import List, Set
from dataclasses import dataclass
import pygame
from enum import Enum, unique
import sys
import random
from collections import deque
from math import sqrt

ALGORITHM = ""

FPS = 8

INIT_LENGTH = 4

WIDTH = 480
HEIGHT = 480
GRID_SIDE = 24
GRID_WIDTH = WIDTH // GRID_SIDE
GRID_HEIGHT = HEIGHT // GRID_SIDE

BRIGHT_BG = (173, 216, 230)
DARK_BG = (183, 226, 240)


SNAKE_COL = (6, 38, 7)
FOOD_COL = (224, 160, 38)
OBSTACLE_COL = (209, 59, 59)
VISITED_COL = (135, 175, 205)


@unique
class Direction(tuple, Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def reverse(self):
        x, y = self.value
        return Direction((x * -1, y * -1))


@dataclass
class Position:
    x: int
    y: int

    def check_bounds(self, width: int, height: int):
        return (self.x >= width) or (self.x < 0) or (self.y >= height) or (self.y < 0)

    def draw_node(self, surface: pygame.Surface, color: tuple, background: tuple):
        r = pygame.Rect(
            (int(self.x * GRID_SIDE), int(self.y * GRID_SIDE)), (GRID_SIDE, GRID_SIDE)
        )
        pygame.draw.rect(surface, color, r)
        pygame.draw.rect(surface, background, r, 1)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Position):
            return (self.x == o.x) and (self.y == o.y)
        else:
            return False

    def __str__(self):
        return f"X{self.x};Y{self.y};"

    def __hash__(self):
        return hash(str(self))


class GameNode:
    nodes: Set[Position] = set()

    def __init__(self):
        self.position = Position(0, 0)
        self.color = (0, 0, 0)

    def randomize_position(self):
        try:
            GameNode.nodes.remove(self.position)
        except KeyError:
            pass

        condidate_position = Position(
            random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1),
        )

        if condidate_position not in GameNode.nodes:
            self.position = condidate_position
            GameNode.nodes.add(self.position)
        else:
            self.randomize_position()

    def draw(self, surface: pygame.Surface):
        self.position.draw_node(surface, self.color, BRIGHT_BG)


class Food(GameNode):
    def __init__(self):
        super(Food, self).__init__()
        self.color = FOOD_COL
        self.randomize_position()


class Obstacle(GameNode):
    def __init__(self):
        super(Obstacle, self).__init__()
        self.color = OBSTACLE_COL
        self.randomize_position()


class Snake:
    def __init__(self, screen_width, screen_height, init_length):
        self.color = SNAKE_COL
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.init_length = init_length
        self.reset()

    def reset(self):
        self.length = self.init_length
        self.positions = [Position((GRID_SIDE // 2), (GRID_SIDE // 2))]
        self.direction = random.choice([e for e in Direction])
        self.score = 0
        self.hasReset = True

    def get_head_position(self) -> Position:
        return self.positions[0]

    def turn(self, direction: Direction):
        if self.length > 1 and direction.reverse() == self.direction:
            return
        else:
            self.direction = direction

    def move(self):
        self.hasReset = False
        cur = self.get_head_position()
        x, y = self.direction.value
        new = Position(cur.x + x, cur.y + y,)
        if self.collide(new):
            self.reset()
        else:
            self.positions.insert(0, new)
            while len(self.positions) > self.length:
                self.positions.pop()

    def collide(self, new: Position):
        return (new in self.positions) or (new.check_bounds(GRID_WIDTH, GRID_HEIGHT))

    def eat(self, food: Food):
        if self.get_head_position() == food.position:
            self.length += 1
            self.score += 1
            while food.position in self.positions:
                food.randomize_position()

    def hit_obstacle(self, obstacle: Obstacle):
        if self.get_head_position() == obstacle.position:
            self.length -= 1
            self.score -= 1
            if self.length == 0:
                self.reset()

    def draw(self, surface: pygame.Surface):
        for p in self.positions:
            p.draw_node(surface, self.color, BRIGHT_BG)


class Player:
    def __init__(self) -> None:
        self.visited_color = VISITED_COL
        self.visited: Set[Position] = set()
        self.chosen_path: List[Direction] = []

    def move(self, snake: Snake) -> bool:
        try:
            next_step = self.chosen_path.pop(0)
            snake.turn(next_step)
            return False
        except IndexError:
            return True

    def search_path(self, snake: Snake, food: Food, *obstacles: Set[Obstacle]):
        """
        Do nothing, control is defined in derived classes
        """
        pass

    def turn(self, direction: Direction):
        """
        Do nothing, control is defined in derived classes
        """
        pass

    def draw_visited(self, surface: pygame.Surface):
        for p in self.visited:
            p.draw_node(surface, self.visited_color, BRIGHT_BG)


class SnakeGame:
    def __init__(self, snake: Snake, player: Player) -> None:
        pygame.init()
        pygame.display.set_caption("AIFundamentals - SnakeGame")

        self.snake = snake
        self.food = Food()
        self.obstacles: Set[Obstacle] = set()
        for _ in range(20):
            ob = Obstacle()
            while any([ob.position == o.position for o in self.obstacles]):
                ob.randomize_position()
            self.obstacles.add(ob)

        self.player = player

        self.fps_clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(
            (snake.screen_height, snake.screen_width), 0, 32
        )
        self.surface = pygame.Surface(self.screen.get_size()).convert()
        self.myfont = pygame.font.SysFont("monospace", 16)

    def drawGrid(self):
        for y in range(0, int(GRID_HEIGHT)):
            for x in range(0, int(GRID_WIDTH)):
                p = Position(x, y)
                if (x + y) % 2 == 0:
                    p.draw_node(self.surface, BRIGHT_BG, BRIGHT_BG)
                else:
                    p.draw_node(self.surface, DARK_BG, DARK_BG)

    def run(self):
        while not self.handle_events():
            self.fps_clock.tick(FPS)
            self.drawGrid()
            if self.player.move(self.snake) or self.snake.hasReset:
                self.player.search_path(self.snake, self.food, self.obstacles)
                self.player.move(self.snake)
            self.snake.move()
            self.snake.eat(self.food)
            for ob in self.obstacles:
                self.snake.hit_obstacle(ob)
            for ob in self.obstacles:
                ob.draw(self.surface)
            self.player.draw_visited(self.surface)
            self.snake.draw(self.surface)
            self.food.draw(self.surface)
            self.screen.blit(self.surface, (0, 0))
            text = self.myfont.render(
                "Score {0}".format(self.snake.score), 1, (0, 0, 0)
            )
            self.screen.blit(text, (5, 10))
            pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP:
                    self.player.turn(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    self.player.turn(Direction.DOWN)
                elif event.key == pygame.K_LEFT:
                    self.player.turn(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.player.turn(Direction.RIGHT)
        return False


class HumanPlayer(Player):
    def __init__(self):
        super(HumanPlayer, self).__init__()

    def turn(self, direction: Direction):
        self.chosen_path.append(direction)


# ----------------------------------
# DO NOT MODIFY CODE ABOVE THIS LINE
# ----------------------------------


class SearchBasedPlayer(Player):
    ALGORITHM = "Dijkstra"  # This can be set to "BFS", "DFS", "Dijkstra", or "A*"

    def __init__(self):
        super().__init__()
        self.visited: Set[Position] = set()  # Set to track visited nodes
        self.obstacles: Set[Position] = set()  # Set to track obstacle positions

    def search_path(self, snake: Snake, food: Food, obstacles: Set[Obstacle]):
        
        
        self.visited.clear()  # Clear any previous visited positions
        self.obstacles = {obstacle.position for obstacle in obstacles}  # Update obstacles

        
        for segment in snake.positions[1:]:
            self.obstacles.add(segment)

        
        if self.ALGORITHM == "BFS":
            return self.bfs_search(snake, food, obstacles)
        elif self.ALGORITHM == "DFS":
            return self.dfs_search(snake, food, obstacles)
        elif self.ALGORITHM == "Dijkstra":
            return self.dijkstra_search(snake, food, obstacles)
        elif self.ALGORITHM == "A*":
            return self.a_star_search(snake, food, obstacles)
        else:
            raise ValueError(f"Unknown algorithm: {self.ALGORITHM}")

    # BFS Algorithm
    def bfs_search(self, snake: Snake, food: Food, obstacles: Set[Obstacle]):
        
        backtrack = [[None for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
        queue = deque()
        head = snake.get_head_position()
        queue.append((head, None, 0))  # (current position, parent position, cost)
        
        found = False
        while queue and not found:
            current, previous, cost = queue.popleft()
            x, y = current.x, current.y

            if current in self.visited or current in self.obstacles:
                continue

            self.visited.add(current)
            backtrack[x][y] = (previous, cost)

            if current == food.position:
                found = True
                break

            for direction in Direction:
                dx, dy = direction.value
                neighbor = Position(x + dx, y + dy)

                if (
                    0 <= neighbor.x < GRID_WIDTH
                    and 0 <= neighbor.y < GRID_HEIGHT
                    and neighbor not in self.visited
                    and neighbor not in self.obstacles
                ):
                    queue.append((neighbor, current, cost + 1))

        path = []
        if found:
            current = food.position
            while current != head:
                previous, _ = backtrack[current.x][current.y]
                dx = current.x - previous.x
                dy = current.y - previous.y
                path.append(Direction((dx, dy)))
                current = previous

            path.reverse()

        self.chosen_path = path

    # DFS Algorithm
    def dfs_search(self, snake: Snake, food: Food, obstacles: Set[Obstacle]):
        shortest_path = None
        stack = [(snake.get_head_position(), [], 0)]
        while stack:
            current, path, cost = stack.pop()

            if shortest_path and len(path) >= len(shortest_path):
                continue

            if current in self.visited or current in self.obstacles:
                continue

            self.visited.add(current)
            path = path + [current]

            if current == food.position:
                if not shortest_path or len(path) < len(shortest_path):
                    shortest_path = path
                continue

            for direction in Direction:
                dx, dy = direction.value
                neighbor = Position(current.x + dx, current.y + dy)

                if (
                    0 <= neighbor.x < GRID_WIDTH
                    and 0 <= neighbor.y < GRID_HEIGHT
                    and neighbor not in self.visited
                    and neighbor not in self.obstacles
                ):
                    stack.append((neighbor, path, cost + 1))

        self.chosen_path = []
        if shortest_path:
            for i in range(len(shortest_path) - 1):
                dx = shortest_path[i + 1].x - shortest_path[i].x
                dy = shortest_path[i + 1].y - shortest_path[i].y
                self.chosen_path.append(Direction((dx, dy)))

    # Dijkstra Algorithm
    def dijkstra_search(self, snake: Snake, food: Food, obstacles: Set[Obstacle]):
        distances = {Position(x, y): float('inf') for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)}
        head = snake.get_head_position()
        distances[head] = 0

        priority_queue = [(0, head)]
        backtrack = {}

        while priority_queue:
            priority_queue.sort(key=lambda x: x[0])
            current_distance, current_position = priority_queue.pop(0)

            if current_position in self.visited:
                continue

            self.visited.add(current_position)

            if current_position == food.position:
                break

            for direction in Direction:
                dx, dy = direction.value
                neighbor = Position(current_position.x + dx, current_position.y + dy)

                if (
                    0 <= neighbor.x < GRID_WIDTH
                    and 0 <= neighbor.y < GRID_HEIGHT
                    and neighbor not in self.visited
                    and neighbor not in self.obstacles
                ):
                    new_distance = current_distance + 1

                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        backtrack[neighbor] = current_position
                        priority_queue.append((new_distance, neighbor))

        path = []
        if food.position in backtrack:
            current = food.position
            while current != head:
                previous = backtrack[current]
                dx = current.x - previous.x
                dy = current.y - previous.y
                path.append(Direction((dx, dy)))
                current = previous

            path.reverse()

        self.chosen_path = path

    # A* Algorithm
    def a_star_search(self, snake: Snake, food: Food, obstacles: Set[Obstacle]):
        open_set = [(0, snake.get_head_position())]
        g_score = {Position(x, y): float('inf') for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)}
        g_score[snake.get_head_position()] = 0
        f_score = {Position(x, y): float('inf') for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)}
        f_score[snake.get_head_position()] = self.heuristic(snake.get_head_position(), food.position)

        came_from = {}

        while open_set:
            current = min(open_set, key=lambda x: x[0])[1] # we choose the one with lowest f score
            open_set = [node for node in open_set if node[1] != current]

            if current == food.position:
                self.chosen_path = self.reconstruct_path(came_from, current)
                return

            self.visited.add(current)

            for direction in Direction:
                dx, dy = direction.value
                neighbor = Position(current.x + dx, current.y + dy)

                if (
                    0 <= neighbor.x < GRID_WIDTH
                    and 0 <= neighbor.y < GRID_HEIGHT
                    and neighbor not in self.visited
                    and neighbor not in self.obstacles
                ):
                    tentative_g_score = g_score[current] + 1

                    if tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, food.position)

                        if neighbor not in [node[1] for node in open_set]:
                            open_set.append((f_score[neighbor], neighbor))

        self.chosen_path = []

    def heuristic(self, position: Position, goal: Position) -> float:
        return sqrt((position.x - goal.x) ** 2 + (position.y - goal.y) ** 2)

    def reconstruct_path(self, came_from: dict, current: Position):
        path = []
        while current in came_from:
            previous = came_from[current]
            dx = current.x - previous.x
            dy = current.y - previous.y
            path.append(Direction((dx, dy)))
            current = previous
        path.reverse()
        return path



if __name__ == "__main__":
    snake = Snake(WIDTH, WIDTH, INIT_LENGTH)
    player = HumanPlayer()
    player = SearchBasedPlayer()
    game = SnakeGame(snake, player)
    game.run()