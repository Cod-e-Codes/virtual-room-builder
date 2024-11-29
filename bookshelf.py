import numpy as np
import matplotlib.pyplot as plt

# Define a list of valid directions for the bookshelf
valid_directions = ["north", "south", "east", "west"]

# Custom exception for invalid bookshelf directions
class BookshelfError(Exception):
    def __init__(self, message):
        super().__init__(message)

# Function to create a bookshelf
def plot_bookshelf(ax, x_start, y_start, height, num_shelves, base_color, shelf_color, direction):
    if direction not in valid_directions:
        raise BookshelfError(f"Invalid direction. Choose from: {', '.join(valid_directions)}")

    # Bookshelf base and top vertices based on direction
    if direction == "north":
        bookshelf_vertices = np.array([
            [x_start, y_start, 0],  # Base
            [x_start, y_start - 1, 0],
            [x_start + 5, y_start - 1, 0],
            [x_start + 5, y_start, 0],
            [x_start, y_start, height],  # Top
            [x_start, y_start - 1, height],
            [x_start + 5, y_start - 1, height],
            [x_start + 5, y_start, height]
        ])
    elif direction == "south":
        bookshelf_vertices = np.array([
            [x_start, y_start, 0],  # Base
            [x_start, y_start + 1, 0],
            [x_start + 5, y_start + 1, 0],
            [x_start + 5, y_start, 0],
            [x_start, y_start, height],  # Top
            [x_start, y_start + 1, height],
            [x_start + 5, y_start + 1, height],
            [x_start + 5, y_start, height]
        ])
    elif direction == "east":
        bookshelf_vertices = np.array([
            [x_start, y_start, 0],  # Base
            [x_start + 1, y_start, 0],
            [x_start + 1, y_start + 5, 0],
            [x_start, y_start + 5, 0],
            [x_start, y_start, height],  # Top
            [x_start + 1, y_start, height],
            [x_start + 1, y_start + 5, height],
            [x_start, y_start + 5, height]
        ])
    elif direction == "west":
        bookshelf_vertices = np.array([
            [x_start, y_start, 0],  # Base
            [x_start - 1, y_start, 0],
            [x_start - 1, y_start - 5, 0],
            [x_start, y_start - 5, 0],
            [x_start, y_start, height],  # Top
            [x_start - 1, y_start, height],
            [x_start - 1, y_start - 5, height],
            [x_start, y_start - 5, height]
        ])

    # Define common bookshelf edges
    bookshelf_edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Base
        (4, 5), (5, 6), (6, 7), (7, 4),  # Top
        (0, 4), (1, 5), (2, 6), (3, 7)   # Vertical edges
    ]

    # Draw bookshelf edges
    for edge in bookshelf_edges:
        point1 = bookshelf_vertices[edge[0]]
        point2 = bookshelf_vertices[edge[1]]
        ax.plot(*zip(point1, point2), color=base_color)

    # Calculate shelf heights based on the number of shelves
    shelf_heights = np.linspace(0, height, num_shelves + 2)[1:-1]

    # Draw shelves
    for shelf_height in shelf_heights:
        if direction in ["north", "south"]:
            if direction == "north":
                shelf_vertices = [
                    [x_start, y_start, shelf_height],  # Start of shelf
                    [x_start, y_start - 1, shelf_height],
                    [x_start + 5, y_start - 1, shelf_height],
                    [x_start + 5, y_start, shelf_height]
                ]
            else:  # For "south"
                shelf_vertices = [
                    [x_start, y_start, shelf_height],  # Start of shelf
                    [x_start, y_start + 1, shelf_height],
                    [x_start + 5, y_start + 1, shelf_height],
                    [x_start + 5, y_start, shelf_height]
                ]
        elif direction in ["east", "west"]:
            if direction == "east":
                shelf_vertices = [
                    [x_start, y_start, shelf_height],  # Start of shelf
                    [x_start + 1, y_start, shelf_height],
                    [x_start + 1, y_start + 5, shelf_height],
                    [x_start, y_start + 5, shelf_height]
                ]
            else:  # For "west"
                shelf_vertices = [
                    [x_start, y_start, shelf_height],  # Start of shelf
                    [x_start - 1, y_start, shelf_height],
                    [x_start - 1, y_start - 5, shelf_height],
                    [x_start, y_start - 5, shelf_height]
                ]

        # Define shelf edges and plot
        shelf_edges = [
            (0, 1), (1, 2), (2, 3), (3, 0)  # Edges of each shelf
        ]
        
        for edge in shelf_edges:
            point1 = shelf_vertices[edge[0]]
            point2 = shelf_vertices[edge[1]]
            ax.plot(*zip(point1, point2), color=shelf_color)


