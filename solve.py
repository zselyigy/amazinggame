import heapq
import main
import time

def GBFS(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons):
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
        if sqmaze[node[0]][node[1]] != 3:
            sqmaze[node[0]][node[1]] = 6
            main.display_ingame_screen(sqmaze, screen, offset_x, offset_y, zoom, rows, cols, buttons)
            time.sleep(0.05)

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