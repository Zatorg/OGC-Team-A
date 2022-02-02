import puzzle
import numpy as np


def game_to_string(game):
    return ','.join(str(item) for innerlist in game for item in innerlist)


def is_game_in_table(game, table):
    flip_game = np.fliplr(game)
    if game_to_string(game) in table:
        return True, False, 0, game
    elif game_to_string(flip_game) in table:
        return True, True, 0, flip_game
    game = np.rot90(game)
    flip_game = np.rot90(flip_game)
    if game_to_string(game) in table:
        return True, False, 1, game
    elif game_to_string(flip_game) in table:
        return True, True, 1, flip_game
    game = np.rot90(game)
    flip_game = np.rot90(flip_game)
    if game_to_string(game) in table:
        return True, False, 2, game
    elif game_to_string(flip_game) in table:
        return True, True, 2, flip_game
    game = np.rot90(game)
    flip_game = np.rot90(flip_game)
    if game_to_string(game) in table:
        return True, False, 3, game
    elif game_to_string(flip_game) in table:
        return True, True, 3, flip_game
    return False, False, 0, game


def adjust_action(a, flip, turns):
    action = a
    if flip:
        for i in range(turns):
            action = (action + 1) % 4
        if action == 1 or action == 3:
            action = (action + 2) % 4
    else:
        for i in range(turns):
            action = (action + 1) % 4
    return action


def reverse_adjust_action(a, flip, turns):
    action = a
    if flip:
        if action == 1 or action == 3:
            action = (action - 2) % 4
        for i in range(turns):
            action = (action - 1) % 4
    else:
        for i in range(turns):
            action = (action - 1) % 4
    return action


def q_learn_game(grid_size, epochs, eval_interval, alpha, alpha_decay,
                 alpha_decay_interval, epsilon, epsilon_decay, epsilon_decay_interval, gamma):
    avg_score_history = []
    last_100_avg_score_history = []
    table_decision_history = []
    last_100_table_decision_history = []
    game_grid = puzzle.GameGrid(size=grid_size)
    q_table = {}
    total_points = 0
    interval_points = 0

    for epoch in range(epochs):
        # Play the Game
        game_grid.reset()
        game, points, state = game_grid.state()
        decision_with_table = 0
        decision_total = 0
        while not state:
            old_game = game
            old_points = points
            decision_total += 1
            a = np.random.randint(0, 4)
            is_in_table, flip, turns, old_game = is_game_in_table(old_game, q_table)
            if is_in_table:
                a = np.argmax(q_table[game_to_string(old_game)])
                a = adjust_action(a, flip, turns)
                if np.random.random() > epsilon:
                    decision_with_table += 1
                    game_grid.move(a)
                else:
                    action = [0, 1, 2, 3]
                    del action[a]
                    a = np.random.choice(action)
                    game_grid.move(a)
            else:
                q_table[game_to_string(old_game)] = [0, 0, 0, 0]
                game_grid.move(a)
            game, points, state = game_grid.state()
            reward = points - old_points
            is_in_table, flip_2, turns_2, game = is_game_in_table(game, q_table)
            if not is_in_table:
                q_table[game_to_string(game)] = [0, 0, 0, 0]
            a = reverse_adjust_action(a, flip, turns)
            new_q = q_table[game_to_string(old_game)][a] + alpha * (reward + gamma * np.amax(q_table[game_to_string(game)]) - q_table[game_to_string(old_game)][a])
            q_table[game_to_string(old_game)][a] = new_q

        # Build histograms
        if len(last_100_avg_score_history) >= 100:
            last_100_avg_score_history.pop(0)
        last_100_avg_score_history.append(points)
        if len(last_100_table_decision_history) >= 100:
            last_100_table_decision_history.pop(0)
        last_100_table_decision_history.append(decision_with_table / float(decision_total))
        table_decision_history.append(np.mean(last_100_table_decision_history))
        avg_score_history.append(np.mean(last_100_avg_score_history))

        # Evaluate
        total_points += points
        interval_points += points
        if epoch % alpha_decay_interval == 0 and epoch != 0:
            alpha = alpha * alpha_decay
        if epoch % epsilon_decay_interval == 0 and epoch != 0:
            epsilon = epsilon * epsilon_decay
        if epoch % eval_interval == 0 and epoch != 0:
            avg_score = interval_points / float(eval_interval)
            print("=====================================")
            print("Epoch: %s" % epoch)
            print("Average Score (last 100): %.2f" % avg_score)
            print("Epsilon: %.10f" % epsilon)
            print("Alpha: %.10f" % alpha)
            interval_points = 0

        game_grid.reset()
    game_grid.destroy()

    print("=====================================")
    print("Q_Table Size: %s" % len(q_table))
    print(q_table)
    print("=====================================")
    avg_score = total_points / float(epochs)
    print("Average Score (overall): %.2f" % avg_score)
    return np.array(avg_score_history), np.array(table_decision_history), q_table
