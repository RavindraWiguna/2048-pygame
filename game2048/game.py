from collections import Counter
from copy import deepcopy
import numpy as np
import pygame
from .colorData import *
from random import choice
from math import sqrt
#=========================================SETUP PHASE=====================
# Initialize pygame
pygame.init()

class GameInformation:
    def __init__(self, matrix, isGameOver, score):
        self.Matrix = matrix
        self.isGameOver = isGameOver
        self.score = score
        

class Game:
    # Game setup
    SCORE_FONT = pygame.font.SysFont('comicsans', 50)
    GAME_COL = COLORS
    
    def __init__(self, window, window_width, window_height) -> None:
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        self.unit_w =self.window_width//4
        self.unit_h = self.window_height//4
        self.Matrix = [0, 0, 0, 0, 
                       0, 0, 0, 0,
                       2, 0, 0, 0,
                       2, 0, 0, 0]
        self.is_pressed = False                 # For human player, so that it only move after not is pressed
        self.last_move = None                   # also for human player to check if we release the last button
        self.empty_tile = []                    # store all 0 in the matrix to spawn random '2' or '4'
        self.done_move =False                   # safe guard so that we didn't spawn before moving
        self.redraw = True
        self.score = 0

    def up(self):
        availableForCombine = Counter()         # store id of the matrix where that id's value is the result of combining 2 similar value
        for col in range(4):
            change = 1                          # initialize the change as 1 so that the loop get executed at least once
            while(change > 0):
                change = 0
                for row in range(1, 4):
                    cur_id = row*4 + col
                    if(self.Matrix[cur_id] == 0):
                        # skip empty tile
                        continue
                    
                    up_id = cur_id-4
                    if(self.Matrix[up_id] == 0):
                        # bisa naik ke atas
                        self.Matrix[up_id] += self.Matrix[cur_id]
                        self.Matrix[cur_id] = 0
                        change +=1
                    elif(self.Matrix[up_id] == self.Matrix[cur_id] and availableForCombine[up_id]==0 and availableForCombine[cur_id] == 0):
                        # kalau tidak 0 dan sama dan bisa di combine
                        change +=1
                        self.Matrix[up_id] += self.Matrix[cur_id]
                        self.Matrix[cur_id] = 0
                        availableForCombine[up_id] = 1 # 1 means not available (yea not so intuitive but there exist a thing called comment and reading)
                        self.score+=self.Matrix[up_id]    

    def down(self):
        availableForCombine = Counter()         # store id of the matrix where that id's value is the result of combining 2 similar value
        for col in range(4):
            change = 1                          # initialize the change as 1 so that the loop get executed at least once
            while(change > 0):
                change = 0
                for row in range(2, -1, -1):
                    cur_id = row*4 + col
                    if(self.Matrix[cur_id] == 0):
                        # skip empty tile
                        continue
                    
                    down_id = cur_id+4
                    if(self.Matrix[down_id] == 0):
                        # bisa ke bawah
                        self.Matrix[down_id] += self.Matrix[cur_id]
                        self.Matrix[cur_id] = 0
                        change +=1
                    elif(self.Matrix[down_id] == self.Matrix[cur_id] and availableForCombine[down_id]==0 and availableForCombine[cur_id] == 0):
                        # kalau tidak 0 dan sama dan bisa di combine
                        change +=1
                        self.Matrix[down_id] += self.Matrix[cur_id]
                        self.Matrix[cur_id] = 0
                        availableForCombine[down_id] = 1 # 1 means not available (yea not so intuitive but there exist a thing called comment and reading)
                        self.score+=self.Matrix[down_id]

    def left(self):
        availableForCombine = Counter()         # store id of the matrix where that id's value is the result of combining 2 similar value
        for row in range(4):
            change = 1                          # initialize the change as 1 so that the loop get executed at least once
            while(change > 0):
                change = 0
                for col in range(1, 4):
                    cur_id = row*4 + col
                    if(self.Matrix[cur_id] == 0):
                        # skip empty tile
                        continue
                    
                    left_id = cur_id-1
                    if(self.Matrix[left_id] == 0):
                        # bisa ke kiri
                        self.Matrix[left_id] += self.Matrix[cur_id]
                        self.Matrix[cur_id] = 0
                        change +=1
                    elif(self.Matrix[left_id] == self.Matrix[cur_id] and availableForCombine[left_id]==0 and availableForCombine[cur_id] == 0):
                        # kalau tidak 0 dan sama dan bisa di combine
                        change +=1
                        self.Matrix[left_id] += self.Matrix[cur_id]
                        self.Matrix[cur_id] = 0
                        availableForCombine[left_id] = 1 # 1 means not available (yea not so intuitive but there exist a thing called comment and reading)
                        self.score+=self.Matrix[left_id]

    def right(self):
        availableForCombine = Counter()         # store id of the matrix where that id's value is the result of combining 2 similar value
        for row in range(4):
            change = 1                          # initialize the change as 1 so that the loop get executed at least once
            while(change > 0):
                change = 0
                for col in range(2, -1, -1):
                    cur_id = row*4 + col
                    if(self.Matrix[cur_id] == 0):
                        # skip empty tile
                        continue
                    
                    right_id = cur_id+1
                    if(self.Matrix[right_id] == 0):
                        # bisa ke kanan
                        self.Matrix[right_id] += self.Matrix[cur_id]
                        self.Matrix[cur_id] = 0
                        change +=1
                    elif(self.Matrix[right_id] == self.Matrix[cur_id] and availableForCombine[right_id]==0 and availableForCombine[cur_id] == 0):
                        # kalau tidak 0 dan sama dan bisa di combine
                        change +=1
                        self.Matrix[right_id] += self.Matrix[cur_id]
                        self.Matrix[cur_id] = 0
                        availableForCombine[right_id] = 1 # 1 means not available (yea not so intuitive but there exist a thing called comment and reading)
                        self.score+=self.Matrix[right_id]

    # will update the matrix, boolean indicating a move has been done and the score
    def move(self, direction):
        last_state = deepcopy(self.Matrix)
        if(direction=="U"):
            self.up()
        elif(direction=="D"):
            self.down()
        elif(direction=='L'):
            self.left()
        elif(direction=="R"):
            self.right()
        
        if(self.Matrix == last_state):
            self.done_move= False
            return 1 # for training NN, false move is punished
        else:
            self.done_move = True
            self.redraw = True
            return 0 # correct so dont punish



    def draw_board(self):
        for i in range(4):
            for j in range(4):
                cur_id = i*4 + j
                value_int = self.Matrix[cur_id]
                value_text = self.SCORE_FONT.render(f'{value_int}', 1, BLACK)
                pygame.draw.rect(self.window, self.GAME_COL[value_int], (self.unit_w*j, self.unit_h*i, self.unit_w, self.unit_h))
                self.window.blit(value_text, (self.unit_w*j + self.unit_w//2 - value_text.get_width()//2, self.unit_h*i + self.unit_h//2 - value_text.get_height()//2))
                
                # self.window.blit(left_score_text,(self.window_width//4 - left_score_text.get_width()//2, 20))
        
    def draw(self):
        # Fill the background color
        if(self.redraw):
            # print("redraw")
            self.window.fill(BG)
            self.draw_board()
            self.redraw = False
        # pygame.display.update()         # Update the frame showed

    def get_empty_tile(self):
        self.empty_tile = [i for i, val in enumerate(self.Matrix) if val == 0]


    # check for game over (no empty tiles and not a single combine is possible)
    def check_game_over(self):
        # Update the empty tiles
        self.get_empty_tile()
        # if exist at least one zero, then it aint the end of world
        if(self.empty_tile):
            return False
        
        # hm, so there is not empty tile..., let's check for combine-es (only the first 3 row and col needed to checked)
        maybeGameOver = True
        for row in range(3):
            if(maybeGameOver):
                for col in range(3):
                    # check horizontal equalness
                    cur_id = row * 4 + col
                    if(self.Matrix[cur_id] == self.Matrix[cur_id+1]):
                        maybeGameOver = False
                        break
                    elif(self.Matrix[cur_id] == self.Matrix[cur_id+4]):
                        maybeGameOver=False
                        break
        # check last row
        row = 3
        for col in range(3):
            cur_id = row * 4 + col
            if(self.Matrix[cur_id] == self.Matrix[cur_id+1]):
                maybeGameOver = False
                break
        # check last col
        col = 3
        for row in range(3):
            cur_id = row * 4 + col
            if(self.Matrix[cur_id] == self.Matrix[cur_id+4]):
                maybeGameOver = False
                break
        return maybeGameOver

    def loop(self):
        """
        Executes a single game loop.
        :returns: GameInformation instance
        """
        # check for game overness
        gameOver = self.check_game_over()

        # if a move has been done then we spawn
        if(self.done_move):
            if(self.empty_tile):
                # print("spawn")
                # spawn random tile
                r_id = choice(self.empty_tile)
                self.Matrix[r_id] = choice((2, 2, 2, 2, 2, 4, 2, 2, 2, 2))
                self.done_move = False
                self.redraw = True
        
        game_info = GameInformation(self.Matrix, gameOver, self.score)
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
    game_info = None
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
                print(game_info.score)
                the_game.is_pressed = False
        
        game_info = the_game.loop()
        isRunning = isRunning and not game_info.isGameOver
        the_game.draw()
        pygame.display.update()

    
    input("type anything to quit")
    pygame.quit()