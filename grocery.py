import sqlite3
from tabulate import tabulate

# ----------------- Database Setup -----------------
conn = sqlite3.connect("grocery.db")
cur = conn.cursor()

tables = {
    "items": ["name", "category", "price"],
    "employees": ["name", "post", "salary"]
}

# Create tables if not exist
cur.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    price REAL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    post TEXT,
    salary REAL
)
""")
conn.commit()


# ----------------- Generic Functions -----------------
def get_input(field):
    """Handle input with numeric validation for price/salary."""
    while True:
        value = input(f"Enter {field}: ")
        if field in ["price", "salary"]:
            try:
                return float(value)
            except ValueError:
                print(" Invalid number. Try again.")
        else:
            if value.strip():
                return value
            else:
                print(" Cannot be empty.")


def add_record(table):
    fields = tables[table]
    values = [get_input(field) for field in fields]
    placeholders = ", ".join(["?"] * len(fields))
    cur.execute(f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({placeholders})", values)
    conn.commit()
    print(" Record added successfully!\n")


def view_records(table):
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    if rows:
        print(tabulate(rows, headers=["ID"] + tables[table], tablefmt="fancy_grid"))
    else:
        print(f"❌ No records found in {table}.\n")


def search_records(table):
    field = tables[table][0]  # search by first field (usually name)
    keyword = input(f"Enter {field} to search: ")
    cur.execute(f"SELECT * FROM {table} WHERE {field} LIKE ?", ('%' + keyword + '%',))
    rows = cur.fetchall()
    if rows:
        print(tabulate(rows, headers=["ID"] + tables[table], tablefmt="fancy_grid"))
    else:
        print(" Record not found.\n")


def update_record(table):
    view_records(table)
    try:
        record_id = int(input(f"Enter {table[:-1]} ID to update: "))
    except ValueError:
        print(" Invalid ID!")
        return

    fields = tables[table]
    values = [get_input(field) for field in fields]
    values.append(record_id)
    cur.execute(f"UPDATE {table} SET {', '.join([f + '=?' for f in fields])} WHERE id=?", values)
    conn.commit()
    print(" Record updated successfully!\n")


def delete_record(table):
    view_records(table)
    try:
        record_id = int(input(f"Enter {table[:-1]} ID to delete: "))
    except ValueError:
        print(" Invalid ID!")
        return
    cur.execute(f"DELETE FROM {table} WHERE id=?", (record_id,))
    conn.commit()
    print(" Record deleted successfully!\n")


# ----------------- Menu System -----------------
def manage_table(table):
    while True:
        print(f"""
------ {table.upper()} MENU ------
1. Add
2. View
3. Search
4. Update
5. Delete
6. Back
""")
        choice = input("Enter choice: ")
        if choice == "1": add_record(table)
        elif choice == "2": view_records(table)
        elif choice == "3": search_records(table)
        elif choice == "4": update_record(table)
        elif choice == "5": delete_record(table)
        elif choice == "6": break
        else: print(" Invalid choice!")


def main_menu():
    while True:
        print("""
==============================================
          GROCERY STORE MANAGEMENT 
==============================================
1. Manage Items
2. Manage Employees
3. Exit
""")
        choice = input("Enter your choice: ")
        if choice == "1": manage_table("items")
        elif choice == "2": manage_table("employees")
        elif choice == "3":
            print(" Exiting... Goodbye!")
            break
        else:
            print(" Invalid choice!")


# ----------------- Run App -----------------
if __name__ == "__main__":
    main_menu()
    conn.close()
