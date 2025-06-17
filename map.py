from collections import OrderedDict

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

# regarding the adjacency list below:

# map / graph thing and also the table below is in the google docs

# first row is the A* score of each col (used for A* search)
# ex: B has A* score of 4.5

# for the rest, rows (A-M, BA-BD) are the start, cols (A-M, AA-AT, BA-BD) are the goals
# ex: look at line 63 if you wanna start at point A, line 69 if point G, line 75 if point M
# ex: from point G to point B, it's 75 meters away

# A-M represent dlsu bldgs above in order
# AA-AT represent food list above in order
# BA, BB, BC, BD arent on campus (e.g. Agno Street); they're just used in the algo

adjacency_list = [
    #  A    B    C    D    E    F    G    H    I    J    K    L    M    AA   AB   AC   AD   AE   AF   AG   AH   AI   AJ   AK   AL   AM   AN   AO   AP   AQ   AR   AS   AT   BA   BB   BC   BD
    [ 5.0, 4.5, 3.0, 3.0, 3.0, 4.8, 3.0, 5.0, 3.0, 4.0, 3.0, 3.0, 3.0, 4.7, 3.9, 4.0, 4.0, 3.0, 4.0, 5.0, 4.0, 3.0, 4.9, 4.8, 4.2, 4.0, 4.0, 3.0, 4.2, 3.0, 4.0, 3.0, 3.9, 3.0, 3.0, 3.0, 3.0],
    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,  49],
    [   0,   0,   0,   0,   0,   0,  75,   0,  83,   0,   0,  70,   0,   0,   0,  0,   0,   0,   1,   1,   0,   0,   1,   1,   0,   0,   0,    0,   0,   1,   0,   0,   0,   0,   0,   0,   0],
    [   0,   0,   0,   0,   0,   0,   0, 280,   0,   0,   0,   0,  52,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [   0,   0,   0,   0,   0,   0, 140,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,  36,   0,   0],
    [   0,   0,   0,   0,   0,   0, 180, 190,   0,   0,   0, 200, 110,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [   0,  75,   0, 140,   0, 180,   0,   0,  97,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [   0,   0, 280,   0,   0, 190,   0,   0,   0,   0,   0,   0, 400,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0, 110,   0,   0,   0,   0,   0,   0,   0,   0],
    [   0,  83,   0,   0,   0,   0,  97,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,  51,   0,   0],
    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   1,   0,   0,   0,   0,   0,  39],
    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0, 140],
    [   0,  70,   0,   0,   0, 200,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,  61,   0,   0],
    [   0,   0,  52,   0,   0, 110,   0, 400,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,  0,   0,   0,   0,   0,   1,   1,   0,   0,   0,   1,   1,    0,   0,   0,   0,   1,   0,   0,   1,   0,   0],
    [   0,   0,   0,   0,   1,   0,   0,   0,   1,   0,   0,   1,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   1,   0,   1,   1],
    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,  1,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,    1,   0,   0,   0,   0,   1,   0,   1,   0,   0]
    [   1,   0,   0,   0,   0,   0,   0,   0,   0,   1,   1,   0,   0,   0,   0,  0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0,   0,   1,   0,   0]
]

def blind_search(start, end):
    """
    Performs a blind search to find the best path between the start and end points
    Prints the list of places to pass through
    Also the total distance, total cost, time it took to calculate, other stats

    Args:
        start (str): start point letter
        end (str): end point letter
    """
    print("\u001b[33mhello blind")

def heuristic_search(start, end):
    """
    Performs a heuristic search to find the best path between the start and end points
    Prints the list of places to pass through
    Also the total distance, total cost, time it took to calculate, other stats

    Args:
        start (str): start point letter
        end (str): end point letter
    """
    print("\u001b[35mhello heuristic")

if __name__ == "__main__":
    dlsu_number = 13 # no of bldgs
    food_number = 20 # no of foods
    letters_list = list(letter_names.keys())
    places_list = list(letter_names.values())

    while True:
        print("\u001b[42m\nWhere are you?\u001b[0m\u001b[32m")
        for i in range(dlsu_number):
            print("[" + str(i+1) + "] " + places_list[i], sep="")
        option = int(input("\n\u001b[0mYour option: "))
        if(option < 1  or option > 14):
            print("\u001b[31mInvalid Input!")
        else:
            start = letters_list[option - 1]
            break

    while True:
        print("\u001b[44m\nWhere do you want to eat?\u001b[0m\u001b[34m")
        for i in range(food_number):
            print("[" + str(i+1) + "] " + places_list[dlsu_number + i], sep="")
        option = int(input("\n\u001b[0mYour option: "))
        if(option < 1  or option > 20):
            print("\u001b[31mInvalid Input!")
        else:
            end = letters_list[option - 1 + dlsu_number]
            break

    print("\u001b[43m\nYour shortest route using BLIND search:\u001b[0m")
    blind_search(start, end)

    print("\u001b[45m\nYour shortest route using HEURISTIC search:\u001b[0m")
    heuristic_search(start, end)

    print("\u001b[0m") # reset colors