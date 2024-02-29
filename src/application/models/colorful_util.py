import random
from typing import List

l_values = [80, 80, 76, 75, 79, 71, 82]
l_index = 0


def generate_random_hsl() -> str:
    h = random.randint(0, 360)
    global l_index

    if l_index < len(l_values):
        l = l_values[l_index]
        l_index += 1
    else:
        l_index = 0
        l = l_values[l_index]
        l_index += 1

    return f"{h}, 100%, {l}%"


def generate_random_coordinates() -> List[str]:
    coordinates = [
        f"{random.randint(0, 100)}% {random.randint(0, 100)}%" for _ in range(6)
    ]
    return coordinates


def generate_css() -> str:
    bg_color_hsl = generate_random_hsl()
    gradient_colors_hsl = [generate_random_hsl() for _ in range(6)]
    gradient_coordinates = generate_random_coordinates()

    css_background = f"background-color: hsl({bg_color_hsl}); background-image:"

    for index, color in enumerate(gradient_colors_hsl):
        coordinates = gradient_coordinates[index]
        css_background += (
            f" radial-gradient(at {coordinates}, hsl({color}) 0px, transparent 50%),"
        )

    css_background = css_background[:-1]

    return css_background
