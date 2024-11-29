import numpy as np
import matplotlib.pyplot as plt

# Function to create a table with top and legs, without bottom edges
def plot_table(ax, x_start, y_start, top_height, leg_height, color):
    table_vertices = np.array([
        [x_start, y_start, top_height],  # table top
        [x_start + 4, y_start, top_height],
        [x_start + 4, y_start + 4, top_height],
        [x_start, y_start + 4, top_height],
        [x_start, y_start, leg_height],  # legs
        [x_start + 4, y_start, leg_height],
        [x_start + 4, y_start + 4, leg_height],
        [x_start, y_start + 4, leg_height]
    ])

    table_edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # table top
        (0, 4), (1, 5), (2, 6), (3, 7)   # legs
    ]

    # Draw table edges
    for edge in table_edges:
        point1 = table_vertices[edge[0]]
        point2 = table_vertices[edge[1]]
        ax.plot(*zip(point1, point2), color)


# Test code snippet
if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    plot_table(ax, 5, 5, 1, 0, "black")
    plt.show()
