from collections import OrderedDict, deque
import heapq
import pandas as pd
df = pd.read_excel("adjacency.xlsx", header=None)
adjacency_list = df.values.tolist()
letter_names = OrderedDict([
    ("A", "Andrew - Br. Andrew Gonzales Hall"),
    ("B", "Bloemen - Br. Alphonsus Bloemen Hall"),
    ("C", "Connon - Br. Gabriel Connon Hall"),
    ("D", "Faculty Center"),
    ("E", "Gokongwei - John Gokongwei Sr. Hall"),
    ("F", "Henry Sy Sr. Hall"),
    ("G", "St. Joseph Hall"),
    ("H", "St. La Salle Hall"),
    ("I", "St. Miguel Febres Cordero Hall"),
    ("J", "Razon - Enrique M. Razon Sports Center"),
    ("K", "Science & Technology Research Center"),
    ("L", "Velasco - Urbano J. Velasco Hall"),
    ("M", "Yuchengco - Don Enrique T. Yuchengco Hall"),
    ("AA", "24 Chicken"),
    ("AB", "Ate Rica's Bacsilog"),
    ("AC", "Bab"),
    ("AD", "The Barn"),
    ("AE", "BBQ Nation"),
    ("AF", "Chef Bab's House of Sisig"),
    ("AG", "Colonel's Curry"),
    ("AH", "Good Munch"),
    ("AI", "Gyuniku"),
    ("AJ", "Happy N' Healthy (Bloemen)"),
    ("AK", "The Hungry Pita"),
    ("AL", "Kitchen City"),
    ("AM", "Kuya Mel Kitchen"),
    ("AN", "Lumpia.natics"),
    ("AO", "Master Chop"),
    ("AP", "McDonald's"),
    ("AQ", "Mongolian Master"),
    ("AR", "Perico's Grill"),
    ("AS", "Tapa Loca"),
    ("AT", "Tori Box"),
    ("BA", "Agno Food Court"),
    ("BB", "Agno St."),
    ("BC", "EGI Taft Tower"),
    ("BD", "Fidel A. Reyes St.")
])

# === BFS with Distance Tracking ===
def blind_search(start, end):
    keys = list(letter_names.keys())
    index_map = {k: i for i, k in enumerate(keys)}
    visited = set()
    queue = deque([([start], 0)])  # (path, total_distance)

    while queue:
        path, total_dist = queue.popleft()
        current = path[-1]

        if current == end:
            print("Path:", " → ".join(path))
            print("Total Distance:", total_dist, "meters")
            print("Steps:", len(path) - 1)
            return

        if current not in visited:
            visited.add(current)
            cur_idx = index_map[current]

            for next_idx, weight in enumerate(adjacency_list[cur_idx]):
                if weight > 0:
                    neighbor = keys[next_idx]
                    if neighbor not in visited:
                        queue.append((path + [neighbor], total_dist + weight))

    print("No path found.")

# --------------- HEURISTIC SEARCH ---------------------
def build_weighted_graph():
    """
    Build a weighted adjacency list graph from the adjacency matrix.
    """
    graph = {}
    keys = list(letter_names.keys())
    n = len(keys)

    for i in range(n):
        src = keys[i]
        graph[src] = []
        for j in range(n):
            weight = adjacency_list[i][j]
            if weight > 0:
                dst = keys[j]
                graph[src].append((dst, weight))
    return graph

def get_heuristic(goal):
    heuristic_values = [
        5.0, 4.5, 3.0, 3.0, 3.0, 4.8, 3.0, 5.0, 3.0, 4.0, 3.0, 3.0, 3.0,
        4.7, 3.9, 4.0, 4.0, 3.0, 4.0, 5.0, 4.0, 3.0, 4.9, 4.8, 4.2, 4.0,
        4.0, 3.0, 4.2, 3.0, 4.0, 3.0, 3.9, 3.0, 3.0, 3.0, 3.0
    ]
    keys = list(letter_names.keys())
    return {key: heuristic_values[i] for i, key in enumerate(keys)}

def heuristic_search(start, goal):
    graph = build_weighted_graph()
    heuristics = get_heuristic(goal)

    open_set = []
    heapq.heappush(open_set, (heuristics[start], start))  # (f, node)

    g = {start: 0}
    h = {start: heuristics[start]}
    f = {start: g[start] + h[start]}
    parent = {start: None}
    closed_set = set()

    while open_set:
        # Get the node in open_set with lowest f value
        current_f, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruct path from goal to start
            path = []
            while current is not None:
                path.insert(0, current)
                current = parent[current]
            print("Path:", " → ".join(path))
            print("Steps:", len(path) - 1)
            print("Total cost:", g[goal])
            return

        closed_set.add(current)

        for neighbor, cost in graph.get(current, []):
            if neighbor in closed_set:
                continue

            tentative_g = g[current] + cost

            if neighbor not in g or tentative_g < g[neighbor]:
                parent[neighbor] = current
                g[neighbor] = tentative_g
                h[neighbor] = heuristics.get(neighbor, float('inf'))
                f[neighbor] = g[neighbor] + h[neighbor]
                heapq.heappush(open_set, (f[neighbor], neighbor))

    print("No path found.")

if __name__ == "__main__":
    letters_list = list(letter_names.keys())
    places_list  = list(letter_names.values())

    # Select campus building
    while True:
        while True:
            print("\033[42m\nWhere are you?\033[0m\033[32m")
            for i, place in enumerate(places_list):
                print(f"[{i+1}] {place}")
            try:
                option = int(input("\n\033[0mYour option: "))
            except ValueError:
                print("\033[31mInvalid input! Please enter a number.\033[0m")
                continue
            if option < 1 or option > len(places_list):
                print("\033[31mInvalid Input!\033[0m")
            else:
                start = letters_list[option - 1]
                break

        # Select any destination location (from all 38)
        while True:
            print("\033[44m\nWhere do you want to go?\033[0m\033[34m")
            for i, place in enumerate(places_list):
                print(f"[{i+1}] {place}")
            try:
                option = int(input("\n\033[0mYour option: "))
            except ValueError:
                print("\033[31mInvalid input! Please enter a number.\033[0m")
                continue
            if option < 1 or option > len(places_list):
                print("\033[31mInvalid Input!\033[0m")
            else:
                end = letters_list[option - 1]
                break

        print("\033[43m\nYour shortest route using BLIND search:\033[0m")
        blind_search(start, end)

        print("\033[45m\nYour shortest route using HEURISTIC search:\033[0m")
        heuristic_search(start, end)

        print("\033[0m")  # reset colors
    
        again = input("\n\033[33mWould you like to find another path? (y/n): \033[0m").strip().lower()
        if again != 'y':
            print("\033[41mExiting program. Goodbye!\033[0m")
            break
