"""
collision: figures out whether a falling object is within the basket.
"""


def is_caught(basket_rect, obj):
    # Horizontal: the object's center is within the basket's span.
    in_x = basket_rect.left <= obj.x <= basket_rect.right
    # Vertical: the circle overlaps the basket's height band. The first
    # check means it has reached the basket's top; the second means it
    # hasn't already fallen completely past the bottom, so a basket
    # sliding under an object that already missed can't catch it.
    in_y = (obj.y + obj.radius >= basket_rect.top
            and obj.y - obj.radius <= basket_rect.bottom)
    return in_x and in_y