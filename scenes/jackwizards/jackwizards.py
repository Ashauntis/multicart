from email.mime import base
from turtle import right
import pygame
from scene import Scene
from utils import SpriteSheet, Animation, load_tpng_folder
from random import choice

class JackWizards(Scene):
    def __init__(self, game):
        super().__init__(game)

        # make the frame surface to draw each frame on
        self.frame = pygame.Surface((320, 180))

        # make a surface to keep the room on so we don't have to redraw it
        self.room = pygame.Surface((320, 180))

        # last room we were in for transition
        self.old_room = pygame.Surface((320, 180))


        # load the tileset and dice it into 16x16 tiles
        self.sheets = {
            "tileset": SpriteSheet("jackwizards/tileset.png"),
            "fireball": SpriteSheet("jackwizards/tileset.png"),
        }

        # load our assets
        self.assets = {
            "idle": Animation(load_tpng_folder("jackwizards/animations/idle"), img_dur=15, loop=True),
            "torch_top": Animation(load_tpng_folder("jackwizards/animations/torch_top"), img_dur=5, loop=True),
            "torch_side": Animation(load_tpng_folder("jackwizards/animations/torch_side"), img_dur=5, loop=True),

        }

        self.tiles = self.sheets["tileset"].dice(16, 16)
        # self.sheets["tileset"].dice_to_folder(16, 16, "tileset")

        self.make_room(True, True, True, True)

        self.transition = 0
        self.transition_duration = 35
        self.transition_direction = None
        self.torches_top = [(80,15), (240,15)]
        self.torches_left_side = [(16, 180*.25), (16, 180*.75)]
        self.torches_right_side = [(320-32, 180*.25), (320-32, 180*.75)]

    def make_room(self, hallway_north: bool = False, hallway_south: bool = False, hallway_east: bool = False, hallway_west: bool = False):
        # wipe the prior room
        self.room.fill((0, 0, 0))

        tilemap = [
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [0 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ,  5],
            [0 , 11, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 14,  5],
            [0 , 21, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 24,  5],
            [0 , 21, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 24,  5],
            [0 , 21, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 24,  5],
            [0 , 21, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 24,  5],
            [0 , 21, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 24,  5],
            [0 , 21, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 24,  5],
            [0 , 31, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 34,  5],
            [40, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 44, 45],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        ]

        floor_spice       = [22, 23, 38, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37]
        left_wall_spice   = [21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 36]
        right_wall_spice  = [24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 39]
        bottom_wall_spice = [32, 32, 32, 32, 32, 32, 32, 32, 33, 47, 48]

        # draw the hallways
        if hallway_north:
            tilemap[0][9] = 37
            tilemap[0][10] = 37
            tilemap[0][11] = 37
            tilemap[1][9] = 37
            tilemap[1][10] = 37
            tilemap[1][11] = 37
            tilemap[2][9] = 37
            tilemap[2][10] = 37
            tilemap[2][11] = 37

        if hallway_south:
            tilemap[9][9] = 37
            tilemap[9][10] = 37
            tilemap[9][11] = 37
            tilemap[10][9] = 37
            tilemap[10][10] = 37
            tilemap[10][11] = 37
            tilemap[11][9] = 37
            tilemap[11][10] = 37
            tilemap[11][11] = 37

        if hallway_east:
            tilemap[5][18] = 37
            tilemap[5][19] = 37
            tilemap[6][18] = 37
            tilemap[6][19] = 37

        if hallway_west:
            tilemap[5][0] = 37
            tilemap[5][1] = 37
            tilemap[6][0] = 37
            tilemap[6][1] = 37

        # randomly spice up some of the basic floor tiles
        for y, row in enumerate(tilemap):
            for x, tile in enumerate(row):
                if tile == 37:
                    tilemap[y][x] = choice(floor_spice)
                if tile == 21:
                    tilemap[y][x] = choice(left_wall_spice)
                if tile == 24:
                    tilemap[y][x] = choice(right_wall_spice)
                if tile == 32:
                    tilemap[y][x] = choice(bottom_wall_spice)

        # render out the room to the room surface
        for y, row in enumerate(tilemap):
            for x, tile in enumerate(row):
                self.room.blit(self.tiles[tile], (x * 16, y * 16))


    def update(self):
        # if the user presses escape or F5 key, quit the event loop.
        if pygame.K_ESCAPE in self.game.just_pressed:
            self.game.scene_push = "Menu"


        # leave if we are in a transition
        if self.transition > 0:
            return

        self.assets["idle"].update()
        self.assets["torch_top"].update()
        self.assets["torch_side"].update()

        if (pygame.K_UP in self.game.just_pressed) or (pygame.K_DOWN in self.game.just_pressed) or (pygame.K_LEFT in self.game.just_pressed) or (pygame.K_RIGHT in self.game.just_pressed):

            self.transition = self.transition_duration
            self.old_room.blit(self.room, (0, 0))
            self.make_room(True, True, True, True)

            if pygame.K_RIGHT in self.game.just_pressed:
                self.transition_direction = "EAST"
            if pygame.K_LEFT in self.game.just_pressed:
                self.transition_direction = "WEST"
            if pygame.K_UP in self.game.just_pressed:
                self.transition_direction = "NORTH"
            if pygame.K_DOWN in self.game.just_pressed:
                self.transition_direction = "SOUTH"


        if pygame.K_RETURN in self.game.just_pressed:

            self.make_room(choice([True, False]), choice([True, False]), choice([True, False]), choice([True, False]))

    def draw_transition(self):
            # the east/west transitions are easier as we can just slide the room over
            if self.transition_direction in ["EAST", "WEST"]:
                step = self.transition_duration - self.transition
                progress = step / self.transition_duration


                if self.transition_direction == "EAST":
                    self.frame.blit(self.old_room, (int(-320 * progress), 0))
                    self.frame.blit(self.room, (int(320 - (320 * progress)), 0))
                if self.transition_direction == "WEST":
                    self.frame.blit(self.old_room, (int(320 * progress), 0))
                    self.frame.blit(self.room, (int(-320 + (320 * progress)), 0))

            # the north/south transitions are a bit more complicated as the top row
            # of each room is blank, we need to adjust the y position of a room
            # to make it looks like it's sliding in edge to edge without a gap

            if self.transition_direction in ["NORTH", "SOUTH"]:

                step = self.transition_duration - self.transition
                progress = step / self.transition_duration

                if self.transition_direction == "NORTH":
                    self.frame.blit(self.old_room, (0, int(180 * progress)))
                    self.frame.blit(self.room, (0, int(-180 + (180 * progress))))

                if self.transition_direction == "SOUTH":
                    self.frame.blit(self.old_room, (0, int(-180 * progress)))
                    self.frame.blit(self.room, (0, int(180 - (180 * progress))))

            self.transition -= 1

    def draw_standard(self):

        # draw the room to start off
        self.frame.blit(self.room, (0, 0))

        # draw the torches
        for torch_position in self.torches_top:
            self.frame.blit(self.assets["torch_top"].img(), torch_position)

        side_torch_image_this_frame = self.assets["torch_side"].img()
        side_torch_image_this_frame_flipped = pygame.transform.flip(side_torch_image_this_frame, True, False)

        for torch_position in self.torches_left_side:
            self.frame.blit(side_torch_image_this_frame, torch_position)

        for torch_position in self.torches_right_side:
            self.frame.blit(side_torch_image_this_frame_flipped, torch_position)

        # draw our character
        self.frame.blit(self.assets["idle"].img(), (160, 90))


    def draw(self):

        # perform the transition if we are in one
        if self.transition > 0:
            self.draw_transition()
        else:
            self.draw_standard()


        # fill the top 16 pixels black for the ui
        pygame.draw.rect(self.frame, (0, 0, 0), (0, 0, 320, 16))

        # FRAME COMPLETE
        # we finished drawing our frame, lets render it to the screen
        self.screen.blit(
            pygame.transform.scale(self.frame, self.screen.get_size()), (0, 0)
        )
