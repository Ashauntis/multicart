import pygame
from scene import Scene
from utils import *
from .scripts.qb import Board, colors, Piece, Shapes
import copy

class QuadBlox(Scene):
    def __init__(self, game):
        super().__init__(game)


        self.player_board = Board((100, 10))
        self.player_board.clear()

        self.opponents = [Board() for _ in range(8)]
        self.setup_opponents()

        self.player_piece = Piece()
        self.next_piece = Piece()

        self.drop_at = 60 # frames per line fall
        self.drop_count = 0

        self.held_down_for = 0
        self.held_toggles_at = 12
        self.held_frame_interval = 4
        self.held_left_for = 0
        self.held_right_for = 0

        self.died_at = 0

        self.level = 0

        self.standard_font_size = 20
        self.standard_stroke = False
        


    def setup_opponents(self):
        for opponent in self.opponents:
            # opponent.clear()

            # setup to draw opponent boards
            obs = 6
            opponent.block_size = obs

            x_step = obs * 11

            y1 = 10
            y2 = y1 + 28 * obs

            x = 640 / 2
            y = y1

            for i, opponent in enumerate(self.opponents):

                opponent.pos = (x, y)

                if i % 2 == 0:
                    y = y2
                else:
                    y = y1
                    x += x_step


    def update(self):
        # if the user presses escape or F5 key, quit the event loop.
        if pygame.K_ESCAPE in self.game.just_pressed:
            self.game.scene_push = "Menu"
            return
        
        
        # if we are dead stop the update logic here
        if self.died_at:
            return 
        
        # check if we are already colliding. If we are, place the piece
        if self.player_piece.collides(self.player_board):
            self.place()
            return


        # LEFT / RIGHT MOVEMENT AND ROTATION
        left_held_tick = False
        right_held_tick = False


        # check if left has been held for a while 
        if not self.game.pressed[pygame.K_LEFT]:
            self.held_left_for = 0
        else:
            self.held_left_for += 1

            if self.held_left_for >= self.held_toggles_at:
                numerator = self.held_left_for - self.held_toggles_at
                denominator = self.held_frame_interval

                if numerator % denominator == 0:
                    left_held_tick = True
            
        
        if not self.game.pressed[pygame.K_RIGHT]:
            self.held_right_for = 0
        else:
            self.held_right_for += 1

            if self.held_right_for >= self.held_toggles_at:
                numerator = self.held_right_for - self.held_toggles_at
                denominator = self.held_frame_interval

                if numerator % denominator == 0:
                    right_held_tick = True
            

        sim_piece = copy.deepcopy(self.player_piece)
        if pygame.K_LEFT in self.game.just_pressed or left_held_tick:
            sim_piece.x -= 1

        if pygame.K_RIGHT in self.game.just_pressed or right_held_tick:
            sim_piece.x += 1

        if pygame.K_UP in self.game.just_pressed:
            sim_piece.rotate_and_size()




        # if the sim piece does not collide update our piece to it
        if not sim_piece.collides(self.player_board):
            self.player_piece = sim_piece



        # DOWN MOVEMENT / GRAVITY 
        # should we fall this frame?
        sim_drop = False
    
        # check if down has been held for a while
        if self.game.pressed[pygame.K_DOWN]:
            self.held_down_for += 1
            if self.held_down_for >= self.held_toggles_at:
                numerator = self.held_down_for - self.held_toggles_at
                denominator = self.held_frame_interval

                if numerator % denominator == 0:
                    sim_drop = True
        else:
            self.held_down_for = 0

        # check for key press down
        if pygame.K_DOWN in self.game.just_pressed:
            sim_drop = True

        # check for gravity fall
        self.drop_count += 1
        if self.drop_count >= self.drop_at:
            sim_drop = True
    
                
        # increment drop count and see if we need to drop the piece
        if sim_drop:
            
            # if we are dropping the piece, reset the drop count
            self.drop_count = 0
            drop_sim = copy.deepcopy(self.player_piece)
            drop_sim.y += 1
            if not drop_sim.collides(self.player_board):
                self.player_piece = drop_sim
            else:
                self.place()

        # check for death
        for x in range(10):
            for y in range(4):
                if self.player_board.grid[y][x]:
                    self.died_at = self.elapsed
                    self.player_board.kill()
                    return


    def place(self):
        # place the current piece and get a new piece
        self.player_board.place(self.player_piece)
        self.player_piece = self.next_piece
        self.next_piece = Piece()

    def draw(self):

        # draw the player board
        self.screen.fill((0, 0, 0))
        self.draw_board(self.player_board)

        # draw the player stats
        pos = self.player_board.pos
        bs = self.player_board.block_size

        self.screen.blit(
            self.standard_text( str(self.player_board.points)),
            (pos[0] + bs * 11, pos[1])
        )

        self.screen.blit(
            self.standard_text("CLEARS"),
            (pos[0] + bs * 11, pos[1] + 20)
        )

        for y in range(4):
            self.screen.blit(
                self.standard_text(f"{y + 1}x " + str(self.player_board.clears[y])),
                (pos[0] + bs * 11, pos[1] + 40 + y * 20)
            )



        # draw the opponents boards
        for opponent in self.opponents:
            self.draw_board(opponent)

        # draw our piece
        self.draw_piece()

    def draw_piece(self):
        for x in range(4):
            for y in range(4):
                if self.player_piece.grid[y][x]:
                    pygame.draw.rect(
                        self.screen,
                        colors[self.player_piece.color],
                        (
                            (self.player_piece.x + x) * 12 + 100,
                            (self.player_piece.y + y) * 12 + 10,
                            12 - 1,
                            12 - 1)
                    )

    def draw_board(self, board: Board):
        pos = board.pos
        bs = board.block_size

        # draw a red horizontal line after the first 4 rows
        pygame.draw.line(
            self.screen,
            (255, 0, 0),
            (pos[0], pos[1] + 4 * bs-1),
            (pos[0] + 10 * bs -1, pos[1] + 4 * bs -1)
        )

        # draw the board
        for y, row in enumerate(board.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen,
                        colors[cell],
                        (
                            pos[0] + x * bs,
                            pos[1] + y * bs,
                            bs - 1,
                            bs - 1)
                    )

        # draw a grey border around the board
        border_width = 4
        pygame.draw.rect(
            surface=self.screen,
            color=(128, 128, 128),
            rect=(
                pos[0] - border_width - 1,
                pos[1] - border_width - 1,
                10 * bs + 2 * border_width + 1,
                24 * bs + 2 * border_width + 1
            ),
            width=border_width
        )


