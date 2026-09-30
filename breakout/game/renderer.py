"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

from game.brick import STRONG, UNBREAKABLE

WIDTH, HEIGHT = 640, 520
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (20, 20, 30)
COLOR_PADDLE = (80, 180, 255)
COLOR_BALL = (240, 240, 240)
COLOR_TEXT = (255, 255, 255)
COLOR_COMBO = (255, 220, 80)
COLOR_LIFE = (255, 100, 100)


def _draw_brick(surface, brick):
    rect = brick.get_rect()
    pygame.draw.rect(surface, brick.color, rect)
    if brick.brick_type == UNBREAKABLE:
        # Metallic look: light frame plus a cross.
        pygame.draw.rect(surface, (200, 205, 220), rect, 2)
        pygame.draw.line(surface, (70, 72, 85), rect.topleft, rect.bottomright, 2)
        pygame.draw.line(surface, (70, 72, 85), rect.topright, rect.bottomleft, 2)
    elif brick.brick_type == STRONG:
        # Thick white frame plus one pip per remaining hit.
        pygame.draw.rect(surface, (255, 255, 255), rect, 2)
        pips = int(brick.hits_remaining)
        spacing = 14
        start_x = rect.centerx - (pips - 1) * spacing / 2
        for i in range(pips):
            pygame.draw.circle(surface, (255, 255, 255),
                               (int(start_x + i * spacing), rect.centery), 3)
    else:
        pygame.draw.rect(surface, (10, 10, 15), rect, 1)


def draw_scene(surface, paddle, ball, bricks):
    surface.fill(COLOR_BG)
    for brick in bricks:
        _draw_brick(surface, brick)
    pygame.draw.rect(surface, COLOR_PADDLE, paddle.get_rect(), border_radius=4)
    pygame.draw.circle(surface, COLOR_BALL, (int(ball.x), int(ball.y)), ball.radius)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_hud(surface, font, score, combo, lives, bricks_left):
    draw_text(surface, font, f"Score: {score}", (10, 10))
    draw_text(surface, font, f"Combo: x{combo}", (185, 10), COLOR_COMBO)
    draw_text(surface, font, f"Lives: {lives}", (330, 10), COLOR_LIFE)
    draw_text(surface, font, f"Bricks: {bricks_left}", (450, 10))


def draw_banner(surface, font, text, y_offset=0, color=(255, 220, 80)):
    surf = font.render(text, True, color)
    rect = surf.get_rect(
        center=(surface.get_width() // 2, surface.get_height() // 2 + y_offset)
    )
    surface.blit(surf, rect)
