import pygame
from utils import Animation, load_tpng_folder, Vector2
from scene import Scene


class Entity:
    def __init__(self, center=(0, 0), hitbox=(0, 0), scene: Scene = None):

        self.scene = scene
        self.game = scene.game
        self.frame: pygame.Surface = scene.frame
        self.center: Vector2 = Vector2(center)
        self.velocity: Vector2 = Vector2(0, 0)
        self.hitbox = hitbox
        self.action = None
        self.animations = {}
        self.facing = 'down'
        self.animation_locked = False

    def update(self):
        self.animations[self.action + "/" + self.facing].update()

    def img(self):
        return self.animations[self.action].img()

class Player(Entity):
    def __init__(self, center=(0, 0), hitbox=(0, 0), scene: Scene = None):
        super().__init__(center=center, hitbox=hitbox, scene=scene)
        self.action = 'idle'
        self.animations = {

            # attack
            "attack/up": Animation(load_tpng_folder("jackwizards/animations/player/attack/up"), img_dur=8, loop=True),
            "attack/left": Animation(load_tpng_folder("jackwizards/animations/player/attack/left"), img_dur=8, loop=True),
            "attack/right": Animation(load_tpng_folder("jackwizards/animations/player/attack/right"), img_dur=8, loop=True),
            "attack/down": Animation(load_tpng_folder("jackwizards/animations/player/attack/down"), img_dur=8, loop=True),

            # block
            "block/up": Animation(load_tpng_folder("jackwizards/animations/player/block/up"), img_dur=15, loop=True),
            "block/left": Animation(load_tpng_folder("jackwizards/animations/player/block/left"), img_dur=15, loop=True),
            "block/right": Animation(load_tpng_folder("jackwizards/animations/player/block/right"), img_dur=15, loop=True),
            "block/down": Animation(load_tpng_folder("jackwizards/animations/player/block/down"), img_dur=15, loop=True),

            # idle
            "idle/up": Animation(load_tpng_folder("jackwizards/animations/player/idle/up"), img_dur=15, loop=True),
            "idle/left": Animation(load_tpng_folder("jackwizards/animations/player/idle/left"), img_dur=15, loop=True),
            "idle/right": Animation(load_tpng_folder("jackwizards/animations/player/idle/right"), img_dur=15, loop=True),
            "idle/down": Animation(load_tpng_folder("jackwizards/animations/player/idle/down"), img_dur=15, loop=True),

            # roll
            "roll/up": Animation(load_tpng_folder("jackwizards/animations/player/roll/up"), img_dur=6, loop=False),
            "roll/left": Animation(load_tpng_folder("jackwizards/animations/player/roll/left"), img_dur=6, loop=False),
            "roll/right": Animation(load_tpng_folder("jackwizards/animations/player/roll/right"), img_dur=6, loop=False),
            "roll/down": Animation(load_tpng_folder("jackwizards/animations/player/roll/down"), img_dur=6, loop=False),

            # swim
            "swim/up": Animation(load_tpng_folder("jackwizards/animations/player/swim/up"), img_dur=15, loop=True),
            "swim/left": Animation(load_tpng_folder("jackwizards/animations/player/swim/left"), img_dur=15, loop=True),
            "swim/right": Animation(load_tpng_folder("jackwizards/animations/player/swim/right"), img_dur=15, loop=True),
            "swim/down": Animation(load_tpng_folder("jackwizards/animations/player/swim/down"), img_dur=15, loop=True),

            # walk
            "walk/up": Animation(load_tpng_folder("jackwizards/animations/player/walk/up"), img_dur=15, loop=True),
            "walk/left": Animation(load_tpng_folder("jackwizards/animations/player/walk/left"), img_dur=15, loop=True),
            "walk/right": Animation(load_tpng_folder("jackwizards/animations/player/walk/right"), img_dur=15, loop=True),
            "walk/down": Animation(load_tpng_folder("jackwizards/animations/player/walk/down"), img_dur=15, loop=True),
        }

    def update(self):
        # todo: check if we took damage



        if self.animation_locked:
            # check if our animation is completed
            if self.animations[self.action + "/" + self.facing].done:
                self.animation_locked = False

        if not self.animation_locked:

            self.action = "idle"

            self.velocity = Vector2(0, 0)

            if self.game.pressed[pygame.K_RIGHT]:
                self.facing = "right"
                self.action = "walk"
                self.velocity.x = 1

            if self.game.pressed[pygame.K_LEFT]:
                self.facing = "left"
                self.action = "walk"
                self.velocity.x = -1

            if self.game.pressed[pygame.K_UP]:
                self.facing = "up"
                self.action = "walk"
                self.velocity.y = -1

            if self.game.pressed[pygame.K_DOWN]:
                self.facing = "down"
                self.action = "walk"
                self.velocity.y = 1

            # just pressed
            if pygame.K_SPACE in self.game.just_pressed:

                self.action = "roll"
                self.animation_locked = True

        self.center += self.velocity

        self.center.x = max(16, min(self.center.x, 320-16))
        self.center.y = max(16, min(self.center.y, 180-16))


        self.animations[self.action + "/" + self.facing].update()

    def draw(self):
        # get the current animation frame
        img = self.animations[self.action + "/" + self.facing].img()

        # draw the frame centered on the current position
        self.frame.blit(img, (self.center.x - img.get_width() // 2, self.center.y - img.get_height() // 2))





class Monster(Entity):
    def __init__(self, center=(0, 0), hitbox=(0, 0), scene: Scene = None):
        super().__init__(center=center, hitbox=hitbox)
