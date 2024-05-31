"""
Contains functions dealing with printing out formatted information.
"""

from constants import BORDER, WIDTH, INNER_WIDTH

def print_title(title: str) -> None:
    print(BORDER * WIDTH)
    print(title.center(WIDTH))
    print(BORDER * WIDTH)

def printout_list(printlist: list, heading: str = None, border: bool = False) -> None:
    if heading:
        print_heading(heading)

    max_size = 1
    buffer = "  "
    if len(printlist) == 0:
        print("No data exists\n")
        return
    for item in printlist:
        if item is None:
            if 4 > max_size:
                max_size = 5
        elif len(item) > max_size:
            max_size = len(item)
    max_size += len(buffer)
    items_per_line = int(INNER_WIDTH / max_size)
    if border:
        list_border = ((max_size+1) * min(items_per_line, len(printlist))) * BORDER
        print("\t" + list_border)
    print("\t", end="")
    for i in range(len(printlist)):
        if i % items_per_line == 0 and i != 0:
            print("\n\t", end="")
        if printlist[i] is None:
            value = "None"
        else:
            value = printlist[i]
        print(f"{value.ljust(max_size)}{buffer}", end="")
    if border:
        print("\n\t" + list_border)
        return
    print("")

def print_heading(heading: str) -> None:
    print("\n" + heading.center(WIDTH, BORDER))
