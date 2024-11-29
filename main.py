import matplotlib.pyplot as plt  # type: ignore

# Import all the components
from room import plot_room as Room
from door import plot_door as Door
from door2 import plot_door as Door2
from table import plot_table as Table
from chair import plot_chair as Chair
from lamp import plot_lamp as Lamp
from bookshelf import plot_bookshelf as Bookshelf
# from couch import plot_couch as Couch


def main():
    # Create a new figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Draw the room
    Room(ax, 15, 15, 4)

    # Add a door
    Door(ax, 5, 0, 2)
    Door2(ax, 0, 5, 2)

    # Add furniture
    Chair(ax, 7, 5, "black", 'north')
    Chair(ax, 7, 9, "black", 'south')
    Chair(ax, 5, 7, "black", 'east')
    Chair(ax, 9, 8, "black", 'west')
    Table(ax, 5, 5.5, .75, 0, "peru")
    Lamp(ax, 0, 14, 1)
    Lamp(ax, 14, 14, 2)
    Bookshelf(ax, 2, 14, 3, 4, "sienna", "black", 'south')
    Bookshelf(ax, 8, 14, 2, 2, "saddlebrown", "tan", 'south')
    # Couch(ax, 12, 10, 1)

    # Set plot limits
    ax.set_xlim([0, 15])
    ax.set_ylim([0, 15])
    ax.set_zlim([0, 4])

    # Set labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()


# Run the main function
if __name__ == '__main__':
    main()
