# import
from glove import *

window = Display("Tile-Editor", 1200, 700, color.MidnightBlack.value)

left_pane = Sprite(Vector(0, 0), Vector(250, 700), color.Charcoal.value)

def set_left_pane_ratio():
    xy_ratio = left_pane.size.x / left_pane.size.y
    screen_ratio = window.get_size().x / window.get_size().y
    ratio = xy_ratio / screen_ratio * 100

    if ( xy_ratio < ratio ):
        left_pane.size.y = window.get_size().y
        left_pane.size.x = int(left_pane.size.y * xy_ratio)

def draw_panes():
    set_left_pane_ratio()
    left_pane.draw_rect(window)

main_game = Game(window, draw_panes)
main_game.loop()
