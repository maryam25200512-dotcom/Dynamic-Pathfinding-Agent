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
    def set_edit_mode(self, mode):
        self.edit_mode = mode
    def add_random_obstacles(self):
        self.obstacles.clear()
        for r in range(self.rows):
            for c in range(self.cols):
                if random.random() < 0.15 and (r, c) != self.start and (r, c) != self.goal:
                    self.obstacles.add((r, c))
        self.draw_grid()
        self.reset_viz()
    def clear_obstacles(self):
        self.obstacles.clear()
        self.draw_grid()
        self.reset_viz()
    def reset_viz(self):
        self.visited.clear()
        self.frontier_set.clear()
        self.path = []
        self.draw_grid()
        self.update_metrics(0, 0, 0)
    def get_heuristic(self, pos):
        return self.heuristic(pos, self.goal)
    def get_neighbors(self, pos):
        r, c = pos
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and (nr, nc) not in self.obstacles:
                neighbors.append((nr, nc))
        return neighbors
    def informed_search(self, start_pos, goal_pos, use_g=True):
        if start_pos == goal_pos:
            return [start_pos], 0, 1, {start_pos}, set()
        open_set = []
        open_set_pos = {start_pos}
        start_h = self.get_heuristic(start_pos)
        start_f = (0 + start_h) if use_g else start_h
        start_node = Node(start_pos, 0, start_h, None, start_f)
        heapq.heappush(open_set, start_node)
        came_from = {}
        g_score = {start_pos: 0}
        closed_set = set()
        expanded = 0
        while open_set:
            current = heapq.heappop(open_set)
            open_set_pos.discard(current.position)
            if current.position in closed_set:
                continue
            closed_set.add(current.position)
            expanded += 1
            if current.position == goal_pos:
                path = []
                curr = current
                while curr:
                    path.append(curr.position)
                    curr = curr.parent
                return path[::-1], current.g, expanded, closed_set.copy(), open_set_pos.copy()
            for neigh in self.get_neighbors(current.position):
                tentative_g = current.g + 1
                if neigh not in g_score or tentative_g < g_score[neigh]:
                    came_from[neigh] = current
                    g_score[neigh] = tentative_g
                    h = self.get_heuristic(neigh)
                    f = (tentative_g + h) if use_g else h
                    neigh_node = Node(neigh, tentative_g, h, current, f)
                    heapq.heappush(open_set, neigh_node)
                    open_set_pos.add(neigh)
        return None, 0, expanded, closed_set, open_set_pos
    def find_path(self):
        self.reset_viz()
        start_time = time.time()
        use_g = (self.algo == 'A*')
        result = self.informed_search(self.start, self.goal, use_g)
        if result[0] is None:
            messagebox.showerror("No Path", "No path found!")
            self.update_metrics(0, 0, 0)
            return
        path, cost, expanded, closed, frontier = result
        exec_time = round((time.time() - start_time) * 1000, 2)
        self.path = path
        self.visited = closed
        self.frontier_set = frontier
        self.update_metrics(expanded, cost, exec_time)
        self.color_search_results()
    def color_search_results(self):
        self.draw_grid()
        for r, c in self.visited:
            if (r, c) != self.start and (r, c) != self.goal and (r, c) not in self.path:
                self.update_cell(r, c, 'visited')
        for r, c in self.frontier_set:
            if (r, c) != self.start and (r, c) != self.goal and (r, c) not in self.path and (r, c) not in self.visited:
                self.update_cell(r, c, 'frontier')
        for r, c in self.path:
            if (r, c) != self.start and (r, c) != self.goal:
                self.update_cell(r, c, 'path')
        self.update_cell(self.start[0], self.start[1], 'start')
        self.update_cell(self.goal[0], self.goal[1], 'goal')
    def update_metrics(self, nodes, cost, etime):
        text = f"Visited: {nodes} | Cost: {cost} | Time: {etime:.2f} ms"
        self.status_label.config(text=text)
if __name__ == "__main__":
    print("Informed Search")
    rows = int(input("Rows: "))
    cols = int(input("Cols: "))
    density = float(input("Density (0-1): "))   
    while True: # Algorithm input with loop until valid
        algo_input = input("Algo (A/G): ").strip().upper()
        if algo_input in ["A", "G"]:
            break
        print("Invalid algorithm! Please use A (for A*) or G (for GBFS).")  
    while True:
        heu_input = input("Heuristic (M/E): ").strip().upper()
        if heu_input in ["M", "E"]:
            break
        print("Invalid heuristic! Please use M (Manhattan) or E (Euclidean).")
    algo = "A*" if algo_input == "A" else "GBFS"
    heuristic_func = manhattan if heu_input == "M" else euclidean
    start = (0, 0)
    goal = (rows - 1, cols - 1)
    obstacles = set()
    for r in range(rows):
        for c in range(cols):
            if (r, c) != start and (r, c) != goal and random.random() < density:
                obstacles.add((r, c))
    print("Dynamic Pathfinding Loading..")
    root = tk.Tk()
    app = PathfindingGUI(root, rows, cols, start, goal, obstacles, algo, heuristic_func)
    root.mainloop()