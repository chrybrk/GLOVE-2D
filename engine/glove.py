# import
import pygame
import sys
from pygame.locals import *
from enum import Enum

# constants
true = True; false = False; nil = None

clock = pygame.time.Clock()
def fpsLock(fps): return clock.tick(fps)

class color(Enum):
    Black = (0, 0, 0)
    MidnightBlack = (40, 40, 43)
    Charcoal = (54, 69, 79)
    JetBlack = (52, 52, 52)
    DarkSlateGray = (47, 79, 79)
    SlateGray = (112, 128, 144)
    LightSlateGray = (119, 136, 153)
    white = (255, 255, 255)

# Physics
class Vector(object):
    def __init__(self, x: int = 0, y: int = 0, z: int = 0) -> nil:
        self.x: int = x
        self.y: int = y
        self.z: int = z

    def __add__(self, vec2: object) -> object:  return Vector(self.x + vec2.x, self.y + vec2.y, self.z + vec2.z)
    def __sub__(self, vec2: object) -> object:  return Vector(self.x - vec2.x, self.y - vec2.y, self.z - vec2.z)
    def __mul__(self, vec2: object) -> object:  return Vector(self.x * vec2.x, self.y * vec2.y, self.z * vec2.z)
    def dot(self, vec2: object) -> object:      return Vector(self.x * vec2.x, self.y * vec2.y, self.z * vec2.z)
    def cross(self, vec2: object) -> object:    return Vector((self.y * vec2.z + vec2.y * self.z), (self.x * vec2.z + vec2.x * self.z), (self.x * vec2.y + vec2.x * self.y))
    def scalar(self, value: int) -> object:     return Vector(self.x * value, self.y * value)
    def value2(self) -> tuple[int, int]:        return (self.x, self.y)

    def __repr__(self) -> str: return f"Vector({self.x}, {self.y}, {self.z})"

class Collision():
    def __init__(self, mask: list[object]) -> nil:
        self.top = false
        self.left = false
        self.bottom = false
        self.right = false
        self.collide = false

        self.mask = mask

    def append_mask(self, value: object) -> nil: self.mask.append(value)

    def pop_mask(self, value: object) -> object: return self.mask.pop(self.mask.index(value))

    def collision_testing(self, a: object) -> nil:
        collision_hit = []

        self.top = false
        self.left = false
        self.bottom = false
        self.right = false

        self.dist = 10

        for b in self.mask:
            if b.position.x - a.size.x <= a.position.x <= b.position.x + b.size.x and b.position.y - a.size.y <= a.position.y <= b.position.y + b.size.y:
                collision_hit.append(b)

        self.collide = true if len(collision_hit) > 0 else false

        for b in collision_hit:
            top = abs((b.position.y + b.size.y) - a.position.y)
            left = abs(b.position.x - (a.position.x + a.size.x))
            bottom = abs(b.position.y - (a.position.y + a.size.y))
            right = abs((b.position.x + b.size.x) - a.position.x)

            self.top = true if top <= self.dist else false
            self.left = true if left <= self.dist else false
            self.bottom = true if bottom <= self.dist else false
            self.right = true if right <= self.dist else false

            if self.bottom:
                a.position.y = b.position.y - a.size.y

class Physics:
    def __init__(self) -> nil:
        self.fall_flag = false
        self.collision_flag = false

        self.gravity = Vector(0, 0)
        self.velocity = Vector(0, 0)
        self.collision = nil

    def add_gravity(self, gravity: Vector, velocity: Vector) -> nil:
        self.fall_flag = true
        self.gravity = gravity
        self.velocity = velocity

    def add_collision(self, *mask: list[object]) -> nil:
        self.collision_flag = true
        self.collision = Collision(mask)

    def apply(self, rect: object, delta: float) -> nil:
        if self.fall_flag:
            rect.position.y = rect.position.y + delta * self.velocity.y
            self.velocity.y = self.velocity.y + delta * self.gravity.y

        if self.collision_flag:
            self.collision.collision_testing(rect)
            if self.collision.bottom: self.velocity = Vector(0, 0)

