import csv
from connect import get_connection, create_table


def insert_from_csv(filepath: str):
    conn = get_connection()
    if not conn:
        return
    with conn:
        with conn.cursor() as cur:
            with open(filepath, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        cur.execute(
                            "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
                            (row["first_name"].strip(), row["phone"].strip())
                        )
                    except Exception:
                        conn.rollback()
    print("CSV imported.")


def insert_from_console():
    name = input("Name: ").strip()
    phone = input("Phone: ").strip()
    conn = get_connection()
    if not conn:
        return
    with conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
                    (name, phone)
                )
                print("Contact added.")
            except Exception as e:
                print(f"Error: {e}")


def update_contact():
    print("1. Update name\n2. Update phone")
    choice = input("Choice: ").strip()
    if choice == "1":
        phone = input("Phone of contact to update: ").strip()
        new_name = input("New name: ").strip()
        conn = get_connection()
        if not conn:
            return
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE phonebook SET first_name = %s WHERE phone = %s",
                    (new_name, phone)
                )
                print("Updated.")
    elif choice == "2":
        name = input("Name of contact to update: ").strip()
        new_phone = input("New phone: ").strip()
        conn = get_connection()
        if not conn:
            return
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE phonebook SET phone = %s WHERE first_name = %s",
                    (new_phone, name)
                )
                print("Updated.")


def query_contacts():
    print("1. All contacts\n2. Search by name\n3. Search by phone prefix")
    choice = input("Choice: ").strip()
    conn = get_connection()
    if not conn:
        return
    with conn.cursor() as cur:
        if choice == "1":
            cur.execute("SELECT id, first_name, phone FROM phonebook ORDER BY id;")
        elif choice == "2":
            name = input("Name: ").strip()
            cur.execute(
                "SELECT id, first_name, phone FROM phonebook WHERE first_name ILIKE %s;",
                (f"%{name}%",)
            )
        elif choice == "3":
            prefix = input("Phone prefix: ").strip()
            cur.execute(
                "SELECT id, first_name, phone FROM phonebook WHERE phone LIKE %s;",
                (f"{prefix}%",)
            )
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(f"{row[0]}. {row[1]} — {row[2]}")
        else:
            print("No contacts found.")
    conn.close()


def delete_contact():
    print("1. Delete by name\n2. Delete by phone")
    choice = input("Choice: ").strip()
    conn = get_connection()
    if not conn:
        return
    with conn:
        with conn.cursor() as cur:
            if choice == "1":
                name = input("Name: ").strip()
                cur.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
            elif choice == "2":
                phone = input("Phone: ").strip()
                cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
            print("Deleted.")


def main():
    create_table()
    while True:
        print("\n1. Import from CSV")
        print("2. Add contact")
        print("3. Update contact")
        print("4. Search contacts")
        print("5. Delete contact")
        print("0. Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            path = input("CSV filepath: ").strip()
            insert_from_csv(path)
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            query_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            break


if __name__ == "__main__":
    main()