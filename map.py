from collections import OrderedDict, deque

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

adjacency_list = [
    #  A    B    C    D    E    F    G    H    I    J    K    L    M    AA   AB   AC   AD   AE   AF   AG   AH   AI   AJ   AK   AL   AM   AN   AO   AP   AQ   AR   AS   AT   BA   BB   BC   BD
    [ 5.0, 4.5, 3.0, 3.0, 3.0, 4.8, 3.0, 5.0, 3.0, 4.0, 3.0, 3.0, 3.0, 4.7, 3.9, 4.0, 4.0, 3.0, 4.0, 5.0, 4.0, 3.0, 4.9, 4.8, 4.2, 4.0, 4.0, 3.0, 4.2, 3.0, 4.0, 3.0, 3.9, 3.0, 3.0, 3.0, 3.0],
    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,  49],
    [   0,   0,   0,   0,   0,   0,  75,   0,  83,   0,   0,  70,   0,   0,   0,   0,   0,   0,   1,   1,   0,   0,   1,   1,   0,   0,   0,    0,   0,   1,   0,   0,   0,   0,   0,   0,   0],
    [   0,   0,   0,   0,   0,   0,   0, 280,   0,   0,   0,   0,  52,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [   0,   0,   0,   0,   0,   0, 140,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,  36,   0,   0,   0,   0],
    [   0,   0,   0,   0,   0,   0, 180, 190,   0,   0,   0, 200, 110,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [   0,  75,   0, 140,   0, 180,   0,   0,  97,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [   0,   0, 280,   0,   0, 190,   0,   0,   0,   0,   0,   0, 400,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0, 110,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [   0,  83,   0,   0,   0,   0,  97,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,  51,   0,   0],
    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   1,   0,   0,   0,   0,   0,  39],
    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0, 140],
    [   0,  70,   0,   0,   0, 200,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,  61,   0,   0],
    [   0,   0,  52,   0,   0, 110,   0, 400,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   1,   1,   0,   0,   0,   1,   1,    0,   0,   0,   0,   1,   0,   0,   1,   0,   0],
    [   0,   0,   0,   0,   1,   0,   0,   0,   1,   0,   0,   1,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   1,   0,   1,   1],
    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   1,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,    1,   0,   0,   0,   0,   1,   0,   1,   0,   0],
    [   1,   0,   0,   0,   0,   0,   0,   0,   0,   1,   1,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   1,   0,   0]
]

def build_graph():
    """
    Build a bidirectional adjacency list (graph) from the adjacency matrix.
    """
    graph = {}
    keys_list = list(letter_names.keys())
    n = len(keys_list)

    for i in range(2, len(adjacency_list)):
        src = keys_list[i - 2]
        graph.setdefault(src, [])
        for j, weight in enumerate(adjacency_list[i][:n]):
            if weight > 0:
                dst = keys_list[j]
                graph.setdefault(dst, [])
                graph[src].append(dst)
                graph[dst].append(src)
    return graph

def blind_search(start, end):
    """
    Perform a simple BFS (blind) search from start to end.
    """
    graph = build_graph()
    visited = set()
    queue = deque([[start]])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == end:
            print("Path:", " → ".join(path))
            print("Steps:", len(path) - 1)
            return

        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                queue.append(path + [neighbor])

    print("No path found.")

def heuristic_search(start, end):
    """
    Placeholder for heuristic search (e.g., A*).
    """
    print("\u001b[35mhello heuristic\u001b[0m")

if __name__ == "__main__":
    dlsu_number = 13  # campus buildings
    food_number = 20  # food stalls
    letters_list = list(letter_names.keys())
    places_list  = list(letter_names.values())

    # Select campus building
    while True:
        print("\u001b[42m\nWhere are you?\u001b[0m\u001b[32m")
        for i in range(dlsu_number):
            print(f"[{i+1}] {places_list[i]}")
        try:
            option = int(input("\n\u001b[0mYour option: "))
        except ValueError:
            print("\u001b[31mInvalid input! Please enter a number.\u001b[0m")
            continue
        if option < 1 or option > dlsu_number:
            print("\u001b[31mInvalid Input!\u001b[0m")
        else:
            start = letters_list[option - 1]
            break

    # Select food stall
    while True:
        print("\u001b[44m\nWhere do you want to eat?\u001b[0m\u001b[34m")
        for i in range(food_number):
            print(f"[{i+1}] {places_list[dlsu_number + i]}")
        try:
            option = int(input("\n\u001b[0mYour option: "))
        except ValueError:
            print("\u001b[31mInvalid input! Please enter a number.\u001b[0m")
            continue
        if option < 1 or option > food_number:
            print("\u001b[31mInvalid Input!\u001b[0m")
        else:
            end = letters_list[dlsu_number + option - 1]
            break

    print("\u001b[43m\nYour shortest route using BLIND search:\u001b[0m")
    blind_search(start, end)

    print("\u001b[45m\nYour shortest route using HEURISTIC search:\u001b[0m")
    heuristic_search(start, end)

    print("\u001b[0m")  # reset colors
