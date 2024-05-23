CREATE_TEAMS_TABLE = """
    CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            team_name TEXT NOT NULL,
            version TEXT NULL,
            pokemon1 TEXT,
            pokemon2 TEXT,
            pokemon3 TEXT,
            pokemon4 TEXT,
            pokemon5 TEXT,
            pokemon6 TEXT
        )
    """