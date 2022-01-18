from puzzle import GameGrid
from player import Player
import random
import sys
import matplotlib.pyplot as plt


def str_repr(state_matrix):
    s = ""
    for row in state_matrix:
        s += ",".join(str(x) for x in row) + ";"
    return s


def mirror(mat, axis):
    if axis == 0:
        return [mat[-i] for i in range(1, len(mat) + 1)]
    else:
        new = []
        for row in mat:
            new.append(row[::-1])
        return new


def rotate(mat, deg):
    for _ in range(deg):
        mat = [[mat[j][i] for j in range(len(mat))]
               for i in range(len(mat[0]) - 1, -1, -1)]
    return mat


def permute_action_index(action_index, transformation, param):
    if transformation == rotate:
        action_index = (action_index+param) % 4
    elif transformation == mirror:
        if param == action_index % 2:
            action_index = (action_index + 2) % 4

    return action_index


transformations = [[mirror, [0, 1]], [rotate, [0, 1, 2, 3]]]

def get_equivalences(matrix):
    equiv = []
    for f, params in transformations:
        for p in params:
            equiv.append([f(matrix, p), f, p])
    return equiv

optimize = True
def get_state(state_matrix):
    if optimize:
        equivalences = get_equivalences(state_matrix)
    else:
        equivalences = [[state_matrix, None, None]]

    found = False

    for s, t, p in equivalences:
        s_hash = hash(repr(s))

        if s_hash in Q_Table:
            found = True
            break

    if not found:
        s_hash = hash(repr(state_matrix))
        Q_Table[s_hash] = [0, 0, 0, 0]
        t = None
        p = None

    return s_hash, t, p


def get_action(state_hash):
    actions = Q_Table[state_hash]
    if max(actions) == 0 or random.random() < epsilon:
        action_idx = random.choice(range(len(actions)))
    else:
        action_idx = max(range(len(actions)), key=lambda i: actions[i])

    action_val = actions[action_idx]
    return action_idx, action_val


epochs = 50000
game_size = 3

e_init = 0.7
e_end = 0.1
a_init = 0.4
a_end = 0.7
gamma = 0.8
epsilon = e_init
alpha = a_init

print("Starting training for game size", game_size)
Q_Table = {}

scores = []
mean_scores = []

game = GameGrid(size=game_size)
player = Player()

for epoch in range(1, epochs+1):
    game.reset()
    state, max_val, over, score = game.state()
    s, t, p = get_state(state)

    while not over:
        a, q_val = get_action(s)
        a_ = permute_action_index(a, t, p)

        old_s = s
        old_state = state
        old_score = score
        old_maxval = max_val

        game.move(player.actions[a_])
        state, max_val, over, score = game.state()

        cell_reward = (repr(state).count("0") - repr(old_state).count("0")) / game_size ** 2
        reward = (score - old_score)
        if max_val - old_maxval > 0:
            reward *= 2
        reward += reward * cell_reward

        s, t, p = get_state(state)

        Q_Table[old_s][a] = q_val + alpha * (reward + gamma * max(Q_Table[s]) - q_val)

        # decay epsilon and alpha
        r = max([(epochs - epoch) / epochs, 0])
        epsilon = (e_init - e_end) * r + e_end
        alpha = (a_init - a_end) * r + a_end

    scores.append(score)
    mean_score = sum(scores[-100:]) / float(len(scores[-100:]))
    mean_scores.append(mean_score)

    if epoch % 100 == 0:
        sys.stdout.write(
            "\repoch {}  \tepsilon: {:.2f}\talpha: {:.2f} \tQ-Table size: {}\tAverage score: {:.2f}\tmax: {}".format(
              epoch, epsilon, alpha, len(Q_Table.keys()), mean_score, max_val))
        sys.stdout.flush()
    if epoch % (1000) == 0:
        print()

game.quit()

print(f"\nAverage score over game size {game_size}: {sum(scores) / len(scores) :.2f}\n", )

x = list(range(len(mean_scores)))
plt.plot(x, mean_scores)
plt.title("3x3 Game Optimized Q-Learning")
plt.show()

print("Q-Table")
print("Anzahl Einträge:", len(Q_Table.keys()))
print(Q_Table)
