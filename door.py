import numpy as np


# Function to add a door
def plot_door(ax, start_x, start_y, height):
    door_vertices = np.array([
        [start_x, start_y, 0],  # base
        [start_x + 2, start_y, 0],
        [start_x, start_y, height],  # vertical
        [start_x + 2, start_y, height]
    ])

    door_edges = [
        (0, 1), (2, 3),  # horizontal
        (0, 2), (1, 3)   # vertical
    ]

    # Draw door edges
    for edge in door_edges:
        point1 = door_vertices[edge[0]]
        point2 = door_vertices[edge[1]]
        ax.plot(*zip(point1, point2), color='red')
