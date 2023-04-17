import random

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