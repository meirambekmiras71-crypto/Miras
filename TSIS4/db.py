import psycopg2
from config import DB_CONFIG


def get_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.OperationalError as e:
        print(f"Connection error: {e}")
        return None


def init_db():
    conn = get_connection()
    if not conn:
        return
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id       SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id            SERIAL PRIMARY KEY,
                    player_id     INTEGER REFERENCES players(id),
                    score         INTEGER   NOT NULL,
                    level_reached INTEGER   NOT NULL,
                    played_at     TIMESTAMP DEFAULT NOW()
                );
            """)
    conn.close()


def get_or_create_player(username):
    conn = get_connection()
    if not conn:
        return None
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM players WHERE username = %s", (username,))
            row = cur.fetchone()
            if row:
                return row[0]
            cur.execute(
                "INSERT INTO players (username) VALUES (%s) RETURNING id",
                (username,)
            )
            return cur.fetchone()[0]
    conn.close()


def save_session(player_id, score, level_reached):
    conn = get_connection()
    if not conn:
        return
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
                (player_id, score, level_reached)
            )
    conn.close()


def get_top10():
    conn = get_connection()
    if not conn:
        return []
    with conn.cursor() as cur:
        cur.execute("""
            SELECT p.username, gs.score, gs.level_reached, gs.played_at
            FROM game_sessions gs
            JOIN players p ON p.id = gs.player_id
            ORDER BY gs.score DESC
            LIMIT 10
        """)
        rows = cur.fetchall()
    conn.close()
    return rows


def get_personal_best(player_id):
    conn = get_connection()
    if not conn:
        return 0
    with conn.cursor() as cur:
        cur.execute(
            "SELECT MAX(score) FROM game_sessions WHERE player_id = %s",
            (player_id,)
        )
        row = cur.fetchone()
    conn.close()
    return row[0] if row and row[0] else 0