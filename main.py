import tkinter as tk
from tkinter import messagebox
import heapq
import math
import random
import time
def manhattan(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) 
def euclidean(pos1, pos2):
    return math.hypot(pos1[0] - pos2[0], pos1[1] - pos2[1])  
class Node:
    def __init__(self, position, g=0, h=0, parent=None, f=None):
        self.position = position  # cell location
        self.g = g  # cost from start
        self.h = h  # guess to goal
        self.parent = parent  # previous cell
        self.f = f if f is not None else g + h  # total score
    def __lt__(self, other):
        return self.f < other.f  #  priority queue
class PathfindingGUI:
    def __init__(self, root, rows, cols, start, goal, obstacles, algo, heuristic_func):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.start = start  # starting cell
        self.goal = goal  # ending cell
        self.obstacles = set(obstacles)  # blocked cells
        self.algo = algo  # A* or GBFS
        self.heuristic = heuristic_func
        self.cell_size = 30
        self.canvas_width = cols * self.cell_size
        self.canvas_height = rows * self.cell_size
        self.edit_mode = 'wall'  
        self.visited = set()
        self.frontier_set = set()
        self.path = []
        self.colors = {
            'empty': '#FFFFFF',
            'wall': '#2d3436',
            'start': '#ffeb3b',
            'goal': '#9c27b0',
            'visited': '#81d4fa',
            'frontier': '#fff176',
            'path': '#4caf50'
        }
        root.title("Dynamic Pathfinding Agent")
        root.configure(bg="#f5f5f5")
        top_frame = tk.Frame(root, bg="#37474f", height=40)
        top_frame.pack(fill=tk.X)
        self.status_label = tk.Label(
            top_frame,
            text="Visited: 0 | Cost: 0 | Time: 0 ms",
            fg="white", bg="#37474f", font=("Arial", 11, "bold")
        )
        self.status_label.pack(pady=8)
        main_content = tk.Frame(root, bg="#f5f5f5")
        main_content.pack(fill=tk.BOTH, expand=True)
        left = tk.Frame(main_content, width=220, bg="#455a64", padx=10, pady=10)
        left.pack(side=tk.LEFT, fill=tk.Y)
        left.pack_propagate(False)
        tk.Label(left, text="Controls", font=("Arial", 12, "bold"), fg="white", bg="#455a64").pack(pady=(0, 10))
        
        buttons_info = [
            ("Start Mode", lambda: self.set_edit_mode('start')),
            ("Goal Mode", lambda: self.set_edit_mode('goal')),
            ("Wall Mode", lambda: self.set_edit_mode('wall')),
            ("Random", self.add_random_obstacles),
            ("Start Search", self.find_path),
            ("Clear", self.clear_obstacles),
            ("Reset", self.reset_viz)
        ]
        
        for text, cmd in buttons_info:
            tk.Button(
                left,
                text=text,
                command=cmd,
                bg="#546e7a",
                fg="white",
                font=("Arial", 10, "bold"),
                relief="flat",
                activebackground="#455a64",
                width=15,
                pady=6
            ).pack(fill=tk.X, pady=5)

        self.canvas = tk.Canvas(
            main_content,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="#eceff1",
            highlightthickness=0
        )
        self.canvas.pack(side=tk.RIGHT, padx=15, pady=15)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.draw_grid()
    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                if (r, c) in self.obstacles:
                    color = self.colors['wall']
                elif (r, c) == self.start:
                    color = self.colors['start']
                elif (r, c) == self.goal:
                    color = self.colors['goal']
                else:
                    color = self.colors['empty']
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#b0bec5", width=1)
    def update_cell(self, r, c, color_key):
        x1 = c * self.cell_size
        y1 = r * self.cell_size
        self.canvas.create_rectangle(
            x1, y1,
            x1 + self.cell_size, y1 + self.cell_size,
            fill=self.colors[color_key],
            outline="#b0bec5", width=1
        )
    def on_canvas_click(self, event):
        c = event.x // self.cell_size
        r = event.y // self.cell_size
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return
        pos = (r, c)
        if self.edit_mode == 'wall':
            if pos != self.start and pos != self.goal:
                self.obstacles.add(pos)
                self.update_cell(r, c, 'wall')
        elif self.edit_mode == 'start':
            if pos not in self.obstacles and pos != self.goal:
                self.start = pos
                self.draw_grid()
        elif self.edit_mode == 'goal':
            if pos not in self.obstacles and pos != self.start:
                self.goal = pos
                self.draw_grid()
    
