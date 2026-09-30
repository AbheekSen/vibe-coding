"""
GameEngine: owns the paddle, ball, bricks, lives, score and combo.

States: "playing", "game_over", "won". Press R at any time to restart.
"""

import pygame

from game.paddle import Paddle
from game.ball import Ball
from game.brick import Brick, NORMAL, STRONG, UNBREAKABLE
from game.collision import handle_ball_brick_collision
from game.renderer import WIDTH, HEIGHT

BRICK_ROWS = 4
BRICK_COLS = 8
BRICK_WIDTH = 68
BRICK_HEIGHT = 22
BRICK_GAP = 6
BRICK_TOP_MARGIN = 50

STARTING_LIVES = 3

# One character per brick: S = strong, N = normal, U = unbreakable.
LAYOUT = [
    "SSSSSSSS",
    "NNNNNNNN",
    "UNNNNNNU",
    "NNNNNNNN",
]
LAYOUT_TYPES = {"N": NORMAL, "S": STRONG, "U": UNBREAKABLE}


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        """Completely reset the game to its starting state."""
        self.paddle = Paddle(x=WIDTH / 2, y=HEIGHT - 30)
        self.ball = Ball(x=WIDTH / 2, y=HEIGHT - 50)
        self.bricks = self._build_bricks()
        self.lives = STARTING_LIVES
        self.score = 0
        self.combo = 1
        self.state = "playing"

    def _build_bricks(self):
        bricks = []
        total_width = BRICK_COLS * (BRICK_WIDTH + BRICK_GAP) - BRICK_GAP
        start_x = (WIDTH - total_width) / 2
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = start_x + col * (BRICK_WIDTH + BRICK_GAP)
                y = BRICK_TOP_MARGIN + row * (BRICK_HEIGHT + BRICK_GAP)
                brick_type = LAYOUT_TYPES[LAYOUT[row][col]]
                bricks.append(Brick(x, y, BRICK_WIDTH, BRICK_HEIGHT, brick_type))
        return bricks

    def _reset_ball(self):
        self.ball = Ball(x=WIDTH / 2, y=HEIGHT - 50)

    def _reset_paddle(self):
        self.paddle = Paddle(x=WIDTH / 2, y=HEIGHT - 30)

    def _breakable_left(self):
        return sum(1 for b in self.bricks if b.is_breakable)

    def handle_input(self, keys_pressed):
        if self.state != "playing":
            return
        dx = 0
        if keys_pressed[pygame.K_LEFT]:
            dx -= self.paddle.speed
        if keys_pressed[pygame.K_RIGHT]:
            dx += self.paddle.speed
        self.paddle.move(dx, WIDTH)

    def handle_keydown(self, key):
        if key == pygame.K_r:
            self.reset()

    def update(self):
        if self.state != "playing":
            return

        self.ball.update()
        self.ball.bounce_off_walls(WIDTH)

        if self.ball.get_rect().colliderect(self.paddle.get_rect()) and self.ball.vy > 0:
            self.ball.bounce_off_paddle(self.paddle.get_rect())

        for brick in self.bricks:
            if handle_ball_brick_collision(self.ball, brick):
                if brick.hit():
                    self.bricks.remove(brick)
                    self.score += brick.points * self.combo
                    self.combo += 1
                break

        if self.ball.is_below(HEIGHT):
            self.lives -= 1
            self.combo = 1
            if self.lives <= 0:
                self.lives = 0
                self.state = "game_over"
            else:
                self._reset_ball()
                self._reset_paddle()
            return

        if self._breakable_left() == 0:
            self.state = "won"

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.paddle, self.ball, self.bricks)
        renderer.draw_hud(surface, font, self.score, self.combo, self.lives,
                          self._breakable_left())
        if self.state == "game_over":
            renderer.draw_banner(surface, font, "GAME OVER")
            renderer.draw_banner(surface, font, "Press R to restart", y_offset=32,
                                 color=(255, 255, 255))
        elif self.state == "won":
            renderer.draw_banner(surface, font, "YOU WIN!")
            renderer.draw_banner(surface, font, "Press R to restart", y_offset=32,
                                 color=(255, 255, 255))
