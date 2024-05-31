# Pokemon Teambuilder

![Pylint](https://github.com/misterlister/pokemon-teambuilder/actions/workflows/pylint.yml/badge.svg)

## What is it?

Pokemon Teambuilder is a command-line application which allows a user to store a database of pokemon teams from different versions.

Users can store information about:

- The player who uses the team
- The game version the team is from
- The species name of up to 6 pokemon on the main team
- The movesets of each pokemon on the team

The user can then access this information from the database, or update it if necessary.

## How do you use it?

Users enter commands by typing one of the listed options on a given menu.

The first letter of any given command may be used as a shortcut instead of entering the full word.

## How does it work?

This application accesses the pokeapi API in order to get up-to-date information about all pokemon, game versions, and movesets.

The information entered is stored locally in a database using sqlite3.


