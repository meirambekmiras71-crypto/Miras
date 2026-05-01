import csv
import json
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
                            "INSERT INTO phonebook (first_name, email, birthday) VALUES (%s, %s, %s) RETURNING id",
                            (
                                row.get("first_name", "").strip(),
                                row.get("email", "").strip() or None,
                                row.get("birthday", "").strip() or None,
                            )
                        )
                        contact_id = cur.fetchone()[0]

                        phone = row.get("phone", "").strip()
                        phone_type = row.get("type", "mobile").strip() or "mobile"
                        if phone:
                            cur.execute(
                                "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                                (contact_id, phone, phone_type)
                            )

                        group = row.get("group", "").strip()
                        if group:
                            cur.execute("CALL move_to_group(%s, %s)", (row["first_name"].strip(), group))

                    except Exception as e:
                        conn.rollback()
                        print(f"Error: {e}")
    print("CSV imported.")


def insert_from_console():
    name = input("Name: ").strip()
    email = input("Email (optional): ").strip() or None
    birthday = input("Birthday (YYYY-MM-DD, optional): ").strip() or None
    phone = input("Phone: ").strip()
    phone_type = input("Phone type (home/work/mobile): ").strip() or "mobile"
    group = input("Group (Family/Work/Friend/Other, optional): ").strip() or None

    conn = get_connection()
    if not conn:
        return
    with conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO phonebook (first_name, email, birthday) VALUES (%s, %s, %s) RETURNING id",
                    (name, email, birthday)
                )
                contact_id = cur.fetchone()[0]
                cur.execute(
                    "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                    (contact_id, phone, phone_type)
                )
                if group:
                    cur.execute("CALL move_to_group(%s, %s)", (name, group))
                print("Contact added.")
            except Exception as e:
                print(f"Error: {e}")


def update_contact():
    print("1. Update name\n2. Update email\n3. Update birthday\n4. Update group")
    choice = input("Choice: ").strip()
    conn = get_connection()
    if not conn:
        return
    with conn:
        with conn.cursor() as cur:
            if choice == "1":
                old_name = input("Current name: ").strip()
                new_name = input("New name: ").strip()
                cur.execute("UPDATE phonebook SET first_name = %s WHERE first_name = %s", (new_name, old_name))
            elif choice == "2":
                name = input("Name: ").strip()
                new_email = input("New email: ").strip()
                cur.execute("UPDATE phonebook SET email = %s WHERE first_name = %s", (new_email, name))
            elif choice == "3":
                name = input("Name: ").strip()
                new_birthday = input("New birthday (YYYY-MM-DD): ").strip()
                cur.execute("UPDATE phonebook SET birthday = %s WHERE first_name = %s", (new_birthday, name))
            elif choice == "4":
                name = input("Name: ").strip()
                group = input("Group: ").strip()
                cur.execute("CALL move_to_group(%s, %s)", (name, group))
            print("Updated.")


def query_contacts():
    print("1. All contacts\n2. Search by name\n3. Search by email\n4. Filter by group\n5. Search by pattern")
    choice = input("Choice: ").strip()

    sort_by = input("Sort by (name/birthday/date, default=name): ").strip() or "name"
    sort_map = {"name": "pb.first_name", "birthday": "pb.birthday", "date": "pb.created_at"}
    order = sort_map.get(sort_by, "pb.first_name")

    conn = get_connection()
    if not conn:
        return

    base_query = """
        SELECT pb.id, pb.first_name, pb.email, pb.birthday, g.name, ph.phone, ph.type
        FROM phonebook pb
        LEFT JOIN groups g ON pb.group_id = g.id
        LEFT JOIN phones ph ON ph.contact_id = pb.id
    """

    with conn.cursor() as cur:
        if choice == "1":
            cur.execute(f"{base_query} ORDER BY {order}")
        elif choice == "2":
            name = input("Name: ").strip()
            cur.execute(f"{base_query} WHERE pb.first_name ILIKE %s ORDER BY {order}", (f"%{name}%",))
        elif choice == "3":
            email = input("Email: ").strip()
            cur.execute(f"{base_query} WHERE pb.email ILIKE %s ORDER BY {order}", (f"%{email}%",))
        elif choice == "4":
            group = input("Group (Family/Work/Friend/Other): ").strip()
            cur.execute(f"{base_query} WHERE g.name = %s ORDER BY {order}", (group,))
        elif choice == "5":
            pattern = input("Search pattern: ").strip()
            cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
            rows = cur.fetchall()
            if rows:
                for row in rows:
                    print(f"{row[0]}. {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} ({row[6]})")
            else:
                print("No contacts found.")
            conn.close()
            return

        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(f"{row[0]}. {row[1]} | {row[2]} | {row[3]} | group: {row[4]} | {row[5]} ({row[6]})")
        else:
            print("No contacts found.")
    conn.close()


