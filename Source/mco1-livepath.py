import pandas as pd
import networkx as nx
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import deque
import heapq
import textwrap

# === 1. Load your two Excel files ===
conn_df   = pd.read_excel("connections.xlsx", header=None, engine="openpyxl")
dist_df   = pd.read_excel("distances.xlsx",   header=None, engine="openpyxl")
conn      = conn_df.values    # 37×37 of 0/1
distances = dist_df.values    # 37×37 of distances

# === 2. Full-names map & labels list ===
letter_names = {
    "A":  "Andrew – Br. Andrew Gonzales Hall",
    "B":  "Bloemen – Br. Alphonsus Bloemen Hall",
    "C":  "Connon – Br. Gabriel Connon Hall",
    "D":  "Faculty Center",
    "E":  "Gokongwei – John Gokongwei Sr. Hall",
    "F":  "Henry Sy Sr. Hall",
    "G":  "St. Joseph Hall",
    "H":  "St. La Salle Hall",
    "I":  "St. Miguel Febres Cordero Hall",
    "J":  "Razon – Enrique M. Razon Sports Center",
    "K":  "Science & Technology Research Center",
    "L":  "Velasco – Urbano J. Velasco Hall",
    "M":  "Yuchengco – Don Enrique T. Yuchengco Hall",
    "AA": "24 Chicken",        "AB": "Ate Rica’s Bacsilog",
    "AC": "Bab",               "AD": "The Barn",
    "AE": "BBQ Nation",        "AF": "Chef Bab’s House of Sisig",
    "AG": "Colonel’s Curry",   "AH": "Good Munch",
    "AI": "Gyuniku",           "AJ": "Happy N’ Healthy (Bloomen)",
    "AK": "The Hungry Pita",   "AL": "Kitchen City",
    "AM": "Kuya Mel Kitchen",  "AN": "Lumpia.natics",
    "AO": "Master Chop",       "AP": "McDonald’s",
    "AQ": "Mongolian Master",  "AR": "Perico’s Grill",
    "AS": "Tapa Loca",         "AT": "Tori Box",
    "BA": "Agno Food Court",   "BB": "Agno St.",
    "BC": "EGI Taft Tower",    "BD": "Fidel A. Reyes St."
}
labels = list(letter_names.keys())
name_to_code = { fullname: code for code, fullname in letter_names.items() }
full_names   = list(letter_names.values())

# === 3. Build adjacency ===
def build_graph_unweighted():
    g = {u: [] for u in labels}
    for i,u in enumerate(labels):
        for j,v in enumerate(labels):
            if conn[i,j] == 1:
                g[u].append(v)
    return g

def build_graph_weighted():
    g = {u: [] for u in labels}
    for i,u in enumerate(labels):
        for j,v in enumerate(labels):
            if conn[i,j] == 1:
                g[u].append((v, float(distances[i,j])))
    return g

# === 4. A* generator (heuristic) ===
def heuristic_search_generator(start, goal):
    graph = build_graph_weighted()
    goal_idx = labels.index(goal)
    hvals = {labels[i]: float(distances[i,goal_idx]) for i in range(len(labels))}
    open_set = []
    g_score = {start:0.0}
    f_score = {start:hvals[start]}
    parent  = {start:None}
    heapq.heappush(open_set,(f_score[start],start))
    while open_set:
        _,current = heapq.heappop(open_set)
        yield ("visit", current)
        if current==goal:
            path=[]
            while current:
                path.insert(0,current)
                current=parent[current]
            yield ("done", path)
            return
        for neigh,c in graph[current]:
            tg = g_score[current]+c
            if neigh not in g_score or tg<g_score[neigh]:
                parent[neigh]=current
                g_score[neigh]=tg
                f_score[neigh]=tg+hvals[neigh]
                heapq.heappush(open_set,(f_score[neigh],neigh))

# === 5. BFS generator (blind) ===
def blind_search_generator(start, end):
    graph = build_graph_unweighted()
    visited = set()
    queue = deque([[start]])
    while queue:
        path = queue.popleft()
        node = path[-1]
        yield ("visit", node)
        if node == end:
            yield ("done", path)
            return
        if node not in visited:
            visited.add(node)
            for nbr in graph[node]:
                queue.append(path + [nbr])