# Display
class Display:
    def __init__(self, title: str, width: int, height: int, color: tuple[int], resizable: bool = false, fps: int = 60) -> nil:
        pygame.init()

        self.title: int = title
        self.width: int = width
        self.height: int = height
        self.color: tuple[int] = color
        self.alive: bool = true
        self.fps: int = fps

        self.window: pygame.display = pygame.display.set_mode((width, height), pygame.RESIZABLE if resizable else 0)
        pygame.display.set_caption(self.title)

    def get_size(self: object) -> Vector: return Vector(self.window.get_size()[0], self.window.get_size()[1])

    def is_alive(self: object) -> nil: return self.alive

# Sprite
class Animation: pass

class Sprite:
    def __init__(self, x: int, y: int, w: int, h: int, color: tuple[int]) -> nil:
        self.position = Vector(x, y)
        self.size = Vector(w, h)
        self.color = color
        self.physics = nil
        self.function = nil

    def add_function(self, sprite_function: object) -> nil:
        self.function = sprite_function

    def add_physics(self, physics: Physics = nil) -> nil: self.physics = Physics() if not physics else physics

    def draw_rect(self, window: Display, delta: float = 0) -> pygame.draw:
        if self.function: self.function()
        if self.physics:
            if delta == 0: print("Warning: missing `delta`, physics component required.")
            self.physics.apply(self, delta)
        return pygame.draw.rect(window.window, self.color, (self.position.x, self.position.y, self.size.x, self.size.y))

class Input:
    def __init__(self) -> nil:
        self.inputs: dict = {}

    def set_key(self, name: str, key: int) -> nil: self.inputs[name] = key
    
    def get_key(self) -> dict: return self.inputs

    def on_key_press(self, name: str, sprite: Sprite, position: Vector, speed: Vector) -> nil:
        keys = pygame.key.get_pressed()
        if keys[self.get_key()[name]]:
            sprite.position.x += position.x * speed.x
            sprite.position.y += position.y * speed.y
            sprite.position.z += position.z * speed.z
    
    def is_key_pressed(self, name: str) -> bool: return pygame.key.get_pressed()[self.get_key()[name]]

class Input2D:
    def __init__(self, speed: int) -> nil:
        self.inputs = Input()

        self.inputs.set_key("up", K_w)
        self.inputs.set_key("down", K_s)
        self.inputs.set_key("left", K_a)
        self.inputs.set_key("right", K_d)

        self.speed = Vector(speed, speed)

        self.up_vector = Vector(0, -1)
        self.down_vector = Vector(0, 1)
        self.left_vector = Vector(-1, 0)
        self.right_vector = Vector(1, 0)

    def move_player(self, player: Sprite) -> nil:
        self.inputs.on_key_press("up", player, self.up_vector, self.speed)
        self.inputs.on_key_press("down", player, self.down_vector, self.speed)
        self.inputs.on_key_press("left", player, self.left_vector, self.speed)
        self.inputs.on_key_press("right", player, self.right_vector, self.speed)

class FontRenderingSystem:
    def __init__(self, window: Display, font_family: str, font_size: int, color: tuple[int, int, int], smooth: int = 1) -> nil:
        self.window = window
        self.font = pygame.font.SysFont(font_family, font_size)
        self.color = color
        self.smooth = smooth

        self.fonts = []

        self.d_fps = nil

    def debug_fps(self, position: tuple[int, int], color: tuple[int, int, int] = nil) -> nil:
        self.d_fps = { 'fnt': self.font.render(f"fps: { int(clock.get_fps()) }", self.smooth, color if color else self.color), 'size': position }

    def create(self, position: tuple[int, int], text: str, color: tuple[int, int, int] = nil) -> nil:
        font = { 'fnt': self.font.render(text, self.smooth, color if color else self.color), 'size': position }
        self.fonts.append(font)

    def clear(self) -> nil:
        for font in self.fonts: del font
        self.fonts = []

    def render(self) -> nil:
        if self.d_fps: self.fonts.append(self.d_fps)
        for font in self.fonts:
            self.window.window.blit(font['fnt'], font['size'])

