# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 811

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Fonts (initialized in main.py)
FONT = None
SMALL_FONT = None

# Paths
TILESET_PATH = 'maps/tileset.png'
BACKGROUND_PATH = 'Mainmenu/Background.jpg'
START_BUTTON_PATH = 'Mainmenu/Start_game_button.png'
START_BUTTON_HOVER_PATH = 'Mainmenu/Start_game_button_hover.png'
QUIT_BUTTON_HOVER_PATH = 'Mainmenu/Load_game_button_hover.png'
QUIT_BUTTON_PATH = 'Mainmenu/Load_game_button.png'
TITLE_PATH = 'Mainmenu/Title.png'
HEART_IMAGE_PATH = 'health/heart.png'
# Map CSV Paths
MAP_CSV_PATHS = [
    "maps/map_default/map_default._no-stepping1.csv",
    "maps/map_default/map_default._step.csv", 
    "maps/map_default/map_default._step2.csv",
    "maps/map_default/map_default._no-stepping2.csv",
    "maps/map_default/map_default._fence2.csv",
    "maps/map_default/map_default._temple.csv",
    "maps/map_default/map_default._temple2.csv",
    "maps/map_default/map_default._cemetery.csv",
    "maps/map_default/map_default._fence.csv",
    "maps/map_default/map_default._bridge.csv",
    "maps/map_default/map_default._trees.csv",
    "maps/map_default/map_default._underground.csv",
    "maps/map_default/map_default._houses1.csv",
    "maps/map_default/map_default._banners.csv",
    "maps/map_default/map_default._houses2.csv",
]

# Layers that act as obstacles
OBSTACLE_LAYERS = [0, 3, 4, 5, 7, 8, 10, 11, 12, 14]

# Player properties
PLAYER_SPEED = 200
ANIMATION_SPEED = 0.1

# Map properties
TILE_SIZE = 16
MAP_SCALE = SCREEN_WIDTH / (10 * TILE_SIZE)
SCALED_TILE_SIZE = int(TILE_SIZE * MAP_SCALE)
