import sqlite3
from utils.globals import datetime, timedelta

class DBManager:
    def __init__(self, db_path="nba_data.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS player_profiles (
                player_id INTEGER PRIMARY KEY,
                full_name TEXT,
                team TEXT,
                position TEXT,
                height REAL,
                weight REAL,
                birthdate TEXT,
                nationality TEXT,
                from_year INTEGER,
                to_year INTEGER,
                status TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS player_season_stats (
                player_id INTEGER,
                season TEXT,
                team TEXT,
                games_played INTEGER,
                points_per_game REAL,
                assists_per_game REAL,
                rebounds_per_game REAL,
                PRIMARY KEY(player_id, season)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS player_game_logs (
            season_id INTEGER,
            player_id INTEGER,
            game_id INTEGER,
            game_date TEXT,
            matchup TEXT,
            wl TEXT,
            min REAL,
            fgm INTEGER,
            fga INTEGER,
            fg_pct REAL,
            fg3m INTEGER,
            fg3a INTEGER,
            fg3_pct REAL,
            ftm INTEGER,
            fta INTEGER,
            ft_pct REAL,
            oreb INTEGER,
            dreb INTEGER,
            reb INTEGER,
            ast INTEGER,
            stl INTEGER,
            blk INTEGER,
            tov INTEGER,
            pf INTEGER,
            pts INTEGER,
            plus_minus REAL,
            video_available TEXT,
            PRIMARY KEY (player_id, game_id)
            )
        """)
        self.conn.commit()

    def save_player_profile(self, rows, headers):
        headers = [header.lower() for header in headers]
        print(f"[DEBUG] Headers: {headers}")

        for row in rows:
            player_id = row.get("PLAYER_ID")
            full_name = row.get("DISPLAY_FIRST_LAST")
            team = row.get("TEAM_NAME")
            position = row.get("POSITION")
            height = row.get("HEIGHT")
            weight = row.get("WEIGHT")
            birthdate = row.get("BIRTHDATE")
            nationality = row.get("COUNTRY")
            from_year = row.get("FROM_YEAR")
            to_year = row.get("TO_YEAR")
            status = row.get("ROSTERSTATUS")

            self.cursor.execute("SELECT COUNT(*) FROM player_profiles WHERE PLAYER_ID = ?", (player_id,))
            if self.cursor.fetchone()[0] > 0:
                self.cursor.execute("""
                    UPDATE player_profiles
                    SET
                        full_name   = ?,
                        team        = ?,
                        position    = ?,
                        height      = ?,
                        weight      = ?,
                        birthdate   = ?,
                        nationality = ?,
                        from_year   = ?,
                        to_year     = ?,
                        status      = ?
                    WHERE player_id = ?
                """, (
                    full_name,
                    team,
                    position,
                    height,
                    weight,
                    birthdate,
                    nationality,
                    from_year,
                    to_year,
                    status,
                    player_id
                ))

            else:
                self.cursor.execute("""
                    INSERT INTO player_profiles (
                        player_id,
                        full_name,
                        team,
                        position,
                        height,
                        weight,
                        birthdate,
                        nationality,
                        from_year,
                        to_year,
                        status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    player_id,
                    full_name,
                    team,
                    position,
                    height,
                    weight,
                    birthdate,
                    nationality,
                    from_year,
                    to_year,
                    status
                    ))

        self.conn.commit()

    def save_season_stats(self, stats_row, headers):
        stats = dict(zip(headers, stats_row))
        self.cursor.execute("""
            INSERT OR REPLACE INTO player_season_stats (
                player_id, season, team, games_played, points_per_game, assists_per_game, rebounds_per_game
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            stats["PLAYER_ID"],
            stats["SEASON_ID"],
            stats["TEAM_ABBREVIATION"],
            stats["GP"],
            stats["PTS"],
            stats["AST"],
            stats["REB"]
        ))
        self.conn.commit()

    def save_game_logs(self, rows, headers):
        headers = [header.lower() for header in headers]

        for row in rows:
            row_dict = {headers[i]: value for i, value in enumerate(row)}

            player_id = row_dict.get("player_id")
            if not player_id:
                print(f"[ERROR] PLAYER_ID não encontrado na linha: {row_dict}")
                continue

            game_id = row_dict.get("game_id")

            if self.game_log_exists(player_id, game_id):
                print(f"[INFO] Registro já existe para player_id={player_id} e game_id={game_id}, pulando...")
                continue

            stats = {header: row_dict.get(header) for header in headers}

            placeholders = ", ".join(["?"] * len(stats))
            columns = ", ".join(stats.keys())

            insert_query = f"""
                INSERT OR REPLACE INTO player_game_logs (
                    {columns}
                ) VALUES (
                    {placeholders}
                )
            """

            self.cursor.execute(insert_query, tuple(stats.values()))

        self.conn.commit()

    def update_sync_date(self, player_id, sync_date):
        self.cursor.execute("""
            INSERT INTO sync_metadata (player_id, last_synced)
            VALUES (?, ?)
            ON CONFLICT(player_id) DO UPDATE SET last_synced=excluded.last_synced
        """, (player_id, sync_date))

    def game_log_exists(self, player_id, game_id):
        self.cursor.execute("""
            SELECT 1 FROM player_game_logs
            WHERE player_id = ? AND game_id = ?
            LIMIT 1
        """, (player_id, game_id))

        return self.cursor.fetchone() is not None
