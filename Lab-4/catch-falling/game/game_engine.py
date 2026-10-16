"""
GameEngine: owns the basket and all falling objects.
"""

import random
import pygame

from game.basket import Basket
from game.falling_object import FallingObject
from game.collision import is_caught
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_MIN_FRAMES = 30   # shortest wait between spawns
SPAWN_INTERVAL_MAX_FRAMES = 70   # longest wait between spawns
MAX_OBJECTS_ON_SCREEN = 6        # no new spawns while this many are falling
MIN_SPAWN_X_DISTANCE = 120       # min horizontal gap from the previous spawn
OBJECT_RADIUS = 14
OBJECT_SPEED = 3
MAX_MISSES = 5


class GameEngine:
    def __init__(self):
        self.basket = Basket(x=WIDTH / 2, y=HEIGHT - 30)
        self.objects = []
        self.frames_until_spawn = 0
        self.last_spawn_x = None
        self.score = 0
        self.misses = 0
        self.game_over = False

    def _pick_spawn_x(self):
        low = OBJECT_RADIUS
        high = WIDTH - OBJECT_RADIUS
        if self.last_spawn_x is None:
            return random.randint(low, high)

        # Valid zones: far enough left or far enough right of the last spawn.
        zones = []
        left_high = self.last_spawn_x - MIN_SPAWN_X_DISTANCE
        right_low = self.last_spawn_x + MIN_SPAWN_X_DISTANCE
        if left_high >= low:
            zones.append((low, left_high))
        if right_low <= high:
            zones.append((right_low, high))

        if not zones:
            # Min distance is too large to satisfy; use the farthest edge.
            return low if self.last_spawn_x > WIDTH / 2 else high

        # Weight by zone width so every valid x is equally likely.
        zone_low, zone_high = random.choices(
            zones, weights=[b - a + 1 for a, b in zones]
        )[0]
        return random.randint(zone_low, zone_high)

    def _spawn_object(self):
        x = self._pick_spawn_x()
        self.last_spawn_x = x
        self.objects.append(
            FallingObject(x=x, y=-OBJECT_RADIUS, radius=OBJECT_RADIUS, speed=OBJECT_SPEED)
        )

    def handle_input(self, keys_pressed):
        if self.game_over:
            return
        if keys_pressed[pygame.K_LEFT]:
            self.basket.x -= self.basket.speed
        if keys_pressed[pygame.K_RIGHT]:
            self.basket.x += self.basket.speed
        # Boundary handling: clamp the center so the whole basket stays on
        # screen, i.e. its edges stop at 0 and WIDTH.
        half_width = self.basket.width / 2
        self.basket.x = max(half_width, min(WIDTH - half_width, self.basket.x))

    def handle_keydown(self, key):
        if self.game_over:
            if key == pygame.K_r:
                self.__init__()      # fresh Basket too, so boost state resets
            return
        if key == pygame.K_SPACE:
            self.basket.activate_boost()

    def update(self):
        if self.game_over:
            return

        self.basket.update_boost()

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            if len(self.objects) < MAX_OBJECTS_ON_SCREEN:
                self._spawn_object()
            self.frames_until_spawn = random.randint(
                SPAWN_INTERVAL_MIN_FRAMES, SPAWN_INTERVAL_MAX_FRAMES
            )

        for obj in self.objects:
            obj.update()

        basket_rect = self.basket.get_rect()
        caught = [o for o in self.objects if is_caught(basket_rect, o)]
        if caught:
            self.objects = [o for o in self.objects if o not in caught]
            self.score += len(caught)

        missed = [o for o in self.objects if o.is_past_bottom(HEIGHT)]
        if missed:
            self.objects = [o for o in self.objects if not o.is_past_bottom(HEIGHT)]
            self.misses += len(missed)
            if self.misses >= MAX_MISSES:
                self.game_over = True

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.basket, self.objects)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Misses: {self.misses}/{MAX_MISSES}", (10, 36))
        renderer.draw_boost_hud(surface, font, self.basket)

        if self.game_over:
            renderer.draw_banner(surface, font, f"Game Over! Final score: {self.score}. Press R to restart.")