from copy import deepcopy
import pygame
from colorData import WHITE, GRAY
from random import choice
from math import sqrt
#=========================================SETUP PHASE=====================
# Initialize pygame
pygame.init()

class GameInformation:
    def __init__(self):
        pass

class Game:
    # Game setup
    SCORE_FONT = pygame.font.SysFont('comicsans', 50)
    
    def __init__(self, window, window_width, window_height) -> None:
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        self.unit_w =self.window_width//4
        self.unit_h = self.window_height//4
        self.Matrix = [0, 0, 0, 0, 
                       2, 2, 0, 0,
                       2, 0, 0, 0,
                       0, 0, 0, 0]
        self.is_pressed = False                 # For human player, so that it only move after not is pressed
        self.last_move = None                   # also for human player to check if we release the last button
        self.empty_tile = []                    # store all 0 in the matrix to spawn random '2' or '4'
        self.done_move =False                   # safe guard so that we didn't spawn before moving

    def up(self):
        isUpdating = True
        everCombine = False
        while(isUpdating):
            last_state = deepcopy(self.Matrix)
            for col in range(4):
                for row in range(1, 4):
                    cur_id = row*4 + col
                    up_id = cur_id-4
                    if(self.Matrix[up_id] == 0 or self.Matrix[up_id] == self.Matrix[cur_id]):
                        # bisa naik ke atas
                        everCombine = everCombine or self.Matrix[up_id] == self.Matrix[cur_id]
                        self.Matrix[up_id] += self.Matrix[cur_id]
                        self.Matrix[cur_id] = 0
            if(self.Matrix == last_state):
                isUpdating = False
    
    def down(self):
        isUpdating = True
        while(isUpdating):
            last_state = deepcopy(self.Matrix)
            for col in range(4):
                for row in range(2, -1, -1):
                    cur_id = row*4 + col
                    down_id = cur_id+4
                    if(self.Matrix[down_id] == 0 or self.Matrix[down_id] == self.Matrix[cur_id]):
                        # bisa naik ke atas
                        self.Matrix[down_id] += self.Matrix[cur_id]
                        self.Matrix[cur_id] = 0
            if(self.Matrix == last_state):
                isUpdating = False

    def left(self):
        isUpdating = True
        while(isUpdating):
            last_state = deepcopy(self.Matrix)
            for row in range(4):
                for col in range(1, 4):
                    cur_id = row*4 + col
                    left_id = cur_id-1
                    if(self.Matrix[left_id] == 0 or self.Matrix[left_id] == self.Matrix[cur_id]):
                        # bisa naik ke atas
                        self.Matrix[left_id] += self.Matrix[cur_id]
                        self.Matrix[cur_id] = 0
            if(self.Matrix == last_state):
                isUpdating = False

    def right(self):
        isUpdating = True
        while(isUpdating):
            last_state = deepcopy(self.Matrix)
            for row in range(4):
                for col in range(2, -1, -1):
                    cur_id = row*4 + col
                    right_id = cur_id+1
                    if(self.Matrix[right_id] == 0 or self.Matrix[right_id] == self.Matrix[cur_id]):
                        # bisa naik ke atas
                        self.Matrix[right_id] += self.Matrix[cur_id]
                        self.Matrix[cur_id] = 0
            if(self.Matrix == last_state):
                isUpdating = False

    def move(self, direction):
        if(direction=="U"):
            self.up()
            self.done_move = True
        elif(direction=="D"):
            self.down()
            self.done_move = True
        elif(direction=='L'):
            self.left()
            self.done_move = True
        elif(direction=="R"):
            self.right()
            self.done_move = True


    def draw_board(self):
        for i in range(4):
            for j in range(4):
                value_text = self.SCORE_FONT.render(f'{self.Matrix[i*4 + j]}', 1, WHITE)
                self.window.blit(value_text, (self.unit_w*j + self.unit_w//2 - value_text.get_width()//2, self.unit_h*i + self.unit_h//2 - value_text.get_height()//2))
                # self.window.blit(left_score_text,(self.window_width//4 - left_score_text.get_width()//2, 20))
        
    def draw(self):
        # Fill the background color
        self.window.fill(GRAY)
        self.draw_board()
        # pygame.display.update()         # Update the frame showed

    def get_empty_tile(self):
        self.empty_tile = [i for i, val in enumerate(self.Matrix) if val == 0]


    def loop(self):
        """
        Executes a single game loop.
        :returns: GameInformation instance
        """
        game_info = GameInformation()

        if(self.done_move):
            # get empty tile
            self.get_empty_tile()
            # spawn random tile
            r_id = choice(self.empty_tile)
            self.Matrix[r_id] = choice((2, 2, 4, 2, 2))
            self.done_move = False
        return game_info

    def reset(self):
        """Resets the entire game."""

if __name__=="__main__":
    isRunning = True
    width, height = 640, 480
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("2048")
    the_game = Game(window, width, height)
    clock = pygame.time.Clock()
    while(isRunning):
        clock.tick(60)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                isRunning = False
                break
        
        keys = pygame.key.get_pressed()
        if(not the_game.is_pressed):
            if(keys[pygame.K_UP]):
                the_game.is_pressed=True
                the_game.move("U")
                the_game.last_move = pygame.K_UP
            elif(keys[pygame.K_DOWN]):
                the_game.is_pressed=True
                the_game.move("D")
                the_game.last_move = pygame.K_DOWN
            elif(keys[pygame.K_LEFT]):
                the_game.is_pressed=True
                the_game.move("L")
                the_game.last_move = pygame.K_LEFT
            elif(keys[pygame.K_RIGHT]):
                the_game.is_pressed=True
                the_game.move("R")
                the_game.last_move = pygame.K_RIGHT
        else:
            # is pressed
            if(not keys[the_game.last_move]):
                the_game.is_pressed = False
        
        the_game.loop()
        the_game.draw()
        pygame.display.update()

    
    pygame.quit()