class Layer:
    def __init__(self, window: Display, *sprites: Sprite) -> nil:
        self.window = window
        self.sprites = sprites

    def run(self, delta: float = 0) -> nil:
        for sprite in self.sprites: sprite.draw_rect(self.window, delta)

class Camera2D:
    def __init__(self, window: Display, target: Sprite, layer: Layer) -> nil:
        self.window = window
        self.target = target
        self.layer = layer
        self.position = Vector(0, 0)
        self.offset = Vector(0, 0)
        self.size = self.window.get_size()
        self.keyboard_speed = 5

    def calculate_position(self, position: Vector) -> nil:
        self.position = position
        for sprite in self.layer.sprites:
            sprite.position.x += self.position.x
            sprite.position.y += self.position.y

    def target_centered(self) -> nil:
        cx = self.window.get_size().x / 2
        cy = self.window.get_size().y / 2

        self.calculate_position(Vector(cx - self.target.position.x, cy - self.target.position.y))

    def free_box_movement(self, box_size: Vector, debug_draw: bool = false) -> nil:
        cx = self.window.get_size().x / 2
        cy = self.window.get_size().y / 2

        posx = cx - box_size.x + (box_size.x / 2)
        posy = cy - box_size.y + (box_size.y / 2)

        bl = self.window.get_size().x - box_size.x - posx
        br = self.window.get_size().x - box_size.x - posx
        bt = self.window.get_size().y - box_size.y - posy
        bb = self.window.get_size().y - box_size.y - posy

        if self.target.position.x < posx: posx = self.target.position.x
        if self.target.position.x > box_size.x + (br - self.target.size.x): posx = br + (self.target.position.x - (box_size.x + (br - self.target.size.x)))
        if self.target.position.y < posy: posy = self.target.position.y
        if self.target.position.y > box_size.y + (bb - self.target.size.y): posy = bb + (self.target.position.y - (box_size.y + (bb - self.target.size.y)))

        x = posx - bl
        y = posy - bt

        for sprite in self.layer.sprites:
            sprite.position.x += x * (-1)
            sprite.position.y += y * (-1)

        if debug_draw:
            pygame.draw.rect(self.window.window, color.JetBlack.value, (posx, posy, box_size.x, box_size.y), 5)

    def keyboard_movement(self, input2D: Input2D) -> nil:
        if input2D.inputs.is_key_pressed("camera_left"): self.offset.x = self.keyboard_speed
        elif input2D.inputs.is_key_pressed("camera_right"): self.offset.x = -self.keyboard_speed
        else: self.offset.x = 0

        if input2D.inputs.is_key_pressed("camera_up"): self.offset.y = self.keyboard_speed
        elif input2D.inputs.is_key_pressed("camera_down"): self.offset.y = -self.keyboard_speed
        else: self.offset.y = 0

        for sprite in self.layer.sprites:
            sprite.position.x += self.offset.x
            sprite.position.y += self.offset.y

    def render(self, delta: float = 0) -> nil:
        self.layer.run(delta)

# Game - Object
class Game:
    def __init__(self, window: Display, *functions: list[object]) -> nil:
        self.window: Display = window
        self.functions = functions

    def loop(self) -> nil:
        while self.window.is_alive():
            self.window.window.fill(self.window.color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.window.alive = false

            for function in self.functions: function(fpsLock(self.window.fps) / 1000)

            pygame.display.update()
            fpsLock(self.window.fps)

def clamp(a, b):
    if b > 0:
        if a > b: return b
    elif b < 0:
        if a < b: return b
    return a
