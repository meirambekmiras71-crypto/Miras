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
                CREATE TABLE IF NOT EXISTS phonebook (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    phone VARCHAR(20) UNIQUE NOT NULL
                );
            """)
    print("Table 'phonebook' is ready.")
    conn.close()