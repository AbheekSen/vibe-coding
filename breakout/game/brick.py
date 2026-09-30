"""
Brick: a single block. Three types:
  - NORMAL:       destroyed after 1 hit
  - STRONG:       destroyed after several hits (STRONG_HITS)
  - UNBREAKABLE:  never destroyed
"""

import pygame

NORMAL = "normal"
STRONG = "strong"
UNBREAKABLE = "unbreakable"

STRONG_HITS = 3

POINTS = {NORMAL: 10, STRONG: 30, UNBREAKABLE: 0}

COLOR_NORMAL = (200, 90, 90)
COLOR_UNBREAKABLE = (120, 125, 140)
# Strong brick color depends on how many hits it has left.
COLOR_STRONG_BY_HITS = {
    3: (150, 70, 200),
    2: (200, 110, 230),
    1: (235, 170, 250),
}


class Brick:
    def __init__(self, x, y, width, height, brick_type=NORMAL):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.brick_type = brick_type
        if brick_type == STRONG:
            self.hits_remaining = STRONG_HITS
        elif brick_type == UNBREAKABLE:
            self.hits_remaining = float("inf")
        else:
            self.hits_remaining = 1

    @property
    def is_breakable(self):
        return self.brick_type != UNBREAKABLE

    @property
    def points(self):
        return POINTS[self.brick_type]

    @property
    def color(self):
        if self.brick_type == UNBREAKABLE:
            return COLOR_UNBREAKABLE
        if self.brick_type == STRONG:
            return COLOR_STRONG_BY_HITS.get(int(self.hits_remaining), COLOR_STRONG_BY_HITS[1])
        return COLOR_NORMAL

    def hit(self):
        """Register one hit. Returns True if the brick is destroyed by it."""
        if not self.is_breakable:
            return False
        self.hits_remaining -= 1
        return self.hits_remaining <= 0

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
