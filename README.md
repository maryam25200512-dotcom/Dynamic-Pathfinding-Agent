# Dynamic Pathfinding Agent

## Project Overview
This project implements a Dynamic Pathfinding Agent that navigates a grid-based environment using informed search algorithms.

The agent finds a path from a Start Node to a Goal Node using:
- A* Search
- Greedy Best-First Search (GBFS)

The application visualizes:
- Visited nodes
- Frontier nodes
- Final optimal path
- Performance metrics in real time

---

## Features
- Dynamic grid sizing (user defines rows and columns)
- Start and goal nodes
- Random obstacle generation with adjustable density
- Interactive map editor (add/remove walls by clicking)
- Support for two heuristic functions:
  - Manhattan Distance
  - Euclidean Distance
- Visualization of search process
- Real-time metrics dashboard:
  - Nodes visited
  - Path cost
  - Execution time

---

## Algorithms Implemented

### 1. A* Search
Uses the evaluation function:
f(n) = g(n) + h(n)

Where:
- g(n) = cost from start node
- h(n) = heuristic estimate to goal

### 2. Greedy Best-First Search (GBFS)
Uses:
f(n) = h(n)

This algorithm selects nodes based only on the heuristic value.

---

## Heuristics

Manhattan Distance  
|x1 - x2| + |y1 - y2|

Euclidean Distance  
√((x1 - x2)² + (y1 - y2)²)

---

## Technologies Used
- Python
- Tkinter (GUI)
- Jupyter Notebook

---

## Installation

1. Install Python (version 3.8 or higher recommended).

2. Install required libraries (if needed):

pip install tkinter

Note: Tkinter is usually pre-installed with Python.

---

## How to Run the Project

### Option 1: Run in Jupyter Notebook
1. Open Jupyter Notebook.
2. Open the project notebook file.
3. Run the cells.
4. Enter the following when prompted:
   - Grid rows
   - Grid columns
   - Obstacle density
   - Algorithm (A for A*, G for GBFS)
   - Heuristic (M for Manhattan, E for Euclidean)

The GUI window will open automatically.

### Option 2: Run as a Python Script

python main.py

Then follow the prompts in the terminal.

---

## GUI Controls

Start Mode  
Set the start node on the grid.

Goal Mode  
Set the goal node.

Wall Mode  
Add obstacles on the grid.

Random  
Generate random obstacles.

Start Search  
Run the selected pathfinding algorithm.

Clear  
Remove all obstacles.

Reset  
Reset the visualization.

---

## Visualization Details

The GUI highlights:
- Frontier Nodes: nodes currently in the priority queue
- Visited Nodes: explored nodes
- Final Path: optimal path from start to goal

It also displays:
- Total nodes visited
- Path cost
- Execution time 




