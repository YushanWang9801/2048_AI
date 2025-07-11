# utils.py
WIDTH = 500
HEIGHT = 600
GRID_SIZE = 4
TILE_SIZE = 100
GRID_PADDING = 10
FONT_SIZE = 36
SMALL_FONT_SIZE = 20

BACKGROUND_COLOR = (250, 248, 239)
GRID_COLOR = (187, 173, 160)
TEXT_COLOR = (119, 110, 101)
BRIGHT_TEXT_COLOR = (255, 255, 255)
GAMEOVER_BG_COLOR = (240, 240, 240, 200)

TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

TEXT_COLORS = {
    2: TEXT_COLOR,
    4: TEXT_COLOR,
    8: BRIGHT_TEXT_COLOR,
    16: BRIGHT_TEXT_COLOR,
    32: BRIGHT_TEXT_COLOR,
    64: BRIGHT_TEXT_COLOR,
    128: BRIGHT_TEXT_COLOR,
    256: BRIGHT_TEXT_COLOR,
    512: BRIGHT_TEXT_COLOR,
    1024: BRIGHT_TEXT_COLOR,
    2048: BRIGHT_TEXT_COLOR,
}
