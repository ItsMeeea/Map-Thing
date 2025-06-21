import pandas as pd
import networkx as nx
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import deque
import heapq

# === 1. Load adjacency matrix from Excel (no headers) ===
df = pd.read_excel('adjacency.xlsx', header=None)
adjacency_matrix = df.values  # should be a 37×37 array

# === 2. Hard-coded 37 labels ===
labels = [
    'A','B','C','D','E','F','G','H','I','J','K','L','M',
    'AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','AT',
    'BA','BB','BC','BD'
]

# === 3. Static heuristic values (must match len(labels)=37) ===
heuristic_list = [
    5.0, 4.5, 3.0, 3.0, 3.0, 4.8, 3.0, 5.0, 3.0, 4.0, 3.0, 3.0, 3.0,
    4.7, 3.9, 4.0, 4.0, 3.0, 4.0, 5.0, 4.0, 3.0, 4.9, 4.8, 4.2, 4.0,
    4.0, 3.0, 4.2, 3.0, 4.0, 3.0, 3.9, 3.0, 3.0, 3.0, 3.0
]
heuristics = {lab: h for lab, h in zip(labels, heuristic_list)}

# === 4. Graph builders ===
def build_graph_unweighted():
    g = {u: [] for u in labels}
    for i, u in enumerate(labels):
        for j, v in enumerate(labels):
            if adjacency_matrix[i][j] > 0:
                g[u].append(v)
    return g

def build_graph_weighted():
    g = {u: [] for u in labels}
    for i, u in enumerate(labels):
        for j, v in enumerate(labels):
            w = adjacency_matrix[i][j]
            if w > 0:
                g[u].append((v, w))
    return g

# === 5. BFS (blind) ===
def blind_search(start, end):
    graph = build_graph_unweighted()
    visited = set()
    queue = deque([[start]])
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == end:
            return path
        if node not in visited:
            visited.add(node)
            for nbr in graph[node]:
                queue.append(path + [nbr])
    return None

