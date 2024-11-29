import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Function to plot a couch with a backrest, seat, and armrests
def plot_couch(ax, x_start, y_start, backrest_height, seat_height, armrest_height):
    couch_vertices = []

    # Backrest vertices
    couch_vertices += [
        [x_start, y_start, 0],  # base of the backrest
        [x_start + 7, y_start, 0],
        [x_start + 7, y_start + 1, 0],
        [x_start, y_start + 1, 0],
        [x_start, y_start, backrest_height],  # top of the backrest
        [x_start + 7, y_start, backrest_height],
        [x_start + 7, y_start + 1, backrest_height],
        [x_start, y_start + 1, backrest_height],
    ]

    # Seat vertices
    couch_vertices += [
        [x_start, y_start + 1, 0],  # base of the seat
        [x_start + 7, y_start + 1, 0],
        [x_start + 7, y_start + 3, 0],
        [x_start, y_start + 3, 0],
        [x_start, y_start + 1, seat_height],  # top of the seat
        [x_start + 7, y_start + 1, seat_height],
        [x_start + 7, y_start + 3, seat_height],
        [x_start, y_start + 3, seat_height],
    ]

    # Armrests vertices
    couch_vertices += [
        [x_start, y_start + 3, 0],  # base of the armrest
        [x_start, y_start + 1, 0],
        [x_start, y_start + 1, armrest_height],  # top of the armrest
        [x_start, y_start + 3, armrest_height],
        [x_start + 7, y_start + 1, 0],  # base of the right armrest
        [x_start + 7, y_start + 3, 0],
        [x_start + 7, y_start + 3, armrest_height],
        [x_start + 7, y_start + 1, armrest_height],
    ]

    # Defining edges for the whole structure
    couch_edges = [
        # Backrest
        (0, 1), (1, 2), (2, 3), (3, 0), 
        (4, 5), (5, 6), (6, 7), (7, 4),  
        (0, 4), (1, 5), (2, 6), (3, 7), 
        # Seat
        (8, 9), (9, 10), (10, 11), (11, 8),
        (12, 13), (13, 14), (14, 15), (15, 12),
        # Armrests
        (16, 17), (17, 18), (18, 19), 
        (20, 21), (21, 22), (22, 23)
    ]

    # Plot the edges
    for edge in couch_edges:
        point1 = couch_vertices[edge[0]]
        point2 = couch_vertices[edge[1]]
        ax.plot(*zip(point1, point2), color='green')

# Test the function
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create a couch with backrest height of 4 units, seat height of 1 unit, and armrest height of 2 units
plot_couch(ax, x_start=0, y_start=0, backrest_height=4, seat_height=1, armrest_height=2)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
