from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QLabel, QMessageBox, QSpinBox, QDialog, QFileDialog, QGraphicsView, QGraphicsScene, QGraphicsRectItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtGui import QPainter
import pandas as pd
import random
from bfs_parking import ParkingSpotFinder
from visualizations import visualize_parking_grid, visualize_route_on_parking_grid
import sys


class ParkingGridFinder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parking Grid Finder")
        self.setGeometry(100, 100, 1000, 800)
        
        # Grid parameters
        self.rows = 10
        self.cols = 10
        self.cell_size = 40  # Size of each grid cell in pixels
        
        # Initialize grid with all empty spots
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.start_point = None
        
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Controls layout
        controls_layout = QHBoxLayout()
        main_layout.addLayout(controls_layout)
        
        # Buttons
        buttons = [
            ("Set Grid Size", self.set_grid_size),
            ("Load CSV Grid", self.load_csv_grid),
            ("Randomize Grid", self.randomize_grid),
            ("Set Start Point", self.set_start_point),
            ("Find Closest Spots", self.find_closest_spots),
            ("Zoom In", lambda: self.zoom(1.2)),
            ("Zoom Out", lambda: self.zoom(0.8))
        ]
        
        for text, method in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(method)
            controls_layout.addWidget(btn)
        
        # Occupancy rate input
        occupancy_layout = QHBoxLayout()
        main_layout.addLayout(occupancy_layout)
        occupancy_label = QLabel("Occupancy Rate (%):")
        self.occupancy_input = QLineEdit()
        self.occupancy_input.setText("30")
        occupancy_layout.addWidget(occupancy_label)
        occupancy_layout.addWidget(self.occupancy_input)
        
        # Graphics view for grid
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        main_layout.addWidget(self.view)
        
        # Create initial grid
        self.create_grid()
    
    def create_grid(self):
        """
        Create the grid representation in the scene.
        """
        self.scene.clear()
        self.grid_items = []
        
        for row in range(self.rows):
            row_items = []
            for col in range(self.cols):
                rect = QGraphicsRectItem(
                    col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                rect.setPen(Qt.black)
                self.scene.addItem(rect)
                row_items.append(rect)
            self.grid_items.append(row_items)
        
        self.update_grid_colors()
        self.view.setSceneRect(0, 0, self.cols * self.cell_size, self.rows * self.cell_size)
    
    def update_grid_colors(self):
        """
        Update the colors of the grid cells based on their state.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid_items[row][col]
                if self.start_point and (row, col) == self.start_point:
                    cell.setBrush(QBrush(QColor("yellow")))
                elif self.grid[row][col] == 1:
                    cell.setBrush(QBrush(QColor("red")))
                else:
                    cell.setBrush(QBrush(QColor("green")))
    
    def toggle_spot(self, row, col):
        """
        Toggle the state of a grid spot.
        """
        if self.start_point and (row, col) == self.start_point:
            QMessageBox.information(self, "Info", "Cannot modify start point")
            return
        self.grid[row][col] = 1 - self.grid[row][col]
        self.update_grid_colors()
    
    def zoom(self, factor):
        """
        Zoom the grid view.
        """
        self.view.scale(factor, factor)
    
    def set_grid_size(self):
        """
        Allow user to set custom grid size.
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("Set Grid Size")
        layout = QVBoxLayout(dialog)
        
        rows_layout = QHBoxLayout()
        rows_label = QLabel("Rows:")
        rows_spin = QSpinBox()
        rows_spin.setRange(3, 100)
        rows_spin.setValue(self.rows)
        rows_layout.addWidget(rows_label)
        rows_layout.addWidget(rows_spin)
        
        cols_layout = QHBoxLayout()
        cols_label = QLabel("Columns:")
        cols_spin = QSpinBox()
        cols_spin.setRange(3, 100)
        cols_spin.setValue(self.cols)
        cols_layout.addWidget(cols_label)
        cols_layout.addWidget(cols_spin)
        
        layout.addLayout(rows_layout)
        layout.addLayout(cols_layout)
        
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        def accept():
            self.rows = rows_spin.value()
            self.cols = cols_spin.value()
            self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
            self.start_point = None
            self.create_grid()
            dialog.accept()
        
        ok_btn.clicked.connect(accept)
        cancel_btn.clicked.connect(dialog.reject)
        dialog.exec_()
    
    def load_csv_grid(self):
        """
        Load parking grid from a CSV file.
        """
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV Grid File", "", "CSV Files (*.csv)")
            if not file_path:
                return
            
            df = pd.read_csv(file_path, header=None)
            grid_data = df.values.tolist()
            
            for row in grid_data:
                for val in row:
                    if val not in (0, 1):
                        raise ValueError("CSV must contain only 0 and 1")
            
            self.grid = grid_data
            self.rows = len(grid_data)
            self.cols = len(grid_data[0])
            self.start_point = None
            self.create_grid()
            QMessageBox.information(self, "Success", "CSV grid loaded successfully")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def randomize_grid(self):
        """
        Randomize grid occupancy.
        """
        try:
            occupancy_rate = float(self.occupancy_input.text())
            if not (0 <= occupancy_rate <= 100):
                raise ValueError("Occupancy rate must be between 0 and 100")
            
            num_occupied = int(self.rows * self.cols * occupancy_rate / 100)
            all_coords = [(r, c) for r in range(self.rows) for c in range(self.cols)]
            occupied_coords = random.sample(all_coords, num_occupied)
            
            self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
            for r, c in occupied_coords:
                self.grid[r][c] = 1
            
            self.start_point = None
            self.update_grid_colors()
            QMessageBox.information(self, "Success", f"Grid randomized with {occupancy_rate}% occupancy")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def set_start_point(self):
        """
        Set the start point on the grid.
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("Set Start Point")
        layout = QVBoxLayout(dialog)
        
        rows_spin = QSpinBox()
        rows_spin.setRange(0, self.rows - 1)
        cols_spin = QSpinBox()
        cols_spin.setRange(0, self.cols - 1)
        
        layout.addWidget(QLabel("Row:"))
        layout.addWidget(rows_spin)
        layout.addWidget(QLabel("Column:"))
        layout.addWidget(cols_spin)
        
        btn = QPushButton("Set Start Point")
        layout.addWidget(btn)
        
        def accept():
            row = rows_spin.value()
            col = cols_spin.value()
            
            self.start_point = (row, col)
            self.update_grid_colors()
            dialog.accept()
        
        btn.clicked.connect(accept)
        dialog.exec_()
    
    def find_closest_spots(self):
        """Find and display the closest parking spots."""
        if not self.start_point:
            QMessageBox.warning(self, "Error", "Please set a start point first.")
            return
        
        # Create the finder object
        finder = ParkingSpotFinder(self.grid)
        
        # Find closest spots
        closest_spots = finder.find_closest_parking_spots(self.start_point)
        
        # If no closest spots found, display a message and return
        if not closest_spots:
            QMessageBox.information(self, "No Spots Found", "No empty parking spots found.")
            return
        
        # Create a formatted string to display the closest spots and their distances
        closest_spots_info = "\n".join([f"Spot: ({spot[0]},{spot[1]}), Distance: {spot[2]}" for spot in closest_spots])
        
        # Show closest spots and their distances in a message box
        QMessageBox.information(self, "Closest Parking Spots", f"The closest parking spots are:\n\n{closest_spots_info}")
        
        # Visualize the parking grid with the closest spots highlighted
        visualize_parking_grid(self.grid, self.start_point, closest_spots)
        
        # Optionally, find the route to the first closest spot and visualize it
        route = finder.find_route_to_parking_spot(self.start_point, closest_spots[0][:2])
        visualize_route_on_parking_grid(self.grid, self.start_point, route)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ParkingGridFinder()
    window.show()
    sys.exit(app.exec_())