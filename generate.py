import random
import numpy
import time


def generate_maze_kruskal(rows, cols,seed, seed_enabled):
    if seed_enabled:
        # Set a fixed seed
        random.seed(seed)
    else:
        seed = int(time.time())
        random.seed(seed)
        print(seed)



    grid = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append((i, j))
        grid.append(row)

    edges = []
    for i in range(rows):
        for j in range(cols):
            if i < rows - 1:
                edges.append(((i, j), (i+1, j)))
            if j < cols - 1:
                edges.append(((i, j), (i, j+1)))

    random.shuffle(edges)

    sets = {cell: {cell} for row in grid for cell in row}

    maze = []
    for edge in edges:
        set1 = sets[edge[0]]
        set2 = sets[edge[1]]
        if set1 != set2:
            maze.append(edge)
            set1.update(set2)
            for cell in set2:
                sets[cell] = set1
    return maze, seed



def transform_display(rows, cols, maze, seed, seed_enabled):
    sqmaze = numpy.zeros((2*rows+1, 2*cols+1))
    for edge in maze:
        i1 = 2*edge[0][0] + 1
        j1 = 2*edge[0][1] + 1
        i2 = 2*edge[1][0] + 1
        j2 = 2*edge[1][1] + 1
        if i1 == i2:
            sqmaze[i1][j1] = 1
            sqmaze[i1][j1+1] = 1
            sqmaze[i1][j2] = 1
        else:
            sqmaze[i1][j1] = 1
            sqmaze[i1+1][j1] = 1
            sqmaze[i2][j1] = 1
    return sqmaze
