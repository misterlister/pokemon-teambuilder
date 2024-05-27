from menus import main_menu
from dbInteraction import init_database
from printouts import (
    greeting,
    goodbye
)


if __name__ == "__main__":
    connection = init_database()
    greeting()
    main_menu(connection)
    goodbye()
    connection.close()