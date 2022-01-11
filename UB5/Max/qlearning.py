import puzzle
import numpy as np
import time
import matplotlib.pyplot as plt

epochs = 10000
eval_interval = 100

game_grid = puzzle.GameGrid(size=2)
alpha = 0.7
epsilon = 0.1
gamma = 0.3
# Use something else as Key, maybe string rep of game
Q_Table = {}
total_points = 0
epoch_points = 0
for epoch in range(epochs):
    game_grid.reset()
    game, points, state = game_grid.state()
    while not state:
        old_game = game
        old_points = points
        old_state = state
        a = 0
        if repr(old_game) in Q_Table:
            a = np.argmax(Q_Table[repr(old_game)])
            if np.random.random() > epsilon:
                game_grid.move(a)
            else:
                action = [0, 1, 2, 3]
                del action[a]
                a = np.random.choice(action)
                game_grid.move(a)
        else:
            Q_Table[repr(old_game)] = [0, 0, 0, 0]
            game_grid.move(np.random.randint(0, 4))
        game, points, state = game_grid.state()
        reward = points - old_points
        if repr(game) not in Q_Table:
            Q_Table[repr(game)] = [0, 0, 0, 0]
        new_Q = Q_Table[repr(old_game)][a] + alpha * (reward + gamma * np.amax(Q_Table[repr(game)]) - Q_Table[repr(old_game)][a])
        Q_Table[repr(old_game)][a] = new_Q
    total_points += points
    epoch_points += points
    game_grid.reset()
    if epoch % eval_interval == 0:
        avg_score = epoch_points / float(eval_interval)
        print(avg_score)
        epoch_points = 0
game_grid.destroy()
print(Q_Table)
avg_score = total_points / float(epochs)
print("Average Score for 2x2 Grid: %.2f" % avg_score)
