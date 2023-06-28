# imports
import random
from engine.glove import *

# init window
window = Display("Heart", 1200, 700, color.white.value, fps=120)

player = Sprite(50, 50, 30, 30, color.Black.value)
# platform0 = Sprite(50, 400, 500, 50, color.JetBlack.value)
# platform1 = Sprite(600, 300, 500, 50, color.JetBlack.value)

platforms = []
for _ in range(20):
    if platforms == []:
        posx = 0
        posy = 400
    else:
        posx = platforms[len(platforms) - 1].position.x + random.choice([100, 150, 200, 250, 300, 350]) + 800
        if random.choice([true, false]):
            posy = platforms[len(platforms) - 1].position.y + 50
        else:
            posy = platforms[len(platforms) - 1].position.y - 50

    platforms.append(Sprite(posx, posy, 800, 50, color.JetBlack.value))

input2d = Input2D(4)
input2d.down_vector = Vector(0, 0)
input2d.up_vector = Vector(0, 0)

input2d.inputs.set_key("jump", K_SPACE)
input2d.inputs.set_key("camera_left", K_q)
input2d.inputs.set_key("camera_right", K_e)
input2d.inputs.set_key("camera_up", K_w)
input2d.inputs.set_key("camera_down", K_s)

g = Vector(-100, 1000)
v = Vector(0, 0)

player.add_physics()
player.physics.add_gravity(g, v)
player.physics.add_collision(*platforms)

font = FontRenderingSystem(window, "monospace", 20, color.Black.value)
layer = Layer(window, player, *platforms)
camera = Camera2D(window, player, layer)

box_size = Vector(window.get_size().x / 100 * 70, window.get_size().y / 100 * 40)

def debug_print():
    c = [
            player.physics.collision.top,
            player.physics.collision.left,
            player.physics.collision.bottom,
            player.physics.collision.right,
        ]

    font.create((5, 5), f"collision: { player.physics.collision.collide }")
    font.create((5, 25), f"top: { c[0] }, left: { c[1] }, bottom: { c[2] }, right: { c[3] }")
    font.create((5, 50), f"pos: ( { int(player.position.x) }, { int(player.position.y) })")
    font.create((5, 75), f"vilocity: { player.physics.velocity }")
    font.debug_fps((window.get_size().x - 100, 5), (200, 50, 50))

def main_game(delta):
    input2d.move_player(player)

    if input2d.inputs.is_key_pressed("jump") and player.physics.collision.collide:
        player.physics.velocity.y = -500

    # camera.target_centered()
    camera.free_box_movement(box_size)

    font.render()
    font.clear()
    camera.render(delta)

# main-game
main_game = Game(window, main_game)
main_game.loop()
