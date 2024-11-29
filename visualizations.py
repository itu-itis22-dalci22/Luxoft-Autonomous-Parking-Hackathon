import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def visualize_parking_grid(grid: List[List[int]], 
                            start: Tuple[int, int], 
                            closest_spots: List[Tuple[int, int, int]]):
    """
    Visualize the parking grid with closest parking spots.
    
    :param grid: 2D list representing the parking area (0 for empty, 1 for occupied)
    :param start: Starting coordinates (row, col)
    :param closest_spots: List of closest parking spots with their distances
    """
    rows, cols = len(grid), len(grid[0])
    
    # Create a color grid
    color_grid = np.zeros((rows, cols, 3))
    
    # Color coding
    # Occupied spots: Red
    # Empty spots: Green
    # Start point: Yellow
    # Closest spots: Blue
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 1:  # Occupied
                color_grid[row, col] = [1, 0, 0]  # Red
            else:  # Empty
                color_grid[row, col] = [0, 1, 0]  # Green
    
    # Mark start point
    color_grid[start[0], start[1]] = [1, 1, 0]  # Yellow
    
    # Mark closest spots
    for spot in closest_spots:
        color_grid[spot[0], spot[1]] = [0, 0, 1]  # Blue
    
    # Plotting
    plt.figure(figsize=(10, 8))
    plt.imshow(color_grid)
    plt.title(f"Parking Grid - Closest Spots from {start}")
    
    # Add grid lines
    for x in range(cols + 1):
        plt.axvline(x - 0.5, color='black', linewidth=1)
    for y in range(rows + 1):
        plt.axhline(y - 0.5, color='black', linewidth=1)
    
    # Add spot coordinates and distances
    for row in range(rows):
        for col in range(cols):
            # Coordinate text
            plt.text(col, row, f"({row},{col})", 
                     ha='center', va='center', color='white', fontsize=8)
    
    # Annotate closest spots with their distances
    for spot in closest_spots:
        row, col, distance = spot
        plt.text(col, row, f"D:{distance}", 
                 ha='center', va='bottom', color='white', fontsize=8)
    
    plt.xticks(range(cols))
    plt.yticks(range(rows))
    plt.grid(False)
    
    # Add a legend
    legend_elements = [
        plt.Rectangle((0, 0), 1, 1, color='red', label='Occupied'),
        plt.Rectangle((0, 0), 1, 1, color='green', label='Empty'),
        plt.Rectangle((0, 0), 1, 1, color='yellow', label='Start Point'),
        plt.Rectangle((0, 0), 1, 1, color='blue', label='Closest Spots')
    ]
    plt.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.tight_layout()
    plt.show()



def visualize_route_on_parking_grid(grid: List[List[int]], 
                                    start: Tuple[int, int], 
                                    route: List[Tuple[int, int]]):
    """
    Visualize the parking grid with the route from the start point to a parking spot.
    
    :param grid: 2D list representing the parking area (0 for empty, 1 for occupied)
    :param start: Starting coordinates (row, col)
    :param route: List of coordinates representing the route
    """
    rows, cols = len(grid), len(grid[0])

    # Create a color grid
    color_grid = np.zeros((rows, cols, 3))

    # Color coding
    # Occupied spots: Red
    # Empty spots: Green
    # Start point: Yellow
    # Route: Purple
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 1:  # Occupied
                color_grid[row, col] = [1, 0, 0]  # Red
            else:  # Empty
                color_grid[row, col] = [0, 1, 0]  # Green

    # Mark start point
    color_grid[start[0], start[1]] = [1, 1, 0]  # Yellow

    # Mark the route
    for row, col in route:
        color_grid[row, col] = [0.5, 0, 0.5]  # Purple for the route

    # Plotting
    plt.figure(figsize=(10, 8))
    plt.imshow(color_grid)
    plt.title(f"Parking Grid - Route from {start} to {route[-1]}")

    # Add grid lines
    for x in range(cols + 1):
        plt.axvline(x - 0.5, color='black', linewidth=1)
    for y in range(rows + 1):
        plt.axhline(y - 0.5, color='black', linewidth=1)

    # Add spot coordinates
    for row in range(rows):
        for col in range(cols):
            plt.text(col, row, f"({row},{col})", 
                     ha='center', va='center', color='white', fontsize=8)

    plt.xticks(range(cols))
    plt.yticks(range(rows))
    plt.grid(False)

    # Add a legend
    legend_elements = [
        plt.Rectangle((0, 0), 1, 1, color='red', label='Occupied'),
        plt.Rectangle((0, 0), 1, 1, color='green', label='Empty'),
        plt.Rectangle((0, 0), 1, 1, color='yellow', label='Start Point'),
        plt.Rectangle((0, 0), 1, 1, color='purple', label='Route')
    ]
    plt.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5))

    plt.tight_layout()
    plt.show()
