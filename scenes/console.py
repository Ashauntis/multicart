# this file is just for reference, it is not used in the game

import pygame
from scene import Scene
from utils import *
import settings

class Console(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.background = self.make_transparent_surface(self.screen.get_size())
        self.background.fill((0, 0, 0, 200))
        self.history = []
        self.command = ""
        self.active = False

    def update(self):

        self.command += self.game.unicode

        for k in self.game.just_pressed:
        
            # execute the command in the console
            if k == pygame.K_RETURN:
                self.history.append("<<" + self.command)

                # make the basic commands case insensitive
                command_lower = self.command.lower()
                if command_lower == "exit" or command_lower == "quit":
                    self.game.quit = True
                elif command_lower == "clear":
                    self.history = []
                elif command_lower == "help" or command_lower == "?":
                    help_docs = [
                        ">>HELP:",
                        "This is a simple console. It will execute the given",
                        "python unless provided an exact command as follows:",
                        ">>HELP>>COMMAND LIST:",
                        "exit | quit   quit the game",
                        "clear         clear the console",
                        "help | ?      show this help",
                        "debug         toggle debug mode",
                    ]

                    # self.history.append(*help_docs)
                    self.history.extend(help_docs)
                elif command_lower == "debug":
                    settings.DEBUG = not settings.DEBUG
                else:
                    # we didn't match a command, so we'll try to execute the python
                    try:
                        exec(self.command)
                    except Exception as e:
                        self.history.append(f">>Error: {e}")
                        
                self.command = ""
                continue
            
            # delete the last character in the command
            if k == pygame.K_BACKSPACE:
                self.command = self.command[:-1]
                continue
        
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.standard_font_size = 16
        self.standard_stroke = 0
        self.standard_font = "system-ui"
        self.standard_color = (255, 255, 255)
        self.screen.blit(self.standard_text("PyGame Console"), (10, 10))
        self.screen.blit(self.standard_text(self.command), (10, 20))

        # draw the last 5 history elements
        for i, h in enumerate(self.history[-10:]):
            self.screen.blit(self.standard_text(h), (10, 30 + 10 * i))
