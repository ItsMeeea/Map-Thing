dlsu_list = """\u001b[32m
[1]  Andrew - Br. Andrew Gonzales Hall
[2]  Bloemen - Br. Alphonsus Bloemen Hall
[3]  Connon - Br. Gabriel Connon Hall
[4]  Faculty Center
[5]  Gokongwei - John Gokongwei Sr. Hall
[6]  Henry Sy Sr. Hall
[7]  St. Joseph Hall
[8]  St. La Salle Hall
[9]  St. Miguel Febres Cordero Hall
[10] Razon - Enrique M. Razon Sports Center
[11] Science & Technology Research Center
[12] Velasco - Urbano J. Velasco Hall
[13] Yuchengco - Don Enrique T. Yuchengco Hall
"""

food_list = """\u001b[34m
[1]  24 Chicken
[2]  Ate Rica's Bacsilog
[3]  Bab
[4]  The Barn
[5]  BBQ Nation
[6]  Chef Bab's House of Sisig
[7]  Colonel's Curry
[8]  Good Munch
[9]  Gyuniku
[10] Happy N' Healthy (Bloemen)
[11] The Hungry Pita
[12] Kitchen City
[13] Kuya Mel Kitchen
[14] Lumpia.natics
[15] Master Chop
[16] McDonald's
[17] Mongolian Master
[18] Perico's
[19] Tapa Loca
[20] Tori Box
"""

# map / graph thing is in google docs also the table is in the docs

# first row is the A* score of each col (used for A* search)
# ex: B has A* score of 4.5

# for the rest, rows are the start, cols are the goals
# ex: look at line 57 if starting at point A, line 63 if point G, line 69 if point M
# ex: from point G to point B, it's 75 meters away

# A-M represent dlsu_list above in order
# AA-AT represent food_list above in order
# N, O, P, Q arent on campus (e.g. Agno Street); they're just used in the algo

# grabe ang tagal ko rito

adjacency_list = [
    #  A    B    C    D    E    F    G    H    I    J    K    L    M    N    O    P    Q    AA   AB   AC   AD   AE   AF   AG   AH   AI   AJ   AK   AL   AM   AN   AO   AP   AQ   AR   AS   AT
    [ 5.0, 4.5, 3.0, 3.0, 3.0, 4.8, 3.0, 5.0, 3.0, 4.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 4.7, 3.9, 4.0, 4.0, 3.0, 4.0, 5.0, 4.0, 3.0, 4.9, 4.8, 4.2, 4.0, 4.0, 3.0, 4.2, 3.0, 4.0, 3.0, 3.9],
    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  49,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,    0,   0,   0,   0,   0,   0],
    [   0,   0,   0,   0,   0,   0,  75,   0,  83,   0,   0,  70,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   1,   1,   0,   0,   1,   1,   0,   0,   0,    0,   0,   1,   0,   0,   0],
    [   0,   0,   0,   0,   0,   0,   0, 280,   0,   0,   0,   0,  52,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0],
    [   0,   0,   0,   0,   0,   0, 140,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0],
    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  36,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0],
    [   0,   0,   0,   0,   0,   0, 180, 190,   0,   0,   0, 200, 110,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0],
    [   0,  75,   0, 140,   0, 180,   0,   0,  97,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0],
    [   0,   0, 280,   0,   0, 190,   0,   0,   0,   0,   0,   0, 400,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0, 110,   0,   0,   0,   0],
    [   0,  83,   0,   0,   0,   0,  97,   0,   0,   0,   0,   0,   0,   0,  51,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0],
    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  39,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   1,   0,   0],
    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 140,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0],
    [   0,  70,   0,   0,   0, 200,   0,   0,   0,   0,   0,   0,   0,   0,  61,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0],
    [   0,   0,  52,   0,   0, 110,   0, 400,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0],
    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  45,   0,   0,   0,   1,  0,   0,   0,   0,   0,   1,   1,   0,   0,   0,   1,   1,    0,   0,   0,   0,   1,   0],
    [   0,   0,   0,   0,  36,   0,   0,   0,  51,   0,   0,  61,   0,  45,   0, 160, 190,   0,   0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0],
    [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 160,   0,   0,   1,   0,  1,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,    1,   0,   0,   0,   0,   1],
    [  49,   0,   0,   0,   0,   0,   0,   0,   0,  39, 140,   0,   0,   0, 190,   0,   0,   0,   0,  0,  19,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,    0,   0,   0,   0,   0,   0]
]

def convert_dlsu(option):
    """
    Converts user's chosen DLSU location into its corresponding point letter

    Args:
        option (int): user's option

    Returns:
        str: converted point letter
    """
    match option:
        case 1: converted = "A"
        case 2: converted = "B"
        case 3: converted = "C"
        case 4: converted = "D"
        case 5: converted = "E"
        case 6: converted = "F"
        case 7: converted = "G"
        case 8: converted = "H"
        case 9: converted = "I"
        case 10: converted = "J"
        case 11: converted = "K"
        case 12: converted = "L"
        case 13: converted = "M"
    return converted

def convert_food(option):
    """
    Converts user's chosen food location into its corresponding point letter

    Args:
        option (int): user's option

    Returns:
        str: converted point letter
    """
    match option:
        case 1: converted = "AA"
        case 2: converted = "AB"
        case 3: converted = "AC"
        case 4: converted = "AD"
        case 5: converted = "AE"
        case 6: converted = "AF"
        case 7: converted = "AG"
        case 8: converted = "AH"
        case 9: converted = "AI"
        case 10: converted = "AJ"
        case 11: converted = "AK"
        case 12: converted = "AL"
        case 13: converted = "AM"
        case 14: converted = "AN"
        case 15: converted = "AO"
        case 16: converted = "AP"
        case 17: converted = "AQ"
        case 18: converted = "AR"
        case 19: converted = "AS"
        case 20: converted = "AT"
    return converted

def blind_search(start, end):
    """
    Performs a blind search to find the best path between the start and end points
    Prints total distance, total cost, time it took to calculate

    Args:
        start (str): start point
        end (str): end point
    """
    print("\u001b[33mhello blind")

def heuristic_search(start, end):
    """
    Performs a heuristic search to find the best path between the start and end points
    Prints total distance, total cost, time it took to calculate

    Args:
        start (str): start point
        end (str): end point
    """
    print("\u001b[35mhello heuristic")

if __name__ == "__main__":
    while True:
        print("\u001b[42m\nWhere are you?\u001b[0m", end='')
        print(dlsu_list)
        option = int(input("\u001b[37mYour option: "))
        if(option < 1  or option > 14):
            print("\u001b[31mInvalid Input!")
        else:
            start = convert_dlsu(option)
            break

    while True:
        print("\u001b[44m\nWhere do you want to eat?\u001b[0m", end='')
        print(food_list)
        option = int(input("\u001b[37mYour option: "))
        if(option < 1  or option > 20):
            print("\u001b[31mInvalid Input!")
        else:
            end = convert_food(option)
            break

    print("\u001b[43m\nYour shortest route using BLIND search:\u001b[0m")
    blind_search(start, end)

    print("\u001b[45m\nYour shortest route using HEURISTIC search:\u001b[0m")
    heuristic_search(start, end)

    print("\u001b[0m") # reset colors