from constants import BORDER, WIDTH, INNER_WIDTH

def print_title(title: str) -> None:
    print(BORDER * WIDTH)
    print(title.center(WIDTH))
    print(BORDER * WIDTH)
    
def print_list(list: list, heading: str = None, border: bool = False) -> None:
    if heading:
        print_heading(heading)
    
    max_size = 1
    if len(list) == 0:
        print("No data exists\n")
        return
    for item in list:
        if item == None:
            if 4 > max_size: max_size = 5
        elif len(item) > max_size:
            max_size = len(item) + 1
    items_per_line = int(INNER_WIDTH / max_size)
    if border:
        list_border = (max_size * min(items_per_line, len(list))) * BORDER
        print("\t" + list_border)
    print("\t", end="")
    for i in range(len(list)):
        if i % items_per_line == 0 and i != 0:
            print("\n\t", end="")
        if list[i] == None:
            value = "None"
        else:
            value = list[i]
        print(f"{value.ljust(max_size, " ") }", end="")
    if border:
        print("\n\t" + list_border)
    else:
        print("")
    
def print_heading(heading: str) -> None:
    print("\n" + heading.center(WIDTH, BORDER))