# === 6. A* (heuristic) ===
def heuristic_search(start, goal):
    graph = build_graph_weighted()
    open_set = []
    g_score = {start: 0}
    f_score = {start: heuristics[start]}
    parent = {start: None}
    heapq.heappush(open_set, (f_score[start], start))

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current:
                path.insert(0, current)
                current = parent[current]
            return path
        for neighbor, cost in graph[current]:
            tentative_g = g_score[current] + cost
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                parent[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristics.get(neighbor, 0)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return None

# === 7. GUI & drawing ===
def run_gui():
    # Build the NetworkX graph
    G = nx.DiGraph()
    for i, u in enumerate(labels):
        for j, v in enumerate(labels):
            w = adjacency_matrix[i][j]
            if w > 0:
                G.add_edge(u, v, weight=w)

    # Fixed positions for plotting
    pos = {
        "A": (12,-5), "B":(-3,1), "C":(-12,-1), "D":(-6,0),  "E":(3,-3),
        "F":(-8,-7), "G":(-6,-2), "H":(-13,-6),"I":(-1,-2), "J":(12,0),
        "K":(10,0),  "L":(-4,-6), "M":(-8,-1), "AA":(-2,-7),"AB":(3,4),
        "AC":(-1,-7),"AD":(15,-3),"AE":(0,-7), "AF":(-7,3), "AG":(-5.5,3),
        "AH":(4,4),  "AI":(5,4),   "AJ":(-4,3),  "AK":(-2.5,3),"AL":(12,-7),
        "AM":(6,4),  "AN":(7,4),   "AO":(1,-7),  "AP":(-15,-4),"AQ":(-1,3),
        "AR":(12,4), "AS":(8,4),   "AT":(2,-7),  "BA":(5,0),   "BB":(2,-1),
        "BC":(1,-5), "BD":(9,-2)
    }

    # Build UI
    root = tk.Tk()
    root.title("Path Finder: BFS & A*")
    root.geometry("1200x800")  # Window size

    frm = tk.Frame(root)
    frm.pack(pady=5)

    tk.Label(frm, text="Start:").grid(row=0, column=0)
    start_var = tk.StringVar(value=labels[0])
    ttk.Combobox(frm, textvariable=start_var, values=labels, width=5)\
        .grid(row=0, column=1, padx=5)

    tk.Label(frm, text="End:").grid(row=0, column=2)
    end_var = tk.StringVar(value=labels[-1])
    ttk.Combobox(frm, textvariable=end_var, values=labels, width=5)\
        .grid(row=0, column=3, padx=5)

    result_lbl = tk.Label(frm, text="", justify='left')
    result_lbl.grid(row=1, column=0, columnspan=5, sticky='w')

    # —— HERE’S THE ONLY CHANGE: a more rectangular canvas
    fig, ax = plt.subplots(figsize=(18, 6))      # ← width=18, height=6
    fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    def draw(bfs_path=None, astar_path=None):
        ax.clear()

        # Base node colors
        node_colors = []
        for node in G.nodes():
            if node in labels[:13]:       # A–M
                node_colors.append("lightgreen")
            elif node in labels[13:33]:   # AA–AT
                node_colors.append("deepskyblue")
            else:
                node_colors.append("white")

        nx.draw_networkx_nodes(
            G, pos,
            node_color=node_colors,
            ax=ax,
            node_size=500,
            edgecolors='black'
        )
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=10)
        nx.draw_networkx_edges(G, pos, edge_color="gray", ax=ax, arrows=False)
        nx.draw_networkx_edge_labels(
            G, pos,
            edge_labels={(u, v): d["weight"] for u, v, d in G.edges(data=True)},
            ax=ax, font_size=8
        )

        # BFS in red
        if bfs_path:
            bfs_edges = list(zip(bfs_path, bfs_path[1:]))
            nx.draw_networkx_nodes(
                G, pos,
                nodelist=bfs_path,
                node_color="red",
                ax=ax,
                node_size=500,
                edgecolors='black'
            )
            nx.draw_networkx_edges(
                G, pos,
                edgelist=bfs_edges,
                edge_color="red",
                width=3,
                ax=ax,
                arrows=True
            )

        # A* in yellow
        if astar_path:
            astar_edges = list(zip(astar_path, astar_path[1:]))
            nx.draw_networkx_nodes(
                G, pos,
                nodelist=astar_path,
                node_color="yellow",
                ax=ax,
                node_size=500,
                edgecolors='black'
            )
            nx.draw_networkx_edges(
                G, pos,
                edgelist=astar_edges,
                edge_color="yellow",
                width=3,
                ax=ax,
                arrows=True
            )

        canvas.draw()

    def on_find():
        s, e = start_var.get(), end_var.get()
        bfs_p = blind_search(s, e)
        ast_p = heuristic_search(s, e)

        # Calculate costs and steps
        if bfs_p:
            bfs_cost = sum(
                adjacency_matrix[labels.index(bfs_p[i])][labels.index(bfs_p[i+1])]
                for i in range(len(bfs_p)-1)
            )
            bfs_steps = len(bfs_p)-1
            bfs_text = f"BFS → {'→'.join(bfs_p)} (steps: {bfs_steps}, cost: {bfs_cost})"
        else:
            bfs_text = "BFS → No path found"

        if ast_p:
            ast_cost = sum(
                adjacency_matrix[labels.index(ast_p[i])][labels.index(ast_p[i+1])]
                for i in range(len(ast_p)-1)
            )
            ast_steps = len(ast_p)-1
            ast_text = f"A*  → {'→'.join(ast_p)} (steps: {ast_steps}, cost: {ast_cost})"
        else:
            ast_text = "A*  → No path found"

        result_lbl.config(text=f"{bfs_text}\n{ast_text}")
        draw(bfs_p, ast_p)

    tk.Button(frm, text="Find Path", command=on_find)\
        .grid(row=0, column=4, padx=5)

    draw()
    root.mainloop()

if __name__ == '__main__':
    run_gui()
