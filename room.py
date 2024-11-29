import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Function to plot the room with given dimensions
def plot_room(ax, length, width, height):
    # Room vertices
    room_vertices = np.array([
        [0, 0, 0],  # bottom corners
        [length, 0, 0],
        [length, width, 0],
        [0, width, 0],
        [0, 0, height],  # top corners
        [length, 0, height],
        [length, width, height],
        [0, width, height]
    ])

    # Room edges
    room_edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # bottom
        (4, 5), (5, 6), (6, 7), (7, 4),  # top
        (0, 4), (1, 5), (2, 6), (3, 7)   # vertical
    ]

    # Draw room edges
    for edge in room_edges:
        point1 = room_vertices[edge[0]]
        point2 = room_vertices[edge[1]]
        ax.plot(*zip(point1, point2), color='black')
