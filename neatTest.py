import multiprocessing
import os
import pickle

import neat
import Main


runs_per_net = 2
simulation_seconds = 60.0


# Use the NN network phenotype and the discrete actuator force function.
def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    fitnesses = []

    for runs in range(runs_per_net):
        sim = Main.simulate()

        # Run the given simulation for up to num_steps time steps.
        fitness = 0.0
        while sim.time < simulation_seconds:
            inputs = sim.observations
            action = net.activate(inputs)

            # Apply action to the simulated cart-pole
            print(action)
            force = cart_pole.discrete_actuator_force(action)
            sim.run(force)

            # Stop if the network fails to keep the cart within the position or angle limits.
            # The per-run fitness is the number of time steps the network can balance the pole
            # without exceeding these limits.
            if not sim.alive:
                break

            fitness = sim.time

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
    config = neat.config.Config(neat.config.DefaultGenome, neat.config.DefaultReproduction,
                             neat.config.DefaultSpeciesSet, neat.config.DefaultStagnation,
                             config_path)

    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))

    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = pop.run(pe.evaluate)

    # Save the winner.
    with open('winner-feedforward', 'wb') as f:
        pickle.dump(winner, f)

    print(winner)


if __name__ == '__main__':
    run()
