import os
import pickle
import visual
import neat
import image
from datetime import datetime
# load the winner
with open('winner-feedforward', 'rb') as f:
    c = pickle.load(f)

print('Loaded genome:')
print(c)
now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
# Load the config file, which is assumed to live in
# the same directory as this script.
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config-feedforward')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)

net = neat.nn.FeedForwardNetwork.create(c, config)
sim = visual.Simulate()

"""node_names = {-1: 'x', -2: 'dx', -3: 'theta', -4: 'dtheta', 0: 'control'}
image.draw_net(config, c, True, node_names=node_names)

image.draw_net(config, c, view=True, node_names=node_names,
                   filename="winner-feedforward.gv")
image.draw_net(config, c, view=True, node_names=node_names,
                   filename="winner-feedforward-enabled.gv", show_disabled=False)
image.draw_net(config, c, view=True, node_names=node_names,
                   filename="winner-feedforward-enabled-pruned.gv", show_disabled=False, prune_unused=True)"""
reward = 0
# Run the given simulation for up to 120 seconds.
while True:
    inputs = sim.observations
    action = net.activate(inputs)
    move = "w"
    if action[0] < 0.5:
        move = "d"
    elif action[0] > 0.5:
        move = "a"
    sim.run(move)

    if not sim.alive:
        break
    reward += sim.reward
print(reward)
now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
