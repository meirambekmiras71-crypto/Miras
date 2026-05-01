import psycopg2
from config import DB_CONFIG


def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.OperationalError as e:
        print(f"Connection error: {e}")
        return None


def create_table():
    conn = get_connection()
    if not conn:
        return
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS groups (
                    id   SERIAL PRIMARY KEY,
                    name VARCHAR(50) UNIQUE NOT NULL
                );
            """)
            cur.execute("""
                INSERT INTO groups (name) VALUES
                    ('Family'), ('Work'), ('Friend'), ('Other')
                ON CONFLICT (name) DO NOTHING;
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phonebook (
                    id         SERIAL PRIMARY KEY,
                    first_name VARCHAR(50)  NOT NULL,
                    email      VARCHAR(100),
                    birthday   DATE,
                    group_id   INTEGER REFERENCES groups(id) ON DELETE SET NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phones (
                    id         SERIAL PRIMARY KEY,
                    contact_id INTEGER     NOT NULL REFERENCES phonebook(id) ON DELETE CASCADE,
                    phone      VARCHAR(20) NOT NULL,
                    type       VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
                );
            """)
    print("Tables are ready.")
    conn.close()