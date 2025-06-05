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
[1] 24 Chicken
[2] Ate Rica's Bacsilog
[3] Bab
[4] The Barn
[5] BBQ Nation
[6] Chef Bab's House of Sisig
[7] Colonel's Curry
[8] Good Munch
[9] Gyuniku
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

def blind_search():
    print("\u001b[33mhello blind")

def heuristic_search():
    print("\u001b[35mhello heuristic")

if __name__ == "__main__":
    start = 0
    end = 0

    while(start < 1  or start > 13):
        print("\u001b[42m\nWhere are you?\u001b[0m", end='')
        print(dlsu_list)
        start = int(input("\u001b[37mYour option: "))
        if(start < 1  or start > 14):
            print("\u001b[31mInvalid Input!")

    while(end < 1 or end > 20):
        print("\u001b[44m\nWhere do you want to eat?\u001b[0m", end='')
        print(food_list)
        end = int(input("\u001b[37mYour option: "))
        if(end < 1  or end > 20):
            print("\u001b[31mInvalid Input!")

    print("\u001b[43m\nYour shortest route using BLIND search:\u001b[0m")
    blind_search()

    print("\u001b[45m\nYour shortest route using HEURISTIC search:\u001b[0m")
    heuristic_search()

    print("\u001b[0m") # reset colors