# === 6. GUI ===
def run_gui():
    G = nx.DiGraph()
    for u in labels:
        for v,w in build_graph_weighted()[u]:
            G.add_edge(u,v,weight=w)

    # fixed positions
    pos = {
        "A":  (12,-5),   "B":(-3,1),    "C":(-12,-1), "D":(-6,0),
        "E":  (3,-3),    "F":(-8,-7),   "G":(-6,-2),  "H":(-13,-6),
        "I":  (-1,-2),   "J":(12,0),    "K":(10,0),   "L":(-4,-6),
        "M":  (-8,-1),   "AA":(-2,-7),  "AB":(3,4),   "AC":(-1,-7),
        "AD": (15,-3),   "AE":(0,-7),   "AF":(-7,3),  "AG":(-5.5,3),
        "AH": (4,4),     "AI":(5,4),    "AJ":(-4,3),  "AK":(-2.5,3),
        "AL": (12,-7),   "AM":(6,4),    "AN":(7,4),   "AO":(1,-7),
        "AP": (-15,-4),  "AQ":(-1,3),   "AR":(12,4),  "AS":(8,4),
        "AT": (2,-7),    "BA":(5,0),    "BB":(2,-1),  "BC":(1,-5),
        "BD": (9,-2)
    }

    root = tk.Tk()
    root.title("Live Pathfinding (A* and BFS)")
    root.geometry("1400x940")

    frm = tk.Frame(root)
    frm.pack(pady=10)

    # Start selector
    ttk.Label(frm, text="Start:").grid(row=0, column=0)
    sv = tk.StringVar(value=full_names[0])
    ttk.Combobox(frm, textvariable=sv, values=full_names, width=40)\
        .grid(row=0, column=1, padx=5)

    # End selector
    ttk.Label(frm, text="End:").grid(row=0, column=2)
    ev = tk.StringVar(value=full_names[-1])
    end_cb = ttk.Combobox(frm, textvariable=ev, values=full_names, width=40)
    end_cb.grid(row=0, column=3, padx=5)
    end_cb.bind("<<ComboboxSelected>>", lambda _: draw())


    status_var = tk.StringVar()
    status_lbl = ttk.Label(frm, textvariable=status_var, background="#f2f2f2", font=("Segoe UI", 10))
    status_lbl.grid(row=1, column=0, columnspan=6, sticky="w", pady=5)

    fig,ax = plt.subplots(figsize=(20,10))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_position([0, 0, 1, 1])  

    visited_nodes = set()

    def draw(current=None, path=None):
        ax.clear()
        goal = name_to_code[ev.get()]
        hvals = {
            labels[i]: float(distances[i, labels.index(goal)])
            for i in range(len(labels))
        }
        ax.set_xticks([]); ax.set_yticks([])
        colors = []
        for n in G.nodes():
            idx = labels.index(n)
            if path and n in path:
                colors.append("#ff33cc") 
            elif n in visited_nodes:
                colors.append("#ffd54f")
            elif idx < 13:
                colors.append("#a8d5a2")
            elif idx < 33:
                colors.append("#9cc9e5")
            else:
                colors.append("#ffffff")
                
        goal_code = name_to_code[ev.get()]
        hvals = {
            labels[i]: float(distances[i, labels.index(goal_code)])
            for i in range(len(labels))
        }

        nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=2000, node_shape="s", linewidths=1.2, edgecolors="#666666", ax=ax)
        nx.draw_networkx_edges(G, pos, edge_color="#bbbbbb", width=2, arrows=False, ax=ax)
        nx.draw_networkx_edge_labels(G, pos, edge_labels={(u,v):f"{d['weight']:.1f}" for u,v,d in G.edges(data=True)}, font_size=6, bbox=dict(facecolor="#f2f2f2", edgecolor="none", pad=0.2), ax=ax)
        wrapped = {n: "\n".join(textwrap.wrap(letter_names[n], 15)) for n in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels=wrapped, font_size=7, ax=ax)
        
        # overlay straight-line heuristic h(n) → current goal
        goal_code = name_to_code[ev.get()]
        hvals = {
            labels[i]: float(distances[i, labels.index(goal_code)])
            for i in range(len(labels))
        }
        for node, (x, y) in pos.items():
            ax.text(
                x - 0.5, y + 0.6,
                f"h={hvals[node]:.1f}",
                fontsize=6, fontweight="bold",
                color="#333333", zorder=10
            )

        
        for n, (x,y) in pos.items():
            ax.text(
                x-0.5, y+0.6,
                f"h={hvals[n]:.1f}",
                fontsize=6, fontweight="bold",
                color="#333333", zorder=10
            )
        
        for n, (x, y) in pos.items():
            ax.text(
                x - 0.5, y + 0.6,
                f"h={hvals[n]:.1f}",
                fontsize=6, fontweight="bold",
                color="#333333", zorder=10
            )

        if path:
            for u,v in zip(path,path[1:]):
                x1,y1 = pos[u]; x2,y2 = pos[v]
                ax.annotate("", xy=(x2,y2), xytext=(x1,y1), arrowprops=dict(arrowstyle="->", color="#ff33cc", lw=3, ls="dashdot", shrinkA=30, shrinkB=30))
        canvas.draw()

    def step_through_astar():
        visited_nodes.clear()
        s = name_to_code[sv.get()]
        e = name_to_code[ev.get()]
        gen = heuristic_search_generator(s, e)
        def step():
            try:
                ev_type, data = next(gen)
                if ev_type == "visit":
                    visited_nodes.add(data)
                    status_var.set(f"A* visiting: {letter_names[data]}")
                    draw()
                    root.after(500, step)
                elif ev_type == "done":
                    # compute total walking distance along the found path
                    total = sum(
                        distances[labels.index(data[i]), labels.index(data[i+1])]
                        for i in range(len(data) - 1)
                    )
                    status_var.set(f"A* search complete.  Total distance: {total:.1f} units")
                    draw(path=data)
            except StopIteration:
                status_var.set("A* search finished.")
        step()

    def step_through_bfs():
        visited_nodes.clear()
        s = name_to_code[sv.get()]
        e = name_to_code[ev.get()]
        gen = blind_search_generator(s, e)
        def step():
            try:
                ev_type, data = next(gen)
                if ev_type == "visit":
                    visited_nodes.add(data)
                    status_var.set(f"BFS visiting: {letter_names[data]}")
                    draw()
                    root.after(500, step)

                elif ev_type == "done":
                    total = sum(
                        distances[labels.index(data[i]), labels.index(data[i+1])]
                        for i in range(len(data) - 1)
                    )
                    status_var.set(f"BFS search complete.  Total distance: {total:.1f} m")
                    draw(path=data)

            except StopIteration:
                status_var.set("BFS search finished.")
        step()

    ttk.Button(frm, text="Run A* Step-by-Step", command=step_through_astar, width=20).grid(row=0, column=4, padx=10)
    ttk.Button(frm, text="Run BFS Step-by-Step", command=step_through_bfs, width=20).grid(row=0, column=5, padx=10)
    draw()
    root.mainloop()

if __name__ == "__main__":
    run_gui()