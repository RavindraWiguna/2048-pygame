from collections import Counter
import pygame
from game2048 import Game, GameInformation
import os
import neat
from neatUtils import visualize
from numpy import argmax
import time
import pickle

'''
A Class of a single Pong Game
'''
class Game2048:
    MOVE_DICT = ("U", "D", "L", "R")
    def __init__(self, window, width, height, fps) -> None:
        self.game = Game(window, width, height)
        self.FPS = fps

    def test_ai(self, net:neat.nn.FeedForwardNetwork):
        isRunning = True
        clock = pygame.time.Clock()
        while(isRunning):
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    isRunning = False
                    break

            # Computer Movement (input -> ball y, ball vel y, paddle y, paddle-ball x distance)
            comp_out = net.activate(self.game.Matrix)
            comp_move = argmax(comp_out)
            print(self.MOVE_DICT[comp_move])
            self.game.move(self.MOVE_DICT[comp_move])
            # Update the game conditions
            game_info = self.game.loop()
            
            # Draw the game's frame
            self.game.draw()
            pygame.display.update()
            # sleep if needed to keep game running at 60 fps
            clock.tick(self.FPS)
            input("continue?")
        
        pygame.quit()

    def calculate_fitness(self, 
                          genome:neat.DefaultGenome, 
                          game_info:GameInformation,
                          total_wrong_move):
        genome.fitness += game_info.score - (total_wrong_move * 2048)


    def train_ai(self, genome, config, isDraw=False):
        isRunning = True
        max_invalid_move = 1
        isDone = False
        # Create the neural networks
        # net = neat.nn.FeedForwardNetwork.create(genome, config)
        net = neat.nn.RecurrentNetwork.create(genome, config)
        total_wrong_move = 0
        while(isRunning):
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    isRunning = False
                    break

            # Computer Movement (input -> ball y, ball vel y, paddle y, paddle-ball x distance)
            comp_out = net.activate(self.game.Matrix)
            comp_move = argmax(comp_out)
            total_wrong_move += self.game.move(self.MOVE_DICT[comp_move])
            # Update the game conditions
            game_info = self.game.loop()
            
            # Draw the game's frame
            # if(isDraw):
                # self.game.draw()
                # pygame.display.update()
            
            # Check for game termination
            if(total_wrong_move > max_invalid_move or game_info.isGameOver):
                self.calculate_fitness(genome, game_info, total_wrong_move)
                isRunning = False
                isDone = True
                break
        
        # pygame.quit()
        return isDone

def eval_genomes(genomes, config):
    print("training genomes")
    """
    Run each genome to determine the fitness.
    """
    width, height = 640, 480
    # win = pygame.display.set_mode((width, height))
    win = None
    pygame.display.set_caption("2048")
    for genome_id, genome in genomes:
        # print the percentages of this net training progress
        # print(round(i/len(genomes) * 100), end=" ")
        genome.fitness = 0
        the_game = Game2048(win, width, height, 60)
        peaceful_exit = the_game.train_ai(genome, config, True)
        if(not peaceful_exit):
            quit()
        # print(f"finish genome id {genome_id}")
            

def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 300)

    # Save the winner
    with open("best_genome.pickle", "wb") as saver:    
        pickle.dump(winner, saver, pickle.HIGHEST_PROTOCOL)
        print("WINNER IS SAVED on best_genome.pickle")
    
    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))
    
    # Show output of the most fit genome against training data.
    # print('\nOutput:')
    # winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    # node_names = {-1:'A', -2: 'B', 0:'A XOR B'}
    # visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    # To load from last check point (in case the training is stopped syre)
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    # p.run(eval_genomes, 10)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, './neatUtils/config-feedforward')
    # run(config_path)
    # config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
    #                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
    #                     config_path)

    # winner_pickle = open(os.path.join(local_dir, "best_genome.pickle"), "rb")
    # winner = pickle.load(winner_pickle)
    # width, height = 640, 480
    # win = pygame.display.set_mode((width, height))
    # the_game = Game2048(win, width, height, 60)
    
    # net = neat.nn.FeedForwardNetwork.create(winner, config)
    # the_game.test_ai(net)
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-299')
    
    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(100))
    p.run(eval_genomes, 500)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)
