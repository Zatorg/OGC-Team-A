import random
import constants as c


def new_game(n):
    matrix = [[0] * n for _ in range(n)]
    matrix = add_two(matrix)
    matrix = add_two(matrix)
    return matrix


def add_two(mat):
    a = random.randint(0, len(mat) - 1)
    b = random.randint(0, len(mat) - 1)
    while mat[a][b] != 0:
        a = random.randint(0, len(mat) - 1)
        b = random.randint(0, len(mat) - 1)
    mat[a][b] = 2
    return mat


def state(mat):
    flat = []
    for row in mat:
        flat.extend(row)

    game_over = True
    score = max(flat)

    if 0 in flat:
        game_over = False

    for i in range(len(flat)):
        if i % len(mat) != len(mat) - 1 and flat[i] == flat[i + 1]:
            game_over = False
        if i < len(flat) - len(mat) and flat[i] == flat[i + len(mat)]:
            game_over = False

    return mat, score, game_over


def reverse(mat):
    new = []
    for row in mat:
        new.append(row[::-1])
    return new


def transpose(mat):
    new = []
    for i in range(len(mat)):
        new.append([mat[j][i] for j in range(len(mat))])
    return new


def shift(mat):
    new = [[0] * len(mat) for _ in range(len(mat))]
    for i in range(len(mat)):
        anchor = 0
        for j in range(len(mat)):
            if mat[i][j] != 0:
                new[i][anchor] = mat[i][j]
                anchor += 1

    done = mat != new
    return new, done


def merge(mat, done):
    for i in range(len(mat)):
        for j in range(len(mat) - 1):
            if mat[i][j] == mat[i][j + 1] and mat[i][j] != 0:
                mat[i][j] *= 2
                mat[i][j + 1] = 0
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
