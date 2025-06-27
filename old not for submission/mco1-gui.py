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
    "AI": "Gyuniku",           "AJ": "Happy N’ Healthy (Bloemen)",
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

# === 4. BFS (blind) ===
def blind_search(start, end):
    graph, visited, queue = build_graph_unweighted(), set(), deque([[start]])
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

# === 5. A* (heuristic) ===
def heuristic_search(start, goal):
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
        if current==goal:
            path=[]
            while current:
                path.insert(0,current)
                current=parent[current]
            return path
        for neigh,c in graph[current]:
            tg = g_score[current]+c
            if neigh not in g_score or tg<g_score[neigh]:
                parent[neigh]=current
                g_score[neigh]=tg
                f_score[neigh]=tg+hvals[neigh]
                heapq.heappush(open_set,(f_score[neigh],neigh))
    return None

# === 6. GUI & drawing ===
def run_gui():
    # build directed graph
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
    root.title("Path Finder: BFS vs A*")
    root.geometry("1400x900")
    root.configure(bg="#f2f2f2")

    frm = tk.Frame(root,bg="#f2f2f2"); frm.pack(pady=10)
    ttk.Label(frm,text="Start:",background="#f2f2f2").grid(row=0,column=0)
    sv = tk.StringVar(value=full_names[0])
    ttk.Combobox(frm, textvariable=sv, values=full_names, width=30).grid(row=0, column=1, padx=5)
    ttk.Label(frm,text="End:",background="#f2f2f2").grid(row=0,column=2)
    ev = tk.StringVar(value=full_names[-1])
    ttk.Combobox(frm, textvariable=ev, values=full_names, width=30).grid(row=0, column=3, padx=5)

    result_lbl = tk.Label(
        frm,text="",justify="left",
        font=("Segoe UI",10),bg="#f2f2f2"
    )
    result_lbl.grid(row=1,column=0,columnspan=5,sticky="w",pady=5)

    fig,ax = plt.subplots(figsize=(20,10))
    fig.patch.set_facecolor("#f2f2f2")
    ax.set_facecolor("#e8e8e8")
    fig.subplots_adjust(.02,.02,.98,.98)

    canvas = FigureCanvasTkAgg(fig,master=root)
    canvas.get_tk_widget().pack(fill="both",expand=True)

    def draw(bfs_path=None,astar_path=None,goal=None):
        ax.clear()
        ax.set_xticks([]); ax.set_yticks([])

        # compute heuristics to this goal
        hvals = {labels[i]: float(distances[i,labels.index(goal)])
                 for i in range(len(labels))}

        # node colors
        cols=[]
        for n in G.nodes():
            idx=labels.index(n)
            if idx<13:    cols.append("#a8d5a2")
            elif idx<33:  cols.append("#9cc9e5")
            else:         cols.append("#ffffff")

        nx.draw_networkx_nodes(
            G,pos,node_color=cols,node_size=2000,
            node_shape="s",linewidths=1.2,edgecolors="#666666",ax=ax
        )

        # wrap labels
        wrapped = {
            n:"\n".join(textwrap.wrap(letter_names[n],15))
            for n in G.nodes()
        }
        nx.draw_networkx_labels(G,pos,labels=wrapped,font_size=7,ax=ax)

        # draw heuristic next to each node
        for n,(x,y) in pos.items():
            ax.text(
                x-0.5, y+0.6,
                f"h={hvals[n]:.1f}",
                fontsize=6, fontweight="bold",
                color="#333333", zorder=10
            )

        # base edges
        nx.draw_networkx_edges(
            G,pos,edge_color="#bbbbbb",width=2,arrows=False,ax=ax
        )
        nx.draw_networkx_edge_labels(
            G,pos,
            edge_labels={(u,v):f"{d['weight']:.1f}" for u,v,d in G.edges(data=True)},
            font_size=6,bbox=dict(facecolor="#f2f2f2",edgecolor="none",pad=0.2),
            ax=ax
        )

        # BFS highlight
        if bfs_path:
            for u,v in zip(bfs_path,bfs_path[1:]):
                x1,y1 = pos[u]; x2,y2 = pos[v]
                ax.annotate(
                    "",
                    xy=(x2,y2), xytext=(x1,y1),
                    arrowprops=dict(
                        arrowstyle="->",
                        color="#e57373",
                        lw=3,
                        ls="dashed",
                        shrinkA=30,
                        shrinkB=30
                    )
                )

        # A* highlight
        if astar_path:
            for u,v in zip(astar_path,astar_path[1:]):
                x1,y1 = pos[u]; x2,y2 = pos[v]
                ax.annotate(
                    "",
                    xy=(x2,y2), xytext=(x1,y1),
                    arrowprops=dict(
                        arrowstyle="->",
                        color="#ffd54f",
                        lw=3,
                        ls="dashdot",
                        shrinkA=30,
                        shrinkB=30
                    )
                )

        canvas.draw()

    def on_find():
        # map the chosen full names back to letter-codes
        s_full = sv.get()
        e_full = ev.get()
        s = name_to_code[s_full]
        e = name_to_code[e_full]

        bfs_p = blind_search(s, e)
        ast_p = heuristic_search(s, e)

        # BFS result
        if bfs_p:
            cost = sum(
                distances[labels.index(bfs_p[i]), labels.index(bfs_p[i+1])]
                for i in range(len(bfs_p)-1)
            )
            bfs_names = [letter_names[n] for n in bfs_p]
            txt1 = f"BFS → {' → '.join(bfs_names)}   steps:{len(bfs_p)-1}, cost:{cost:.1f}"
        else:
            txt1 = "BFS → no path"

        # A* result
        if ast_p:
            cost = sum(
                distances[labels.index(ast_p[i]), labels.index(ast_p[i+1])]
                for i in range(len(ast_p)-1)
            )
            ast_names = [letter_names[n] for n in ast_p]
            txt2 = f"A*  → {' → '.join(ast_names)}   steps:{len(ast_p)-1}, cost:{cost:.1f}"
        else:
            txt2 = "A* → no path"

        result_lbl.config(text=f"{txt1}\n{txt2}")
        draw(bfs_path=bfs_p, astar_path=ast_p, goal=e)


    ttk.Button(frm,text="Find Path",command=on_find,width=14)\
       .grid(row=0,column=4,padx=10)

    # initial draw (default end)
    draw(goal=labels[-1])
    root.mainloop()

if __name__=="__main__":
    run_gui()
