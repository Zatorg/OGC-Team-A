import time
import argparse

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

from puzzle import GameGrid
from player import Player


def main(args):
    if args["machine"]:
        print("number of epochs:", args["epochs"])
        scores = []
        for i in [2, 3, 4]:
            start = time.time()
            scores.append(train(epochs=args["epochs"], game_size=i))
            print(f"game size {i}x{i}:")
            print(f"\tfinished in {time.time() - start:.3f} secs")
            print("\tmean score:", sum(scores[-1]) / len(scores[-1]))

        plot_results(scores)

    else:
        game = GameGrid(args["size"])
        game.mainloop()


def plot_results(results):
    fig, ax = plt.subplots()

    plt.yscale('log', base=2)
    ax.yaxis.set_major_formatter(ScalarFormatter())  # 4 instead of 2²
    ax.set_ylabel("Score")
    ax.set_xlabel("Game")

    plots = []
    labels = []
    for i, r in enumerate(results):
        plots.append(ax.plot(list(range(len(r))), r))
        labels.append(f"{i+2}x{i+2}")

    fig.legend(plots, labels=labels, loc="center right", borderaxespad=0.1)
    plt.show()


def train(epochs, game_size):
    game = GameGrid(game_size)
    player = Player()

    scores = []
    while epochs > 0:
        # if you want to watch:
        #game.update()
        m = player.move()
        game.move(m)
        _, score, over = game.state()

        if over:
            scores.append(score)
            game.reset()
            epochs -= 1

    game.quit()
    return scores


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--human', dest='machine', action='store_false', default=True)
    parser.add_argument('-epochs', type=int, default=100)
    parser.add_argument('-size', type=int, default=4)

    args = vars(parser.parse_args())
    main(args)
