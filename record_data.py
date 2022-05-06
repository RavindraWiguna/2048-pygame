import datetime
import pickle
import pygame
from game2048 import Game
import pandas as pd
import numpy as np

def main():
    isRunning = True
    width, height = 640, 480
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("2048")
    the_game = Game(window, width, height)
    clock = pygame.time.Clock()
    game_info = None
    isWrong = True
    beforeMoveMatrix = None
    gameRecord = None
    moveUpRecord = []
    moveDownRecord = []
    moveLeftRecord = []
    moveRightRecord = []
    curMove = None
    while(isRunning):
        isWrong = True
        clock.tick(60)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                isRunning = False
                break
        keys = pygame.key.get_pressed()
        if(not the_game.is_pressed):
            if(keys[pygame.K_UP]):
                the_game.is_pressed=True
                isWrong = the_game.move("U")
                the_game.last_move = pygame.K_UP
                curMove = "U"
            elif(keys[pygame.K_DOWN]):
                the_game.is_pressed=True
                isWrong = the_game.move("D")
                the_game.last_move = pygame.K_DOWN
                curMove = "D"
            elif(keys[pygame.K_LEFT]):
                the_game.is_pressed=True
                isWrong = the_game.move("L")
                the_game.last_move = pygame.K_LEFT
                curMove = "L"
            elif(keys[pygame.K_RIGHT]):
                the_game.is_pressed=True
                isWrong = the_game.move("R")
                the_game.last_move = pygame.K_RIGHT
                curMove = "R"
        else:
            # is pressed
            if(not keys[the_game.last_move]):
                # print(game_info.score)
                the_game.is_pressed = False
        
        # record the datah befure updating
        if(not isWrong):
            if type(gameRecord) == type(None):
                gameRecord = np.array([the_game.Matrix], dtype=np.uint16)
            else:
                gameRecord = np.concatenate((gameRecord, [the_game.Matrix]), axis=0)
            
            # Record the move of this state
            moveDownRecord.append((curMove=="D")*1)
            moveUpRecord.append((curMove=="U")*1)
            moveRightRecord.append((curMove=="R")*1)
            moveLeftRecord.append((curMove=="L")*1)
            # print(moveDownRecord)
            # print(moveUpRecord)
            # print(moveRightRecord)
            # print(moveLeftRecord)
            # print(gameRecord)
            # print(type(gameRecord))
        game_info = the_game.loop()
        isRunning = isRunning and not game_info.isGameOver
        the_game.draw()
        pygame.display.update()

    
    input("type anything to quit")
    pygame.quit()
    # Save it to pandas
    df = pd.DataFrame(gameRecord, columns = [i for i in range(16)])
    df['Up'] = moveUpRecord
    df['Down'] = moveDownRecord
    df['Left'] = moveLeftRecord
    df['Right'] = moveRightRecord

    print(df)
    curDate = datetime.datetime.now().strftime("%y_%m_%d_%H%M%S")
    df.to_csv(f'game_record_{curDate}.csv')

if __name__=="__main__":
    main()