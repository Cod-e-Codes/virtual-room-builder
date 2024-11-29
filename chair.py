import numpy as np
import matplotlib.pyplot as plt

# Valid directions
valid_directions = ["north", "south", "east", "west"]


# Custom exception for invalid directions
class ChairError(Exception):
    def __init__(self, message):
        super().__init__(message)


# Chair edge definitions
chair_edges = [
    (0, 4), (1, 5), (2, 6), (3, 7),  # Leg to seat connections
    (4, 5), (5, 6), (6, 7), (7, 4),  # Seat connections
    (7, 11), (6, 10), (10, 11)  # Backrest connections
]


# Main function to plot a chair in specified direction
def plot_chair(ax, x_start, y_start, color, direction):
    if direction not in valid_directions:
        raise ChairError(f"Invalid direction. Choose from: {', '.join(valid_directions)}")

    if direction == "north":
        # Define vertices for north-facing chair
        chair_vertices = np.array([
            [x_start, y_start, 0],  # Legs
            [x_start - 1, y_start, 0],
            [x_start - 1, y_start - 1, 0],
            [x_start, y_start - 1, 0],
            [x_start, y_start, 0.5],  # Seat
            [x_start - 1, y_start, 0.5],
            [x_start - 1, y_start - 1, 0.5],
            [x_start, y_start - 1, 0.5],
            [x_start, y_start, 1],  # Backrest
            [x_start - 1, y_start, 1],
            [x_start - 1, y_start - 1, 1],
            [x_start, y_start - 1, 1]
        ])
    elif direction == "south":
        # Define vertices for south-facing chair
        chair_vertices = np.array([
            [x_start, y_start, 0],  # Legs
            [x_start - 1, y_start, 0],
            [x_start - 1, y_start + 1, 0],
            [x_start, y_start + 1, 0],
            [x_start, y_start, 0.5],  # Seat
            [x_start - 1, y_start, 0.5],
            [x_start - 1, y_start + 1, 0.5],
            [x_start, y_start + 1, 0.5],
            [x_start, y_start, 1],  # Backrest
            [x_start - 1, y_start, 1],
            [x_start - 1, y_start + 1, 1],
            [x_start, y_start + 1, 1]
        ])
    elif direction == "east":
        # Define vertices for east-facing chair
        chair_vertices = np.array([
            [x_start, y_start, 0],  # Legs
            [x_start, y_start + 1, 0],
            [x_start - 1, y_start + 1, 0],
            [x_start - 1, y_start, 0],
            [x_start, y_start, 0.5],  # Seat
            [x_start, y_start + 1, 0.5],
            [x_start - 1, y_start + 1, 0.5],
            [x_start - 1, y_start, 0.5],
            [x_start, y_start, 1],  # Backrest
            [x_start, y_start + 1, 1],
            [x_start - 1, y_start + 1, 1],
            [x_start - 1, y_start, 1]
        ])
    elif direction == "west":
        # Define vertices for west-facing chair
        chair_vertices = np.array([
            [x_start, y_start, 0],  # Legs
            [x_start, y_start - 1, 0],
            [x_start + 1, y_start - 1, 0],
            [x_start + 1, y_start, 0],
            [x_start, y_start, 0.5],  # Seat
            [x_start, y_start - 1, 0.5],
            [x_start + 1, y_start - 1, 0.5],
            [x_start + 1, y_start, 0.5],
            [x_start, y_start, 1],  # Backrest
            [x_start, y_start - 1, 1],
            [x_start + 1, y_start - 1, 1],
            [x_start + 1, y_start, 1]
        ])

    # Draw the edges
    for edge in chair_edges:
        point1 = chair_vertices[edge[0]]
        point2 = chair_vertices[edge[1]]
        ax.plot(*zip(point1, point2), color=color, linewidth=1)


# Test code snippet
if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    plot_chair(ax, 0, 0, "red", "north")
    plot_chair(ax, 2, 2, "orange",  "west")
    plt.show()
