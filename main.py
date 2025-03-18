import tkinter as tk
import heapq

# Grid settings
GRID_SIZE = 10
TILE_SIZE = 50

# Colors
EMPTY_COLOR = "white"
PILLAR_COLOR = "black"
START_COLOR = "green"
END_COLOR = "red"
PATH_COLOR = "blue"

# Initialize grid and state
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
start = None
end = None

# Pre-set 5 pillar positions
initial_pillars = [(2, 3), (4, 5), (6, 7), (1, 8), (7, 2)]
for x, y in initial_pillars:
    grid[x][y] = 1

# A* Pathfinding algorithm
def astar(grid, start, end):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in neighbors:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE:
                if grid[neighbor[0]][neighbor[1]] == 1:
                    continue  # Skip pillars

                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_list, (f_score, neighbor))

    return []  # No path found

# Handle clicks on the grid
def on_click(event):
    global start, end
    x, y = event.x // TILE_SIZE, event.y // TILE_SIZE

    if grid[x][y] == 1:
        return

    if not start:
        start = (x, y)
        canvas.itemconfig(tiles[x][y], fill=START_COLOR)
    elif not end:
        end = (x, y)
        canvas.itemconfig(tiles[x][y], fill=END_COLOR)
    else:
        path = astar(grid, start, end)
        if path:
            for px, py in path:
                canvas.itemconfig(tiles[px][py], fill=PATH_COLOR)
        else:
            print("No path found")

# Toggle pillar
def toggle_pillar(x, y):
    if grid[x][y] == 0:
        grid[x][y] = 1
        canvas.itemconfig(tiles[x][y], fill=PILLAR_COLOR)
    else:
        grid[x][y] = 0
        canvas.itemconfig(tiles[x][y], fill=EMPTY_COLOR)

# Create the main window
root = tk.Tk()
root.title("Route Finder")

canvas = tk.Canvas(root, width=GRID_SIZE * TILE_SIZE, height=GRID_SIZE * TILE_SIZE)
canvas.pack()

# Draw grid
tiles = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        rect = canvas.create_rectangle(
            x * TILE_SIZE, y * TILE_SIZE,
            (x + 1) * TILE_SIZE, (y + 1) * TILE_SIZE,
            fill=PILLAR_COLOR if (x, y) in initial_pillars else EMPTY_COLOR
        )
        tiles[x][y] = rect

# Bind events
canvas.bind("<Button-1>", on_click)  # Left click to select start/end
canvas.bind("<Button-3>", lambda e: toggle_pillar(e.x // TILE_SIZE, e.y // TILE_SIZE))  # Right click for pillars

root.mainloop()
