import puzzle
import numpy as np
import time
import matplotlib.pyplot as plt

# Initializers
num_games = 100

#Simulate 2x2 Game
exec_time_2x2 = time.perf_counter()
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
exec_time_2x2 = time.perf_counter() - exec_time_2x2
avg_score_2x2 = game_pointsum_2x2 / float(num_games)
print("2x2 finished in %.5f" % exec_time_2x2)
print("Average Score for 2x2 Grid: %.2f" % avg_score_2x2)

# Simulate 3x3 Game
exec_time_3x3 = time.perf_counter()
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
exec_time_3x3 = time.perf_counter() - exec_time_3x3
avg_score_3x3 = game_pointsum_3x3 / float(num_games)
print("3x3 finished in %.5f" % exec_time_3x3)
print("Average Score for 3x3 Grid: %.2f" % avg_score_3x3)

# Simulate 4x4 Game
exec_time_4x4 = time.perf_counter()
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
exec_time_4x4 = time.perf_counter() - exec_time_4x4
avg_score_4x4 = game_pointsum_4x4 / float(num_games)
print("4x4 finished in %.5f" % exec_time_4x4)
print("Average Score for 4x4 Grid: %.2f" % avg_score_4x4)

# Plot Figure
plt.rcdefaults()
fig, ax = plt.subplots()
game_sizes = ("2x2", "3x3", "4x4")
avg_scores = [avg_score_2x2, avg_score_3x3, avg_score_4x4]
y_pos = np.arange(len(game_sizes))
ax.barh(y_pos, avg_scores)
ax.set_yticks(y_pos, labels=game_sizes)
ax.invert_yaxis()
ax.set_xlabel('Average Score')
ax.set_title('Average Score for random 2048 Games')
plt.show()
