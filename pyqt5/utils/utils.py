from PIL import ImageGrab


def get_real_resolution():
    screen = ImageGrab.grab()
    screen_width, screen_height = screen.size
    return screen_width, screen_height
