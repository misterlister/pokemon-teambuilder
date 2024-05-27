from constants import (
    LGBORDER,
    MDBORDER,
    SMBORDER
)

def greeting() -> None:
    print(LGBORDER*2)
    print("Welcome to the Pokemon Teambuilder!")
    print(LGBORDER*2)
    
def goodbye() -> None:
    print(LGBORDER*3)
    print("Thanks for using the Pokemon Teambuilder! See you later!")
    print(LGBORDER*3)
    
def print_list(list: list, heading:str = None) -> None:
    if heading:
        if len(heading) < 20:
            border = LGBORDER
        elif len(heading) < 40:
            border = MDBORDER
        else:
            border = SMBORDER
        print("\n", border, heading, border)
    max_size = 1
    if len(list) == 0:
        print("No data exists\n")
        return
    for item in list:
        if item == None:
            if 4 > max_size: max_size = 5
        elif len(item) > max_size:
            max_size = len(item) + 1
    items_per_line = int(90 / max_size)
    for i in range(len(list)):
        if i % items_per_line == 0 and i > 0:
            print("")
        if list[i] == None:
            value = "None"
        else:
            value = list[i]
        print(f"{value.ljust(max_size, " ")} ", end="")
    print("")
    
    