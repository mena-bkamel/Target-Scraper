import sqlite3
from datetime import datetime as dt


def create_db(db_name: str = "file.db", table_name="Product"):
    # Connect to the database (or create it if it doesn't exist)
    db_name = db_name.replace(" ", "_") + ".db"
    try:
        with sqlite3.connect(db_name) as conn:
            # Create a cursor object to execute SQL commands
            cursor = conn.cursor()

            cursor.execute(f'''CREATE TABLE IF NOT EXISTS 
                    "{table_name}" (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_name TEXT NOT NULL,
                        price REAL,
                        num_reviews TEXT,
                        url TEXT,
                        date TEXT
                        )''')
            conn.commit()
            print(f"Database '{db_name}' and table '{table_name}' created successfully.")

    except sqlite3.Error as err:
        print(f"Error creating database or table: {err}")


def save_product_database(db_name, product_name, price, num_reviews, url, table_name="Product"):

    db_name = db_name.replace(" ", "_") + ".db"
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()

        try:
            cursor.execute(
                f"INSERT INTO '{table_name}' (product_name, price, num_reviews, url, date) VALUES (?, ?, ?, ?, ?)",
                (product_name, price, num_reviews, url, dt.now().strftime("%Y-%m-%d")))
        except sqlite3.Error as err:
            print(f"Error saving data to '{db_name}.db': {err}")

        conn.commit()



