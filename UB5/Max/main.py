import argparse
import qlearning
import random_player
import matplotlib.pyplot as plt
import numpy as np
import json


def main(args):
    q_history, qd_history, q_table = qlearning.q_learn_game(args["size"], args["epochs"], args["eval_interval"], args["alpha"],
                                       args["alpha_decay"], args["alpha_decay_interval"], args["epsilon"],
                                       args["epsilon_decay"], args["epsilon_decay_interval"], args["gamma"])
    r_history = random_player.random_player_game(args["size"], args["epochs"], args["eval_interval"])
    x = np.arange(0, len(q_history))
    plt.figure(1)
    plt.plot(x, q_history)
    plt.plot(x, r_history, color="red")
    plt.ylabel("Avg Score")
    plt.xlabel("Epoch")

    plt.figure(2)
    x = np.arange(0, len(qd_history))
    plt.plot(x, qd_history*100)
    plt.ylabel("Table based decision %")
    plt.xlabel("Epoch")
    plt.show()

    with open('file.txt', 'w') as file:
        file.write(json.dumps(q_table))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-size', type=int, default=2)
    parser.add_argument('-epochs', type=int, default=10000)
    parser.add_argument('-eval_interval', type=int, default=100)
    parser.add_argument('-alpha', type=float, default=0.7)
    parser.add_argument('-alpha_decay', type=float, default=0.95)
    parser.add_argument('-alpha_decay_interval', type=int, default=150)
    parser.add_argument('-epsilon', type=float, default=0.3)
    parser.add_argument('-epsilon_decay', type=float, default=0.9)
    parser.add_argument('-epsilon_decay_interval', type=int, default=100)
    parser.add_argument('-gamma', type=float, default=0.3)
    args = vars(parser.parse_args())
    main(args)
