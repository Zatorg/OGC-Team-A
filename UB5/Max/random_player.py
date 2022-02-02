import puzzle
import numpy as np


def random_player_game(game_size, epochs, eval_interval):
    game_grid = puzzle.GameGrid(size=game_size)
    avg_score_history = []
    last_100_history = []
    total_points = 0
    interval_points = 0

    for epoch in range(epochs):
        # Play the Game
        game_grid.reset()
        game, points, state = game_grid.state()
        while not state:
            game_grid.move(np.random.randint(0, 4))
            game, points, state = game_grid.state()

        # Build histogram
        if len(last_100_history) >= 100:
            last_100_history.pop(0)
        last_100_history.append(points)
        avg_score_history.append(np.mean(last_100_history))

        # Evaluate
        total_points += points
        interval_points += points
        if epoch % eval_interval == 0 and epoch != 0:
            avg_score = interval_points / float(eval_interval)
            print("=====================================")
            print("Epoch: %s" % epoch)
            print("Average Score (last 100): %.2f" % avg_score)
            interval_points = 0
        game_grid.reset()
    game_grid.destroy()

    print("=====================================")
    avg_score = total_points / float(epochs)
    print("Average Score (overall): %.2f" % avg_score)
    return np.array(avg_score_history)
