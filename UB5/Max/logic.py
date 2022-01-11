import numpy as np


def new_game(n):
    matrix = np.zeros((n, n), dtype=np.uint16)
    matrix = add_two(matrix)
    matrix = add_two(matrix)
    return matrix


def add_two(mat):
    a = np.random.randint(0, mat.shape[0])
    b = np.random.randint(0, mat.shape[0])
    while mat[a, b] != 0:
        a = np.random.randint(0, mat.shape[0])
        b = np.random.randint(0, mat.shape[0])
    mat[a, b] = 2
    return mat


def game_state(mat):
    # check for win cell
    if np.amax(mat) == 2048:
        return 'win'
    # check for any zero entries
    if np.amin(mat) == 0:
        return 'not over'
    # check for same cells that touch each other
    for i in range(mat.shape[0]-1):
        # intentionally reduced to check the row on the right and below
        # more elegant to use exceptions but most likely this will be their solution
        for j in range(mat.shape[0]-1):
            if mat[i, j] == mat[i+1, j] or mat[i, j+1] == mat[i, j]:
                return 'not over'
    for k in range(mat.shape[0]-1):  # to check the left/right entries on the last row
        if mat[mat.shape[0]-1, k] == mat[mat.shape[0]-1, k+1]:
            return 'not over'
    for j in range(mat.shape[0]-1):  # check up/down entries on last column
        if mat[j, mat.shape[0]-1] == mat[j+1, mat.shape[0]-1]:
            return 'not over'
    return 'lose'


def cover_up(mat):
    new = np.zeros(mat.shape, dtype=np.uint16)
    done = False
    for i in range(mat.shape[0]):
        count = 0
        for j in range(mat.shape[1]):
            if mat[i, j] != 0:
                new[i, count] = mat[i, j]
                if j != count:
                    done = True
                count += 1
    return new, done


def merge(mat, done):
    points = 0
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]-1):
            if mat[i, j] == mat[i, j+1] and mat[i, j] != 0:
                mat[i, j] *= 2
                points += mat[i, j]
                mat[i, j+1] = 0
                done = True
    return mat, done, points


def up(game):
    # return matrix after shifting up
    game = np.transpose(game)
    game, done = cover_up(game)
    game, done, points = merge(game, done)
    game = cover_up(game)[0]
    game = np.transpose(game)
    return game, done, points


def down(game):
    # return matrix after shifting down
    game = np.fliplr(np.transpose(game))
    game, done = cover_up(game)
    game, done, points = merge(game, done)
    game = cover_up(game)[0]
    game = np.transpose(np.fliplr(game))
    return game, done, points


def left(game):
    # return matrix after shifting left
    game, done = cover_up(game)
    game, done, points = merge(game, done)
    game = cover_up(game)[0]
    return game, done, points


def right(game):
    # return matrix after shifting right
    game = np.fliplr(game)
    game, done = cover_up(game)
    game, done, points = merge(game, done)
    game = cover_up(game)[0]
    game = np.fliplr(game)
    return game, done, points

