import random
import numpy

def generate_maze_kruskal(rows, cols):
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
    return maze



def transform_display(rows, cols, maze):
    sqmaze = numpy.zeros((2*rows+1, 2*cols+1))
#    for i in range(2*rows+1):
#        for j in range(2*cols+1):
#            if i % 2 == 1 and j % 2 == 1:
#                sqmaze[j][i] = 1

    for edge in maze:
        i1 = 2*edge[0][0] + 1
        j1 = 2*edge[0][1] + 1
        i2 = 2*edge[1][0] + 1
        j2 = 2*edge[1][1] + 1
        if i1 == i2:
#            j = (j1 + j2) // 2
            sqmaze[j1][i1] = 1
            sqmaze[j1+1][i1] = 1
            sqmaze[j2][i1] = 1
        else:
#            i = (i1 + i2) // 2
            sqmaze[j1][i1] = 1
            sqmaze[j1][i1+1] = 1
            sqmaze[j1][i2] = 1
    return sqmaze