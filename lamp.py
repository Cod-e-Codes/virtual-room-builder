import numpy as np

# Function to create a lamp
def plot_lamp(ax, x_start, y_start, lamp_height):
    lamp_vertices = np.array([
        [x_start, y_start, 0],  # lamp base
        [x_start + 1, y_start, 0],
        [x_start + 1, y_start + 1, 0],
        [x_start, y_start + 1, 0],
        [x_start, y_start, lamp_height],  # lamp height
        [x_start + 1, y_start, lamp_height],
        [x_start + 1, y_start + 1, lamp_height],
        [x_start, y_start + 1, lamp_height]
    ])

    lamp_edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # base
        (4, 5), (5, 6), (6, 7), (7, 4),  # top
        (0, 4), (1, 5), (2, 6), (3, 7)   # vertical
    ]

    # Draw lamp edges
    for edge in lamp_edges:
        point1 = lamp_vertices[edge[0]]
        point2 = lamp_vertices[edge[1]]
        ax.plot(*zip(point1, point2), color='orange')
