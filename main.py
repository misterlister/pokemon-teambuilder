from menus import main_menu
from dbInteraction import init_database
from printouts import print_title
from constants import GREETING, GOODBYE
from textManip import press_enter, clear

if __name__ == "__main__":
    connection = init_database()
    clear()
    print_title(GREETING)
    press_enter()
    main_menu(connection)
    clear()
    print_title(GOODBYE)
    connection.close()
