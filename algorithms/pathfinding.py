import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import heapq
from collections import deque

# Pathfinding Algorithms Dictionary
PATHFINDING_ALGORITHMS = {
    "Depth-First Search (DFS)": "depth_first_search",
    "Breadth-First Search (BFS)": "breadth_first_search",
    "A* Algorithm": "a_star",
    "Dijkstra's Algorithm": "dijkstra",
}

# Function to generate a weighted graph
def generate_grid(rows, cols, obstacle_prob=0.2):
    grid = np.zeros((rows, cols), dtype=int)
    
    for i in range(rows):
        for j in range(cols):
            if np.random.rand() < obstacle_prob and (i, j) not in [(0, 0), (rows - 1, cols - 1)]:
                grid[i, j] = 1  # 1 represents an obstacle
    
    return grid

# Function to get valid neighbors
def get_neighbors(grid, node):
    rows, cols = grid.shape
    x, y = node
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and grid[nx, ny] == 0:  # Ignore obstacles
            neighbors.append((nx, ny))

    return neighbors

# Function to reconstruct path
def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

# Depth-First Search (DFS)
def depth_first_search(grid, start, end, update_callback):
    stack = [start]
    visited = set()
    came_from = {}

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        update_callback(grid, visited, None)
        time.sleep(0.1)

        if node == end:
            return reconstruct_path(came_from, end)

        for neighbor in get_neighbors(grid, node):
            if neighbor not in visited:
                came_from[neighbor] = node
                stack.append(neighbor)

    return None

# Breadth-First Search (BFS)
def breadth_first_search(grid, start, end, update_callback):
    queue = deque([start])
    visited = set()
    came_from = {}

    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        update_callback(grid, visited, None)
        time.sleep(0.1)

        if node == end:
            return reconstruct_path(came_from, end)

        for neighbor in get_neighbors(grid, node):
            if neighbor not in visited:
                came_from[neighbor] = node
                queue.append(neighbor)

    return None

# A* Algorithm
def a_star(grid, start, end, update_callback):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = [(0, start)]
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    came_from = {}

    while open_set:
        _, node = heapq.heappop(open_set)

        update_callback(grid, set(g_score.keys()), None)
        time.sleep(0.1)

        if node == end:
            return reconstruct_path(came_from, end)

        for neighbor in get_neighbors(grid, node):
            tentative_g_score = g_score[node] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = node
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

# Dijkstra's Algorithm
def dijkstra(grid, start, end, update_callback):
    pq = [(0, start)]
    distances = {start: 0}
    came_from = {}

    while pq:
        cost, node = heapq.heappop(pq)

        update_callback(grid, set(distances.keys()), None)
        time.sleep(0.1)

        if node == end:
            return reconstruct_path(came_from, end)

        for neighbor in get_neighbors(grid, node):
            new_cost = cost + 1
            if neighbor not in distances or new_cost < distances[neighbor]:
                came_from[neighbor] = node
                distances[neighbor] = new_cost
                heapq.heappush(pq, (new_cost, neighbor))

    return None

# Function to visualize the grid with weighted paths
def plot_grid(grid, visited, path):
    fig, ax = plt.subplots(figsize=(6, 6))  # Adjusted size
    rows, cols = grid.shape

    ax.set_xticks(np.arange(cols + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(rows + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=1)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_aspect('equal')

    for i in range(rows):
        for j in range(cols):
            y_pos = rows - 1 - i  # Flip y-axis

            if grid[i, j] == 1:
                ax.add_patch(plt.Circle((j, y_pos), 0.3, color="black"))  # Obstacles
            elif (i, j) in visited:
                ax.add_patch(plt.Circle((j, y_pos), 0.3, color="blue"))  # Visited nodes
            elif path and (i, j) in path:
                ax.add_patch(plt.Circle((j, y_pos), 0.3, color="lightgreen"))  # Path

            ax.text(j, y_pos, f"{i},{j}", color="white", ha='center', va='center', fontsize=8)

    # Start and End nodes
    ax.add_patch(plt.Circle((0, rows - 1), 0.3, color="red"))   # Start
    ax.add_patch(plt.Circle((cols - 1, 0), 0.3, color="gold"))  # End

    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(-0.5, rows - 0.5)

    return fig

# Streamlit visualization
def visualize_pathfinding():
    st.subheader("Pathfinding Algorithm Visualizer")

    algorithm = st.selectbox("Choose Pathfinding Algorithm", list(PATHFINDING_ALGORITHMS.keys()))
    
    rows, cols = 10, 10
    grid = generate_grid(rows, cols)

    start = (0, 0)
    end = (rows - 1, cols - 1)

    grid_display = st.empty()

    def update_grid(grid, visited, path):
        fig = plot_grid(grid, visited, path)
        grid_display.pyplot(fig)

    if st.button("Start Pathfinding"):
        path = globals()[PATHFINDING_ALGORITHMS[algorithm]](grid, start, end, update_grid)

        if path:
            st.success("Path found!")
        else:
            st.error("No path found.")

        fig = plot_grid(grid, set(), path)
        grid_display.pyplot(fig)

