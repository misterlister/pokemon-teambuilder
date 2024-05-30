CREATE_PLAYER_TABLE = """
    CREATE TABLE IF NOT EXISTS players (
        player_id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT NOT NULL UNIQUE
    )
    """
    
CREATE_POKEMON_TABLE = """
    CREATE TABLE IF NOT EXISTS pokemon (
        pokemon_id INTEGER PRIMARY KEY AUTOINCREMENT,
        pokemon_name TEXT NOT NULL,
        move1 TEXT,
        move2 TEXT,
        move3 TEXT,
        move4 TEXT
    )
    """

CREATE_TEAMS_TABLE = """
    CREATE TABLE IF NOT EXISTS teams (
        team_id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER NOT NULL,
        team_name TEXT NOT NULL,
        version TEXT NOT NULL,
        pokemon1 INTEGER,
        pokemon2 INTEGER,
        pokemon3 INTEGER,
        pokemon4 INTEGER,
        pokemon5 INTEGER,
        pokemon6 INTEGER,
        FOREIGN KEY (player_id) REFERENCES players(id),
        FOREIGN KEY (pokemon1) REFERENCES pokemon(id) ON DELETE SET NULL,
        FOREIGN KEY (pokemon2) REFERENCES pokemon(id) ON DELETE SET NULL,
        FOREIGN KEY (pokemon3) REFERENCES pokemon(id) ON DELETE SET NULL,
        FOREIGN KEY (pokemon4) REFERENCES pokemon(id) ON DELETE SET NULL,
        FOREIGN KEY (pokemon5) REFERENCES pokemon(id) ON DELETE SET NULL,
        FOREIGN KEY (pokemon6) REFERENCES pokemon(id) ON DELETE SET NULL
    )
    """
