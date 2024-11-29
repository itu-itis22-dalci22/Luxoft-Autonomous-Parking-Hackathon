import numpy as np
from typing import List, Tuple
from collections import deque
import random

class ParkingSpotFinder:
    def __init__(self, parking_grid: List[List[int]]):
        """
        Initialize the parking spot finder with a 2D grid.
        
        :param parking_grid: 2D list representing the parking area
        0 represents an empty spot, 1 represents an occupied spot
        """

        # Validate input grid
        check_cols = len(set(len(row) for row in parking_grid))
        if check_cols != 1:
            raise ValueError("Invalid parking grid: Rows have different lengths")
        
        # Check grid values
        for row in parking_grid:
            for val in row:
                if val not in (0, 1):
                    raise ValueError("Invalid parking grid: Values should be 0 or 1")
        
        self.grid = parking_grid
        self.rows = len(parking_grid)
        self.cols = len(parking_grid[0])
    
    def find_closest_parking_spots(self, start: Tuple[int, int]) -> List[Tuple[int, int, int]]:
        """
        Find all closest empty parking spots using Breadth-First Search.
        
        :param start: Starting coordinates (row, col)
        :return: List of tuples (row, col, distance) of the closest empty spots
        """
        # Validate start position
        if not self._is_valid_position(start[0], start[1]):
            raise ValueError("Invalid starting position")
        
        # Directions for movement (up, right, down, left)
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        # Shuffle the directions randomly to change the order of exploration
        random.shuffle(directions)

        # Queue for BFS
        queue = deque([(start[0], start[1], 0)])
        
        # Tracking visited positions to avoid revisiting
        visited = set([(start[0], start[1])])
        
        # Store closest parking spots
        closest_spots = []
        min_distance = float('inf')
        
        while queue:
            current_row, current_col, distance = queue.popleft()
            
            # If we've found spots and current distance is greater than min, stop searching
            if closest_spots and distance > min_distance:
                break
            
            # Check if current spot is empty
            if self.grid[current_row][current_col] == 0:
                # If this is a new minimum distance, clear previous spots
                if distance < min_distance:
                    closest_spots = [(current_row, current_col, distance)]
                    min_distance = distance
                # If this is at the same minimum distance, add to the list
                elif distance == min_distance:
                    closest_spots.append((current_row, current_col, distance))
            
            # Explore neighboring cells
            for dx, dy in directions:
                new_row, new_col = current_row + dx, current_col + dy
                
                # Check if new position is valid and not visited
                if (self._is_valid_position(new_row, new_col) and 
                    (new_row, new_col) not in visited):
                    queue.append((new_row, new_col, distance + 1))
                    visited.add((new_row, new_col))
        
        return closest_spots
    
    def find_route_to_parking_spot(self, start: Tuple[int, int], target: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Find the shortest route from the start to the target parking spot.
        
        :param start: Starting coordinates (row, col)
        :param target: Target parking spot coordinates (row, col)
        :return: List of tuples representing the route (row, col)
        """
        if not (self._is_valid_position(*start) and self._is_valid_position(*target)):
            raise ValueError("Invalid start or target position")
        
        # Directions for movement (up, right, down, left)
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        # Queue for BFS with path tracking
        queue = deque([(start, [])])  # Each entry is (current_position, path_so_far)
        visited = set([start])
        
        while queue:
            current, path = queue.popleft()
            
            # Check if we've reached the target
            if current == target:
                return path + [target]
            
            for dx, dy in directions:
                new_row, new_col = current[0] + dx, current[1] + dy
                new_pos = (new_row, new_col)
                
                if self._is_valid_position(new_row, new_col) and new_pos not in visited:
                    visited.add(new_pos)
                    queue.append((new_pos, path + [current]))
        
        # Return an empty path if no route is found
        return []
    
    def _is_valid_position(self, row: int, col: int) -> bool:
        """
        Check if the given position is within the grid bounds.
        
        :param row: Row index
        :param col: Column index
        :return: Boolean indicating if position is valid
        """
        return (0 <= row < self.rows and 
                0 <= col < self.cols)