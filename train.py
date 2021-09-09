import multiprocessing
import os
import pickle
# import time
import neat
import game
from datetime import datetime
import image
runs_per_net = 2
simulation_seconds = 60000.0

# Use the NN network phenotype and the discrete actuator force function.


def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    fitnesses = []

    for runs in range(runs_per_net):
        sim = game.Simulate()

        # Run the given simulation for up to num_steps time steps.
        fitness = 0.0
        sim.alive = True
        while sim.time < simulation_seconds:
            inputs = sim.observations
            action = net.activate(inputs)
            move = ""
            if action[0] < 0.5:
                move = "d"
            elif 0.5 < action[0]:
                move = "a"
            sim.run(move)

            if not sim.alive:

                break
            fitness += sim.reward
        fitnesses.append(fitness)

    # The genome's fitness is its worst performance across all runs.
    return min(fitnesses)


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)


def run():
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    config = neat.config.Config(neat.genome.DefaultGenome, neat.reproduction.DefaultReproduction,
                                neat.species.DefaultSpeciesSet, neat.stagnation.DefaultStagnation,
                                config_path)
    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))
    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    # Where the simulation starts
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    winner = pop.run(pe.evaluate)
    # Save the winner.
    with open('winner-feedforward', 'wb') as f:
        pickle.dump(winner, f)

    print(winner)

    """image.plot_stats(stats, ylog=True, view=True, filename="feedforward-fitness.svg")
    image.plot_species(stats, view=True, filename="feedforward-speciation.svg")"""
    """ 
    node_names = {-1: 'x', -2: 'dx', -3: 'theta', -4: 'dtheta', 0: 'control'}
    image.draw_net(config, winner, True, node_names=node_names)

    image.draw_net(config, winner, view=True, filename="winner-feedforward.gv", node_names=node_names)
    image.draw_net(config, winner, view=True, node_names=node_names, 
                   filename="winner-feedforward-enabled.gv", show_disabled=False)
    image.draw_net(config, winner, view=True, node_names=node_names, 
                   filename="winner-feedforward-enabled-pruned.gv", show_disabled=False, prune_unused=True)"""

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)


if __name__ == '__main__':
    run()
