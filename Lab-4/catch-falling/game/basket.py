"""
Basket: the player-controlled catcher at the bottom of the screen.
"""

import pygame

BOOST_SPEED_MULTIPLIER = 2.0     # boosted speed = normal speed * this
BOOST_DURATION_FRAMES = 90       # how long a boost lasts (1.5 s at 60 FPS)
BOOST_COOLDOWN_FRAMES = 150      # recharge time after a boost ends (2.5 s)


class Basket:
    def __init__(self, x, y, width=90, height=24, speed=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.boosted_frames = 0          # frames of boost remaining
        self.cooldown_frames = 0         # frames of cooldown remaining
        self.normal_speed = speed
        self.boost_speed = speed * BOOST_SPEED_MULTIPLIER

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )

    def is_boosted(self):
        return self.boosted_frames > 0

    def can_boost(self):
        return self.boosted_frames == 0 and self.cooldown_frames == 0

    def activate_boost(self):
        """Start a boost if one is available. Returns True if it started."""
        if not self.can_boost():
            return False
        self.boosted_frames = BOOST_DURATION_FRAMES
        self.speed = self.boost_speed
        return True

    def update_boost(self):
        """Call once per frame: run down the boost, then the cooldown."""
        if self.boosted_frames > 0:
            self.boosted_frames -= 1
            if self.boosted_frames == 0:
                self.speed = self.normal_speed
                self.cooldown_frames = BOOST_COOLDOWN_FRAMES
        elif self.cooldown_frames > 0:
            self.cooldown_frames -= 1

    def boost_fraction(self):
        """Fraction of the active boost left (1.0 just started, 0.0 over)."""
        return self.boosted_frames / BOOST_DURATION_FRAMES

    def cooldown_fraction(self):
        """Fraction of the cooldown left (1.0 just started, 0.0 ready)."""
        return self.cooldown_frames / BOOST_COOLDOWN_FRAMES