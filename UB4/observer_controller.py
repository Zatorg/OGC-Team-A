import puzzle
import numpy as np

# Initializers
num_games = 100

#Simulate 2x2 Game
game_grid_2x2 = puzzle.GameGrid(size=2)
game_pointsum_2x2 = 0
for i in range(num_games):
    game_grid_2x2.reset()
    game_2x2, maxpoints_2x2, state_2x2 = game_grid_2x2.state()
    while not state_2x2:
        game_grid_2x2.move(np.random.randint(0, 4))
        game_2x2, maxpoints_2x2, state_2x2 = game_grid_2x2.state()
    game_pointsum_2x2 += maxpoints_2x2
game_grid_2x2.destroy()

# Simulate 3x3 Game
game_grid_3x3 = puzzle.GameGrid(size=3)
game_pointsum_3x3 = 0
for i in range(num_games):
    game_grid_3x3.reset()
    game_3x3, maxpoints_3x3, state_3x3 = game_grid_3x3.state()
    while not state_3x3:
        game_grid_3x3.move(np.random.randint(0, 4))
        game_3x3, maxpoints_3x3, state_3x3 = game_grid_3x3.state()
    game_pointsum_3x3 += maxpoints_3x3
game_grid_3x3.destroy()

# Simulate 4x4 Game
game_grid_4x4 = puzzle.GameGrid(size=4)
game_pointsum_4x4 = 0
for i in range(num_games):
    game_grid_4x4.reset()
    game_4x4, maxpoints_4x4, state_4x4 = game_grid_4x4.state()
    while not state_4x4:
        game_grid_4x4.move(np.random.randint(0, 4))
        game_4x4, maxpoints_4x4, state_4x4 = game_grid_4x4.state()
    game_pointsum_4x4 += maxpoints_4x4
game_grid_4x4.destroy()

print(game_pointsum_2x2 / float(num_games))
print(game_pointsum_3x3 / float(num_games))
print(game_pointsum_4x4 / float(num_games))