def paginated_view():
    limit = int(input("Records per page: ").strip())
    page = 1
    conn = get_connection()
    if not conn:
        return

    while True:
        offset = (page - 1) * limit
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
            rows = cur.fetchall()

        if not rows:
            print("No more contacts.")
            break

        for row in rows:
            print(f"{row[0]}. {row[1]} | {row[2]} | {row[3]}")

        print(f"\nPage {page} | next / prev / quit")
        cmd = input("Command: ").strip().lower()
        if cmd == "next":
            page += 1
        elif cmd == "prev" and page > 1:
            page -= 1
        elif cmd == "quit":
            break

    conn.close()


def add_phone():
    name = input("Contact name: ").strip()
    phone = input("Phone: ").strip()
    phone_type = input("Type (home/work/mobile): ").strip() or "mobile"
    conn = get_connection()
    if not conn:
        return
    with conn:
        with conn.cursor() as cur:
            try:
                cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))
                print("Phone added.")
            except Exception as e:
                print(f"Error: {e}")
    conn.close()


def upsert_contact():
    name = input("Name: ").strip()
    phone = input("Phone: ").strip()
    conn = get_connection()
    if not conn:
        return
    with conn:
        with conn.cursor() as cur:
            cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    print("Done.")
    conn.close()


def bulk_insert():
    data = []
    print("Enter contacts (empty name to stop):")
    while True:
        name = input("Name: ").strip()
        if not name:
            break
        phone = input("Phone: ").strip()
        data.append([name, phone])
    if not data:
        return
    conn = get_connection()
    if not conn:
        return
    with conn:
        with conn.cursor() as cur:
            cur.execute("CALL bulk_insert_contacts(%s::VARCHAR[][])", (data,))
    print("Done.")
    conn.close()


def delete_contact():
    value = input("Enter name or phone to delete: ").strip()
    conn = get_connection()
    if not conn:
        return
    with conn:
        with conn.cursor() as cur:
            cur.execute("CALL delete_contact(%s)", (value,))
    print("Deleted.")
    conn.close()


def export_to_json():
    conn = get_connection()
    if not conn:
        return
    with conn.cursor() as cur:
        cur.execute("""
            SELECT pb.id, pb.first_name, pb.email, pb.birthday::TEXT, g.name,
                   json_agg(json_build_object('phone', ph.phone, 'type', ph.type)) AS phones
            FROM phonebook pb
            LEFT JOIN groups g ON pb.group_id = g.id
            LEFT JOIN phones ph ON ph.contact_id = pb.id
            GROUP BY pb.id, pb.first_name, pb.email, pb.birthday, g.name
            ORDER BY pb.id
        """)
        rows = cur.fetchall()

    contacts = []
    for row in rows:
        contacts.append({
            "id": row[0],
            "first_name": row[1],
            "email": row[2],
            "birthday": row[3],
            "group": row[4],
            "phones": row[5] if row[5] else []
        })

    filepath = input("Export filepath (e.g. contacts.json): ").strip()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)
    print(f"Exported {len(contacts)} contacts to {filepath}.")
    conn.close()


def import_from_json():
    filepath = input("JSON filepath: ").strip()
    with open(filepath, encoding="utf-8") as f:
        contacts = json.load(f)

    conn = get_connection()
    if not conn:
        return

    with conn:
        with conn.cursor() as cur:
            for c in contacts:
                cur.execute("SELECT id FROM phonebook WHERE first_name = %s", (c["first_name"],))
                existing = cur.fetchone()

                if existing:
                    action = input(f'"{c["first_name"]}" already exists. Skip or overwrite? (s/o): ').strip().lower()
                    if action != "o":
                        continue
                    cur.execute(
                        "UPDATE phonebook SET email = %s, birthday = %s WHERE first_name = %s",
                        (c.get("email"), c.get("birthday"), c["first_name"])
                    )
                    contact_id = existing[0]
                    cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))
                else:
                    cur.execute(
                        "INSERT INTO phonebook (first_name, email, birthday) VALUES (%s, %s, %s) RETURNING id",
                        (c["first_name"], c.get("email"), c.get("birthday"))
                    )
                    contact_id = cur.fetchone()[0]

                for ph in c.get("phones", []):
                    cur.execute(
                        "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                        (contact_id, ph["phone"], ph.get("type", "mobile"))
                    )

                if c.get("group"):
                    cur.execute("CALL move_to_group(%s, %s)", (c["first_name"], c["group"]))

    print("Import done.")
    conn.close()


def main():
    create_table()
    while True:
        print("\n1.  Import from CSV")
        print("2.  Add contact")
        print("3.  Update contact")
        print("4.  Search / Filter contacts")
        print("5.  Paginated view")
        print("6.  Add phone to contact")
        print("7.  Upsert contact")
        print("8.  Bulk insert")
        print("9.  Delete contact")
        print("10. Export to JSON")
        print("11. Import from JSON")
        print("0.  Exit")
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
            paginated_view()
        elif choice == "6":
            add_phone()
        elif choice == "7":
            upsert_contact()
        elif choice == "8":
            bulk_insert()
        elif choice == "9":
            delete_contact()
        elif choice == "10":
            export_to_json()
        elif choice == "11":
            import_from_json()
        elif choice == "0":
            break


if __name__ == "__main__":
    main()