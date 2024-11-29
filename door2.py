import numpy as np
import matplotlib.pyplot as plt


# Function to add a door
def plot_door(ax, start_x, start_y, height):
    door_vertices = np.array([
        [start_x, start_y, 0],  # base
        [start_x, start_y + 2, 0],
        [start_x, start_y, height],  # vertical
        [start_x, start_y + 2, height]
    ])

    door_edges = [
        (0, 1), (2, 3),  # horizontal
        (0, 2), (1, 3)   # vertical
    ]

    # Draw doorway edges
    for edge in door_edges:
        point1 = door_vertices[edge[0]]
        point2 = door_vertices[edge[1]]
        ax.plot(*zip(point1, point2), color='red')


# Test code snippet
if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    plot_door(ax, 0, 5, 2)
    plt.show()
