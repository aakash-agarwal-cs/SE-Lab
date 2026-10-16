"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (25, 30, 45)
COLOR_BASKET = (150, 110, 70)
COLOR_BASKET_BOOST = (255, 200, 60)
COLOR_TEXT = (255, 255, 255)
COLOR_BOOST_ACTIVE = (255, 200, 60)
COLOR_BOOST_COOLDOWN = (130, 140, 160)
COLOR_BOOST_READY = (100, 220, 130)
COLOR_BAR_BG = (60, 66, 85)

BOOST_BAR_POS = (10, 92)
BOOST_BAR_SIZE = (160, 12)


def draw_scene(surface, basket, objects):
    surface.fill(COLOR_BG)
    for obj in objects:
        pygame.draw.circle(surface, obj.color, (int(obj.x), int(obj.y)), obj.radius)
    basket_color = COLOR_BASKET_BOOST if basket.is_boosted() else COLOR_BASKET
    pygame.draw.rect(surface, basket_color, basket.get_rect(), border_radius=6)


def draw_boost_hud(surface, font, basket):
    """Boost label plus a bar: shrinks while active, refills while recharging."""
    if basket.is_boosted():
        label, color, fill = "BOOST!", COLOR_BOOST_ACTIVE, basket.boost_fraction()
    elif basket.cooldown_frames > 0:
        label, color, fill = "Boost recharging...", COLOR_BOOST_COOLDOWN, 1 - basket.cooldown_fraction()
    else:
        label, color, fill = "Boost ready [SPACE]", COLOR_BOOST_READY, 1.0

    draw_text(surface, font, label, (10, 62), color)

    x, y = BOOST_BAR_POS
    w, h = BOOST_BAR_SIZE
    pygame.draw.rect(surface, COLOR_BAR_BG, (x, y, w, h), border_radius=4)
    fill_w = int(w * fill)
    if fill_w > 0:
        pygame.draw.rect(surface, color, (x, y, fill_w, h), border_radius=4)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (255, 220, 80))
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(surf, rect)