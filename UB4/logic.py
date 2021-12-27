#
# CS1010FC --- Programming Methodology
#
# Mission N Solutions
#
# Note that written answers are commented out to allow us to run your
# code easily while grading your problem set.

import constants as c
import numpy as np

#######
# Task 1a #
#######

# [Marking Scheme]
# Points to note:
# Matrix elements must be equal but not identical
# 1 mark for creating the correct matrix


def new_game(n):
    matrix = np.zeros((n, n), dtype=np.uint16)
    matrix = add_two(matrix)
    matrix = add_two(matrix)
    return matrix

###########
# Task 1b #
###########

# [Marking Scheme]
# Points to note:
# Must ensure that it is created on a zero entry
# 1 mark for creating the correct loop


def add_two(mat):
    a = np.random.randint(0, mat.shape[0])
    b = np.random.randint(0, mat.shape[0])
    while mat[a, b] != 0:
        a = np.random.randint(0, mat.shape[0])
        b = np.random.randint(0, mat.shape[0])
    mat[a, b] = 2
    return mat


###########
# Task 1c #
###########

# [Marking Scheme]
# Points to note:
# Matrix elements must be equal but not identical
# 0 marks for completely wrong solutions
# 1 mark for getting only one condition correct
# 2 marks for getting two of the three conditions
# 3 marks for correct checking


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


###########
# Task 2a #
###########

# [Marking Scheme]
# Points to note:
# 0 marks for completely incorrect solutions
# 1 mark for solutions that show general understanding
# 2 marks for correct solutions that work for all sizes of matrices

###########
# Task 2b #
###########

# [Marking Scheme]
# Points to note:
# 0 marks for completely incorrect solutions
# 1 mark for solutions that show general understanding
# 2 marks for correct solutions that work for all sizes of matrices

##########
# Task 3 #
##########

# [Marking Scheme]
# Points to note:
# The way to do movement is compress -> merge -> compress again
# Basically if they can solve one side, and use transpose and reverse correctly they should
# be able to solve the entire thing just by flipping the matrix around
# No idea how to grade this one at the moment. I have it pegged to 8 (which gives you like,
# 2 per up/down/left/right?) But if you get one correct likely to get all correct so...
# Check the down one. Reverse/transpose if ordered wrongly will give you wrong result.


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
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]-1):
            if mat[i, j] == mat[i, j+1] and mat[i, j] != 0:
                mat[i, j] *= 2
                mat[i, j+1] = 0
                done = True
    return mat, done


def up(game):
    # return matrix after shifting up
    game = np.transpose(game)
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = np.transpose(game)
    return game, done


def down(game):
    # return matrix after shifting down
    game = np.fliplr(np.transpose(game))
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = np.transpose(np.fliplr(game))
    return game, done


def left(game):
    # return matrix after shifting left
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    return game, done


def right(game):
    # return matrix after shifting right
    game = np.fliplr(game)
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = np.fliplr(game)
    return game, done

