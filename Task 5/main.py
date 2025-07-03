#!/usr/bin/env python3
# Based on https://python101.readthedocs.io/pl/latest/pygame/pong/#
import pygame
from typing import Type
import skfuzzy as fuzz
import skfuzzy.control as fuzzcontrol
import numpy as np

FPS = 30


class Board:
    def __init__(self, width: int, height: int):
        self.surface = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption("AIFundamentals - PongGame")

    def draw(self, *args):
        background = (0, 0, 0)
        self.surface.fill(background)
        for drawable in args:
            drawable.draw_on(self.surface)

        pygame.display.update()


class Drawable:
    def __init__(self, x: int, y: int, width: int, height: int, color=(255, 255, 255)):
        self.width = width
        self.height = height
        self.color = color
        self.surface = pygame.Surface(
            [width, height], pygame.SRCALPHA, 32
        ).convert_alpha()
        self.rect = self.surface.get_rect(x=x, y=y)

    def draw_on(self, surface):
        surface.blit(self.surface, self.rect)


class Ball(Drawable):
    def __init__(
        self,
        x: int,
        y: int,
        radius: int = 20,
        color=(255, 10, 0),
        speed: int = 3,
    ):
        super(Ball, self).__init__(x, y, radius, radius, color)
        pygame.draw.ellipse(self.surface, self.color, [0, 0, self.width, self.height])
        self.x_speed = speed
        self.y_speed = speed
        self.start_speed = speed
        self.start_x = x
        self.start_y = y
        self.start_color = color
        self.last_collision = 0

    def bounce_y(self):
        self.y_speed *= -1

    def bounce_x(self):
        self.x_speed *= -1

    def bounce_y_power(self):
        self.color = (
            self.color[0],
            self.color[1] + 10 if self.color[1] < 255 else self.color[1],
            self.color[2],
        )
        pygame.draw.ellipse(self.surface, self.color, [0, 0, self.width, self.height])
        self.x_speed *= 1.1
        self.y_speed *= 1.1
        self.bounce_y()

    def reset(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.x_speed = self.start_speed
        self.y_speed = self.start_speed
        self.color = self.start_color
        self.bounce_y()

    def move(self, board: Board, *args):
        self.rect.x += round(self.x_speed)
        self.rect.y += round(self.y_speed)

        if self.rect.x < 0 or self.rect.x > (
            board.surface.get_width() - self.rect.width
        ):
            self.bounce_x()

        if self.rect.y < 0 or self.rect.y > (
            board.surface.get_height() - self.rect.height
        ):
            self.reset()

        timestamp = pygame.time.get_ticks()
        if timestamp - self.last_collision < FPS * 4:
            return

        for racket in args:
            if self.rect.colliderect(racket.rect):
                self.last_collision = pygame.time.get_ticks()
                if (self.rect.right < racket.rect.left + racket.rect.width // 4) or (
                    self.rect.left > racket.rect.right - racket.rect.width // 4
                ):
                    self.bounce_y_power()
                else:
                    self.bounce_y()


class Racket(Drawable):
    def __init__(
        self,
        x: int,
        y: int,
        width: int = 80,
        height: int = 20,
        color=(255, 255, 255),
        max_speed: int = 10,
    ):
        super(Racket, self).__init__(x, y, width, height, color)
        self.max_speed = max_speed
        self.surface.fill(color)

    def move(self, x: int, board: Board):
        delta = x - self.rect.x
        delta = self.max_speed if delta > self.max_speed else delta
        delta = -self.max_speed if delta < -self.max_speed else delta
        delta = 0 if (self.rect.x + delta) < 0 else delta
        delta = (
            0
            if (self.rect.x + self.width + delta) > board.surface.get_width()
            else delta
        )
        self.rect.x += delta


class Player:
    def __init__(self, racket: Racket, ball: Ball, board: Board) -> None:
        self.ball = ball
        self.racket = racket
        self.board = board

    def move(self, x: int):
        self.racket.move(x, self.board)

    def move_manual(self, x: int):
        """
        Do nothing, control is defined in derived classes
        """
        pass

    def act(self, x_diff: int, y_diff: int):
        """
        Do nothing, control is defined in derived classes
        """
        pass


class PongGame:
    def __init__(
        self, width: int, height: int, player1: Type[Player], player2: Type[Player]
    ):
        pygame.init()
        self.board = Board(width, height)
        self.fps_clock = pygame.time.Clock()
        self.ball = Ball(width // 2, height // 2)

        self.opponent_paddle = Racket(x=width // 2, y=0)
        self.oponent = player1(self.opponent_paddle, self.ball, self.board)

        self.player_paddle = Racket(x=width // 2, y=height - 20)
        self.player = player2(self.player_paddle, self.ball, self.board)

    def run(self):
        while not self.handle_events():
            self.ball.move(self.board, self.player_paddle, self.opponent_paddle)
            self.board.draw(
                self.ball,
                self.player_paddle,
                self.opponent_paddle,
            )
            self.oponent.act(
                self.oponent.racket.rect.centerx - self.ball.rect.centerx,
                self.oponent.racket.rect.centery - self.ball.rect.centery,
            )
            self.player.act(
                (self.player.racket.rect.centerx - self.ball.rect.centerx),
                (self.player.racket.rect.centery - self.ball.rect.centery),
            )
            self.fps_clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                return True
        keys = pygame.key.get_pressed()
        if keys[pygame.constants.K_LEFT]:
            self.player.move_manual(0)
        elif keys[pygame.constants.K_RIGHT]:
            self.player.move_manual(self.board.surface.get_width())
        return False


class NaiveOponent(Player):
    def __init__(self, racket: Racket, ball: Ball, board: Board):
        super(NaiveOponent, self).__init__(racket, ball, board)

    def act(self, x_diff: int, y_diff: int):
        x_cent = self.ball.rect.centerx
        self.move(x_cent)


class HumanPlayer(Player):
    def __init__(self, racket: Racket, ball: Ball, board: Board):
        super(HumanPlayer, self).__init__(racket, ball, board)

    def move_manual(self, x: int):
        self.move(x)


# ----------------------------------
# DO NOT MODIFY CODE ABOVE THIS LINE
# ----------------------------------

# import numpy as np
# import matplotlib.pyplot as plt


class FuzzyPlayerMamdani(Player):
    def __init__(self, racket: Racket, ball: Ball, board: Board):
        super(FuzzyPlayerMamdani, self).__init__(racket, ball, board)
        # for Mamdami:

        # Universos que definen que valores van a poder tomar las diferencias en x e y. Tambien universo de la velocidad
        x_diff_universe = np.arange(-800, 801, 1)
        y_diff_universe = np.arange(0, 401, 1)
        speed_universe = np.arange(-1 * racket.max_speed, racket.max_speed + 1, 1)
        
        # Antecedente de diferencia de x y antecedente de diferencia de y
        x_diff = fuzzcontrol.Antecedent(x_diff_universe, "horizontal_difference")
        y_diff = fuzzcontrol.Antecedent(y_diff_universe, "vertical_difference")

        # Consecuente de velocidad
        speed = fuzzcontrol.Consequent(speed_universe, "speed")


        # Sets de los antecedentes y el consecuente
        x_diff["far_left"] = fuzz.trapmf(x_diff_universe, [-800, -800, -400, -200])
        x_diff["left"] = fuzz.trimf(x_diff_universe, [-400, -200, 0])
        x_diff["center"] = fuzz.trimf(x_diff_universe, [-25, 0, 25])
        x_diff["right"] = fuzz.trimf(x_diff_universe, [0, 200, 400])
        x_diff["far_right"] = fuzz.trapmf(x_diff_universe, [200, 400, 800, 800])

        y_diff["far"] = fuzz.trapmf(y_diff_universe, [300, 350, 400, 400])
        y_diff["middle"] = fuzz.trimf(y_diff_universe, [250, 300, 350])
        y_diff["close"] = fuzz.trapmf(y_diff_universe, [0, 0, 150, 300])

        speed["extra_fast_left"] = fuzz.trapmf(speed_universe, [-10, -10, -9, -8])
        speed["fast_left"] = fuzz.trimf(speed_universe, [-9, -8, -7])
        speed["left"] = fuzz.trimf(speed_universe, [-7, -5, -2])
        speed["stop"] = fuzz.trimf(speed_universe, [-1, 0, 1])
        speed["right"] = fuzz.trimf(speed_universe, [2, 5, 7])
        speed["fast_right"] = fuzz.trimf(speed_universe, [7, 8, 9])
        speed["extra_fast_right"] = fuzz.trapmf(speed_universe, [8, 9, 10, 10])


        # Reglas que determinan el output de la velocidad dependiendo de donde se encuentre la bola
        rules = [
            fuzzcontrol.Rule(x_diff["far_left"] & y_diff["far"], speed["left"]),
            fuzzcontrol.Rule(x_diff["far_left"] & y_diff["middle"], speed["fast_left"]),
            fuzzcontrol.Rule(x_diff["far_left"] & y_diff["close"], speed["extra_fast_left"]),

            fuzzcontrol.Rule(x_diff["left"] & y_diff["far"], speed["left"]),
            fuzzcontrol.Rule(x_diff["left"] & y_diff["middle"], speed["fast_left"]),
            fuzzcontrol.Rule(x_diff["left"] & y_diff["close"], speed["extra_fast_left"]),

            fuzzcontrol.Rule(x_diff["center"] & y_diff["far"], speed["stop"]),
            fuzzcontrol.Rule(x_diff["center"] & y_diff["middle"], speed["stop"]),
            fuzzcontrol.Rule(x_diff["center"] & y_diff["close"], speed["stop"]),

            fuzzcontrol.Rule(x_diff["right"] & y_diff["far"], speed["right"]),
            fuzzcontrol.Rule(x_diff["right"] & y_diff["middle"], speed["fast_right"]),
            fuzzcontrol.Rule(x_diff["right"] & y_diff["close"], speed["extra_fast_right"]),

            fuzzcontrol.Rule(x_diff["far_right"] & y_diff["far"], speed["right"]),
            fuzzcontrol.Rule(x_diff["far_right"] & y_diff["middle"], speed["fast_right"]),
            fuzzcontrol.Rule(x_diff["far_right"] & y_diff["close"], speed["extra_fast_right"])
        ]


        # Creamos el sistema de control
        self.racket_controller = fuzzcontrol.ControlSystemSimulation(
            fuzzcontrol.ControlSystem(rules)
        )

        x_diff.view()
        y_diff.view()
        speed.view()
        

    def act(self, x_diff: int, y_diff: int):
        velocity = self.make_decision(x_diff, y_diff)
        self.move(self.racket.rect.x + velocity)

    def make_decision(self, x_diff: int, y_diff: int):
        # for Mamdami:
        x_diff = (-1) * x_diff

        self.racket_controller.input["horizontal_difference"] = x_diff
        self.racket_controller.input["vertical_difference"] = y_diff
        self.racket_controller.compute()

        velocity = self.racket_controller.output["speed"]
        

        return velocity


class FuzzyPlayerTSK(Player):
    def __init__(self, racket: Racket, ball: Ball, board: Board):
        super(FuzzyPlayerTSK, self).__init__(racket, ball, board)
        
        # Universos que definen que valores van a poder tomar las diferencias en x e y
        self.x_universe = np.arange(-800, 801, 1)
        self.y_universe = np.arange(0, 401, 1)
        
        # Funciones membership para la diferencia horizontal
        self.x_mf = {
            "far_left": fuzz.trapmf(self.x_universe, [-800, -800, -400, -200]),
            "left": fuzz.trimf(self.x_universe, [-400, -200, 0]),
            "center": fuzz.trimf(self.x_universe, [-25, 0, 25]),
            "right": fuzz.trimf(self.x_universe, [0, 200, 400]),
            "far_right": fuzz.trapmf(self.x_universe, [200, 400, 800, 800]),
        }
        
        # Funciones membership para la diferencia vertical
        self.y_mf = {
            "far": fuzz.trapmf(self.y_universe, [300, 350, 400, 400]),
            "middle": fuzz.trimf(self.y_universe, [250, 300, 350]),
            "close": fuzz.trapmf(self.y_universe, [0, 0, 150, 300]),
        }
        
        # Reglas para cada tipo de velocidad, definidas como funciones lambda
        self.velocity_fx = {
            "extra_fast_left": lambda x_diff, y_diff: -1 * (abs(x_diff) + 10/y_diff) * 0.8,
            "fast_left": lambda x_diff, y_diff: -1 * (abs(x_diff) + 10/y_diff) * 0.5,
            "left": lambda x_diff, y_diff: -1 * (abs(x_diff) + 10/y_diff) * 0.3,
            "stop": lambda x_diff, y_diff: 0,
            "right": lambda x_diff, y_diff: (abs(x_diff) + 10/y_diff) * 0.3,
            "fast_right": lambda x_diff, y_diff: (abs(x_diff) + 10/y_diff) * 0.5,
            "extra_fast_right": lambda x_diff, y_diff: (abs(x_diff) + 10/y_diff) * 0.8,
        }

    def act(self, x_diff: int, y_diff: int):
        velocity = self.make_decision(x_diff, y_diff)        
        # Regulamos para que la velocidad no se exceda de diez
        velocity = max(-10, min(10, velocity))
        self.move(self.racket.rect.x + velocity)

    def make_decision(self, x_diff: int, y_diff: int):
        # Calculate membership degrees for x_diff and y_diff
        x_diff = (-1) * x_diff

        x_vals = {
            name: fuzz.interp_membership(self.x_universe, mf, x_diff)
            for name, mf in self.x_mf.items()
        }
        y_vals = {
            name: fuzz.interp_membership(self.y_universe, mf, y_diff)
            for name, mf in self.y_mf.items()
        }
        
        # Rule activations (Zadeh norms - MIN operator for AND, MAX for rule aggregation)
        activations = {
            "extra_fast_left": max(
                [
                    x_vals["far_left"] * y_vals["close"],
                    x_vals["far_left"] * y_vals["middle"],
                    x_vals["left"] * y_vals["close"],
                ]
            ),
            "fast_left": max(
                [
                    x_vals["far_left"] * y_vals["far"],
                    x_vals["left"] * y_vals["middle"],
                ]
            ),
            "left": max(
                [
                    x_vals["left"] * y_vals["far"],
                ]
            ),
            "stop": max(
                [
                    x_vals["center"] * y_vals["far"],
                    x_vals["center"] * y_vals["middle"],
                    x_vals["center"] * y_vals["close"],
                ]
            ),
            "right": max(
                [
                    x_vals["right"] * y_vals["far"],
                ]
            ),
            "fast_right": max(
                [
                    x_vals["far_right"] * y_vals["far"],
                    x_vals["right"] * y_vals["middle"],
                ]
            ),
            "extra_fast_right": max(
                [
                    x_vals["far_right"] * y_vals["close"],
                    x_vals["far_right"] * y_vals["middle"],
                    x_vals["right"] * y_vals["close"],
                ]
            ),
        }
        
        # Calculate weighted sum (TSK defuzzification)
        velocity = sum(
            activations[rule] * self.velocity_fx[rule](x_diff, y_diff)
            for rule in activations
        ) / sum(activations[rule] for rule in activations if activations[rule] > 0)
        
        # Return the final velocity
        return velocity

    


class FuzzyPlayerStrategy(Player):
    def __init__(self, racket: Racket, ball: Ball, board: Board):
        super(FuzzyPlayerStrategy, self).__init__(racket, ball, board)
        # for Mamdami:

        # Universos que definen que valores van a poder tomar las diferencias en x e y. Tambien universo de la velocidad
        x_diff_universe = np.arange(-800, 801, 1)
        y_diff_universe = np.arange(0, 401, 1)
        speed_universe = np.arange(-1 * racket.max_speed, racket.max_speed + 1, 1)
        
        # Antecedente de diferencia de x y antecedente de diferencia de y
        x_diff = fuzzcontrol.Antecedent(x_diff_universe, "horizontal_difference")
        y_diff = fuzzcontrol.Antecedent(y_diff_universe, "vertical_difference")

        # Consecuente de velocidad
        speed = fuzzcontrol.Consequent(speed_universe, "speed")


        # Sets de los antecedentes y el consecuente
        x_diff["far_left"] = fuzz.trapmf(x_diff_universe, [-800, -800, -400, -200])
        x_diff["left"] = fuzz.trimf(x_diff_universe, [-400, -200, 0])
        x_diff["center"] = fuzz.trimf(x_diff_universe, [-50, 0, 50])
        x_diff["right"] = fuzz.trimf(x_diff_universe, [0, 200, 400])
        x_diff["far_right"] = fuzz.trapmf(x_diff_universe, [200, 400, 800, 800])

        y_diff["far"] = fuzz.trapmf(y_diff_universe, [300, 350, 400, 400])
        y_diff["middle"] = fuzz.trimf(y_diff_universe, [250, 300, 350])
        y_diff["close"] = fuzz.trapmf(y_diff_universe, [0, 0, 150, 300])

        speed["extra_fast_left"] = fuzz.trapmf(speed_universe, [-10, -10, -9, -8])
        speed["fast_left"] = fuzz.trimf(speed_universe, [-9, -8, -7])
        speed["left"] = fuzz.trimf(speed_universe, [-7, -5, -2])
        speed["stop"] = fuzz.trimf(speed_universe, [-1, 0, 1])
        speed["right"] = fuzz.trimf(speed_universe, [2, 5, 7])
        speed["fast_right"] = fuzz.trimf(speed_universe, [7, 8, 9])
        speed["extra_fast_right"] = fuzz.trapmf(speed_universe, [8, 9, 10, 10])


        # Reglas que determinan el output de la velocidad dependiendo de donde se encuentre la bola
        rules = [
            fuzzcontrol.Rule(x_diff["far_left"] & y_diff["far"], speed["left"]),
            fuzzcontrol.Rule(x_diff["far_left"] & y_diff["middle"], speed["fast_left"]),
            fuzzcontrol.Rule(x_diff["far_left"] & y_diff["close"], speed["extra_fast_left"]),

            fuzzcontrol.Rule(x_diff["left"] & y_diff["far"], speed["left"]),
            fuzzcontrol.Rule(x_diff["left"] & y_diff["middle"], speed["fast_left"]),
            fuzzcontrol.Rule(x_diff["left"] & y_diff["close"], speed["extra_fast_left"]),

            fuzzcontrol.Rule(x_diff["center"] & y_diff["far"], speed["left"]),
            fuzzcontrol.Rule(x_diff["center"] & y_diff["middle"], speed["left"]),
            fuzzcontrol.Rule(x_diff["center"] & y_diff["close"], speed["fast_left"]),

            fuzzcontrol.Rule(x_diff["right"] & y_diff["far"], speed["right"]),
            fuzzcontrol.Rule(x_diff["right"] & y_diff["middle"], speed["fast_right"]),
            fuzzcontrol.Rule(x_diff["right"] & y_diff["close"], speed["extra_fast_right"]),

            fuzzcontrol.Rule(x_diff["far_right"] & y_diff["far"], speed["right"]),
            fuzzcontrol.Rule(x_diff["far_right"] & y_diff["middle"], speed["fast_right"]),
            fuzzcontrol.Rule(x_diff["far_right"] & y_diff["close"], speed["extra_fast_right"])
        ]


        # Creamos el sistema de control
        self.racket_controller = fuzzcontrol.ControlSystemSimulation(
            fuzzcontrol.ControlSystem(rules)
        )
        

    def act(self, x_diff: int, y_diff: int):
        velocity = self.make_decision(x_diff, y_diff)
        self.move(self.racket.rect.x + velocity)

    def make_decision(self, x_diff: int, y_diff: int):
        x_diff = (-1) * x_diff

        self.racket_controller.input["horizontal_difference"] = x_diff
        self.racket_controller.input["vertical_difference"] = y_diff
        self.racket_controller.compute()

        velocity = self.racket_controller.output["speed"]
        

        return velocity



if __name__ == "__main__":
    # game = PongGame(800, 400, NaiveOponent, HumanPlayer)
    game = PongGame(800, 400, NaiveOponent, FuzzyPlayerStrategy)
    game.run()