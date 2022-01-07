import numpy as np


def new_game(n):
    matrix = np.zeros(shape=(n,n))
    matrix = add_two(matrix, 2)
    return matrix


def add_two(mat, n=1):
    flat = mat.flatten()
    zeros = np.argwhere(flat == 0).squeeze()
    if zeros.shape == ():
        zeros = [zeros]
    zeros = np.random.choice(zeros, min(len(zeros), n))
    flat[zeros] = 2
    mat = flat.reshape(mat.shape)
    return mat


# OBSERVE
def score(mat):
    return np.max(mat)

# OBSERVE
def game_state(mat):
    flat = mat.flatten()

    if 0 in flat:
        return False

    for i in range(len(flat)):
        if i % len(mat) != len(mat) - 1 and flat[i] == flat[i + 1]:
            return False
        if i < len(flat) - len(mat) and flat[i] == flat[i + len(mat)]:
            return False

    return True


def reverse(mat):
    return np.flip(mat, axis=-1)


def transpose(mat):
    return np.transpose(mat)


def shift(mat):
    new = np.zeros_like(mat)
    for i in range(mat.shape[0]):
        anchor = 0
        for j in range(mat.shape[1]):
            if mat[i][j] != 0:
                new[i][anchor] = mat[i][j]
                anchor += 1

    done = not np.array_equal(mat, new)
    return new, done


def merge(mat, done):
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]-1):
            if mat[i][j] == mat[i][j+1] and mat[i][j] != 0:
                mat[i][j] *= 2
                mat[i][j+1] = 0
                done = True
    return mat, done


def up(mat):
    mat = transpose(mat)
    mat, done = shift(mat)
    mat, done = merge(mat, done)
    mat = shift(mat)[0]
    mat = transpose(mat)
    return mat, done


def down(mat):
    mat = reverse(transpose(mat))
    mat, done = shift(mat)
    mat, done = merge(mat, done)
    mat = shift(mat)[0]
    mat = transpose(reverse(mat))
    return mat, done


def left(mat):
    mat, done = shift(mat)
    mat, done = merge(mat, done)
    mat = shift(mat)[0]
    return mat, done


def right(mat):
    mat = reverse(mat)
    mat, done = shift(mat)
    mat, done = merge(mat, done)
    mat = shift(mat)[0]
    mat = reverse(mat)
    return mat, done
