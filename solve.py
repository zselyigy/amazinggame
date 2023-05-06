import heapq
import main
import time
import globals
import decimal

def GBFS(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons):
    # Define the heuristic function
    def heuristic(node):
        return abs(node[0] - end[0]) + abs(node[1] - end[1])
#        return (abs(node[0] - end[0]))^2 + (abs(node[1] - end[1]))^2

    # Find start and end points
    for i in range(len(sqmaze)):
        for j in range(len(sqmaze[0])):
            if sqmaze[i][j] == 3:
                start = (i, j)
            elif sqmaze[i][j] == 4:
                end = (i, j)

    # Initialize the data structures
    visited = set()
    parents = {}
    queue = []

    # Add the start node to the queue
    heapq.heappush(queue, (heuristic(start), start))

    # Loop until the queue is empty or the goal is found
    while queue:
        # Pop the node with the lowest heuristic value
        node = heapq.heappop(queue)[1]

        # Check if the goal has been reached
        if node == end:
            # Reconstruct the path and return it
            path = [node]
            while node != start:
                node = parents[node]
                path.append(node)
            return list(reversed(path))

        # Add the node to the visited set
        visited.add(node)
        globals.alg_sp = globals.alg_sp+1
        globals.solved_text = globals.alg_sp / globals.path_nmbr
        globals.c = decimal.Decimal(globals.solved_text)
        globals.percentage =(round(globals.c, 4) * 100)

        if sqmaze[node[0]][node[1]] != 3:
            sqmaze[node[0]][node[1]] = 6
#            main.display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 1)
            main.display_mazecell(screen, offset_x, offset_y, zoom, node[0], node[1], sqmaze)
            time.sleep(1/((rows*cols)/4))


        # Expand the node's neighbors
        for neighbor in [(node[0]-1, node[1]), (node[0]+1, node[1]), (node[0], node[1]-1), (node[0], node[1]+1)]:
            if neighbor[0] < 0 or neighbor[0] >= len(sqmaze) or neighbor[1] < 0 or neighbor[1] >= len(sqmaze[0]):
                # Neighbor is out of bounds
                continue
            if sqmaze[neighbor[0]][neighbor[1]] == 0:
                # Neighbor is a wall
                continue
            if neighbor in visited:
                # Neighbor has already been visited
                continue

            # Add the neighbor to the queue and update its parent
            parents[neighbor] = node
            heapq.heappush(queue, (heuristic(neighbor), neighbor))

    # Goal was not found
    return None

def astar(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons):
    # Define the heuristic function
    def heuristic(node):
        return abs(node[0] - end[0]) + abs(node[1] - end[1])
    
    # Find start and end points
    for i in range(len(sqmaze)):
        for j in range(len(sqmaze[0])):
            if sqmaze[i][j] == 3:
                start = (i, j)
            elif sqmaze[i][j] == 4:
                end = (i, j)

    # Initialize the data structures
    visited = set()
    parents = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start)}
    queue = []

    # Add the start node to the queue
    heapq.heappush(queue, (f_score[start], start))

    # Loop until the queue is empty or the goal is found
    while queue:
        # Pop the node with the lowest f-score
        node = heapq.heappop(queue)[1]

        # Check if the goal has been reached
        if node == end:
            # Reconstruct the path and return it
            path = [node]
            while node != start:
                node = parents[node]
                path.append(node)
            return list(reversed(path))

        # Add the node to the visited set
        visited.add(node)
        globals.alg_sp = globals.alg_sp+1
        globals.solved_text = globals.alg_sp / globals.path_nmbr
        globals.c = decimal.Decimal(globals.solved_text)
        globals.percentage =(round(globals.c, 4) * 100)

        if sqmaze[node[0]][node[1]] != 3:
            sqmaze[node[0]][node[1]] = 6
#            main.display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons, 1)
            main.display_mazecell(screen, offset_x, offset_y, zoom, node[0], node[1], sqmaze)
            time.sleep(1/((rows*cols)/2))

        # Expand the node's neighbors
        for neighbor in [(node[0]-1, node[1]), (node[0]+1, node[1]), (node[0], node[1]-1), (node[0], node[1]+1)]:
            if neighbor[0] < 0 or neighbor[0] >= len(sqmaze) or neighbor[1] < 0 or neighbor[1] >= len(sqmaze[0]):
                # Neighbor is out of bounds
                continue
            if sqmaze[neighbor[0]][neighbor[1]] == 0:
                # Neighbor is a wall
                continue
            if neighbor in visited:
                # Neighbor has already been visited
                continue

            # Calculate the tentative g-score for the neighbor
            tentative_g_score = g_score[node] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                # This path to the neighbor is better than any previous one. Update the neighbor's g-score, f-score, and parent.
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor)
                parents[neighbor] = node

                # Add the neighbor to the queue
                heapq.heappush(queue, (f_score[neighbor], neighbor))

    # Goal was not found
    return None


def dfs(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons):
    # Find start and end points
    for i in range(len(sqmaze)):
        for j in range(len(sqmaze[0])):
            if sqmaze[i][j] == 3:
                start = (i, j)
            elif sqmaze[i][j] == 4:
                end = (i, j)

    # Initialize the data structures
    visited = set()
    parents = {}
    stack = []

    # Add the start node to the stack
    stack.append(start)

    # Loop until the stack is empty or the goal is found
    while stack:
        # Pop the next node from the stack
        node = stack.pop()

        # Check if the goal has been reached
        if node == end:
            # Reconstruct the path and return it
            path = [node]
            while node != start:
                node = parents[node]
                path.append(node)
            return list(reversed(path))

        # Add the node to the visited set
        visited.add(node)
        globals.alg_sp = globals.alg_sp+1
        globals.solved_text = globals.alg_sp / globals.path_nmbr
        globals.c = decimal.Decimal(globals.solved_text)
        globals.percentage =(round(globals.c, 4) * 100)

        if sqmaze[node[0]][node[1]] != 3:
            sqmaze[node[0]][node[1]] = 6
            main.display_mazecell(screen, offset_x, offset_y, zoom, node[0], node[1], sqmaze)
            time.sleep(1/((rows*cols)/2))

        # Expand the node's neighbors
        for neighbor in [(node[0]-1, node[1]), (node[0]+1, node[1]), (node[0], node[1]-1), (node[0], node[1]+1)]:
            if neighbor[0] < 0 or neighbor[0] >= len(sqmaze) or neighbor[1] < 0 or neighbor[1] >= len(sqmaze[0]):
                # Neighbor is out of bounds
                continue
            if sqmaze[neighbor[0]][neighbor[1]] == 0:
                # Neighbor is a wall
                continue
            if neighbor in visited:
                # Neighbor has already been visited
                continue

            # Set the parent of the neighbor to the current node
            parents[neighbor] = node

            # Add the neighbor to the stack
            stack.append(neighbor)

    # Goal was not found
    return None


def bfs(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons):
    # Find start and end points
    for i in range(len(sqmaze)):
        for j in range(len(sqmaze[0])):
            if sqmaze[i][j] == 3:
                start = (i, j)
            elif sqmaze[i][j] == 4:
                end = (i, j)
    # Find the rows and columns of the maze
    rows = len(sqmaze)
    cols = len(sqmaze[0])

    # Initialize the data structures
    visited = set()
    parents = {}
    queue = []

    # Add the start node to the queue
    queue.append(start)

    # Loop until the queue is empty or the goal is found
    while queue:
        # Pop the node from the front of the queue
        node = queue.pop(0)

        # Check if the goal has been reached
        if node == end:
            # Reconstruct the path and return it
            path = [node]
            while node != start:
                node = parents[node]
                path.append(node)
            return list(reversed(path))

        # Add the node to the visited set
        visited.add(node)
        globals.alg_sp = globals.alg_sp+1
        globals.solved_text = globals.alg_sp / globals.path_nmbr
        globals.c = decimal.Decimal(globals.solved_text)
        globals.percentage =(round(globals.c, 4) * 100)

        if sqmaze[node[0]][node[1]] != 3:
            sqmaze[node[0]][node[1]] = 6
            main.display_mazecell(screen, offset_x, offset_y, zoom, node[0], node[1], sqmaze)
            time.sleep(1/((rows*cols)/2))

        # Expand the node's neighbors
        for neighbor in [(node[0]-1, node[1]), (node[0]+1, node[1]), (node[0], node[1]-1), (node[0], node[1]+1)]:
            if neighbor[0] < 0 or neighbor[0] >= rows or neighbor[1] < 0 or neighbor[1] >= cols:
                # Neighbor is out of bounds
                continue
            if sqmaze[neighbor[0]][neighbor[1]] == 0:
                # Neighbor is a wall
                continue
            if neighbor in visited:
                # Neighbor has already been visited
                continue

            # Add the neighbor to the queue and mark its parent
            queue.append(neighbor)
            parents[neighbor] = node

    # Goal was not found
    return None



def dijkstra(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons):
    # Find start and end points
    for i in range(len(sqmaze)):
        for j in range(len(sqmaze[0])):
            if sqmaze[i][j] == 3:
                start = (i, j)
            elif sqmaze[i][j] == 4:
                end = (i, j)

    # Initialize the data structures
    visited = set()
    parents = {}
    distances = {start: 0}
    queue = []

    # Add the start node to the queue
    heapq.heappush(queue, (distances[start], start))

    # Loop until the queue is empty or the goal is found
    while queue:
        # Pop the node with the lowest distance
        node = heapq.heappop(queue)[1]

        # Check if the goal has been reached
        if node == end:
            # Reconstruct the path and return it
            path = [node]
            while node != start:
                node = parents[node]
                path.append(node)
            return list(reversed(path))

        # Add the node to the visited set
        visited.add(node)
        globals.alg_sp = globals.alg_sp+1
        globals.solved_text = globals.alg_sp / globals.path_nmbr
        globals.c = decimal.Decimal(globals.solved_text)
        globals.percentage =(round(globals.c, 4) * 100)

        if sqmaze[node[0]][node[1]] != 3:
            sqmaze[node[0]][node[1]] = 6
            main.display_mazecell(screen, offset_x, offset_y, zoom, node[0], node[1], sqmaze)
            time.sleep(1/((rows*cols)))

        # Expand the node's neighbors
        for neighbor in [(node[0]-1, node[1]), (node[0]+1, node[1]), (node[0], node[1]-1), (node[0], node[1]+1)]:
            if neighbor[0] < 0 or neighbor[0] >= len(sqmaze) or neighbor[1] < 0 or neighbor[1] >= len(sqmaze[0]):
                # Neighbor is out of bounds
                continue
            if sqmaze[neighbor[0]][neighbor[1]] == 0:
                # Neighbor is a wall
                continue
            if neighbor in visited:
                # Neighbor has already been visited
                continue

            # Calculate the tentative distance for the neighbor
            tentative_distance = distances[node] + 1

            if neighbor not in distances or tentative_distance < distances[neighbor]:
                # This path to the neighbor is better than any previous one. Update the neighbor's distance and parent.
                distances[neighbor] = tentative_distance
                parents[neighbor] = node

                # Add the neighbor to the queue
                heapq.heappush(queue, (distances[neighbor], neighbor))

    # Goal was not found
    return None