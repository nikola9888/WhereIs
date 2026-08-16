import os
import sqlite3
from datetime import datetime

from kivy.app import App


class Database:


    def __init__(self):

        self.db_path = self.get_database_path()


        self.conn = sqlite3.connect(
            self.db_path,
            timeout=10
        )


        self.conn.row_factory = sqlite3.Row


        self.cursor = self.conn.cursor()


        self.cursor.execute(
            "PRAGMA foreign_keys = ON"
        )


        self.create_tables()

        self.migrate()

        self.create_default_categories()



    # =================================================
    # PATH
    # =================================================

    def get_database_path(self):

        app = App.get_running_app()


        if app:

            folder = app.user_data_dir

        else:

            folder = "."


        os.makedirs(
            folder,
            exist_ok=True
        )


        return os.path.join(
            folder,
            "whereis.db"
        )



    # =================================================
    # TABLES
    # =================================================

    def create_tables(self):


        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT UNIQUE NOT NULL,

            icon TEXT DEFAULT '📦'

        )
        """)



        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS items(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            category_id INTEGER,

            location TEXT,

            description TEXT,

            image_path TEXT DEFAULT '',

            created_at TEXT DEFAULT CURRENT_TIMESTAMP,

            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,


            FOREIGN KEY(category_id)

            REFERENCES categories(id)

            ON DELETE SET NULL

        )
        """)



        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS item_history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            item_id INTEGER NOT NULL,

            action TEXT,

            location TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP,


            FOREIGN KEY(item_id)

            REFERENCES items(id)

            ON DELETE CASCADE

        )
        """)



        self.conn.commit()



    # =================================================
    # MIGRATION
    # =================================================

    def migrate(self):

        self.cursor.execute(
            "PRAGMA table_info(items)"
        )


        columns = [

            row["name"]

            for row in self.cursor.fetchall()

        ]


        if "updated_at" not in columns:

            self.cursor.execute(
                """
                ALTER TABLE items

                ADD COLUMN updated_at TEXT
                """
            )


        self.conn.commit()



    # =================================================
    # DEFAULT CATEGORY
    # =================================================

    def create_default_categories(self):


        categories = [

            ("Keys","🔑"),

            ("Documents","📄"),

            ("Electronics","📱"),

            ("Clothes","👕"),

            ("Tools","🔧"),

            ("Wallet","👛"),

            ("Other","📦")

        ]


        for name, icon in categories:


            self.cursor.execute(
                """
                SELECT id

                FROM categories

                WHERE name=?
                """,
                (name,)
            )


            if not self.cursor.fetchone():

                self.cursor.execute(
                    """
                    INSERT INTO categories
                    (name,icon)

                    VALUES (?,?)
                    """,
                    (
                        name,
                        icon
                    )
                )


        self.conn.commit()



    # =================================================
    # CATEGORIES
    # =================================================

    def get_categories(self):

        self.cursor.execute(
            """
            SELECT *

            FROM categories

            ORDER BY name
            """
        )


        return self.cursor.fetchall()



    # =================================================
    # ADD ITEM
    # =================================================

    def add_item(
        self,
        name,
        category_id,
        location,
        description,
        image_path=""
    ):


        self.cursor.execute(
            """
            INSERT INTO items

            (
            name,
            category_id,
            location,
            description,
            image_path
            )

            VALUES(?,?,?,?,?)

            """,
            (
                name,
                category_id,
                location,
                description,
                image_path
            )
        )


        self.conn.commit()


        return self.cursor.lastrowid



    # =================================================
    # GET ITEMS
    # =================================================

    def get_all_items(self):

        self.cursor.execute(
            """
            SELECT

            items.id,
            items.name,
            categories.name,
            categories.icon,
            items.location,
            items.description,
            items.image_path


            FROM items


            LEFT JOIN categories

            ON categories.id = items.category_id


            ORDER BY items.id DESC

            """
        )


        return [

            tuple(row)

            for row in self.cursor.fetchall()

        ]



    # =================================================
    # SINGLE ITEM
    # =================================================

    def get_item(self,item_id):


        self.cursor.execute(
            """
            SELECT *

            FROM items

            WHERE id=?

            """,
            (item_id,)
        )


        row = self.cursor.fetchone()


        return tuple(row) if row else None



    # =================================================
    # UPDATE ITEM
    # =================================================

    def update_item(
        self,
        item_id,
        name,
        category_id,
        location,
        description,
        image_path
    ):


        self.cursor.execute(
            """
            UPDATE items

            SET

            name=?,

            category_id=?,

            location=?,

            description=?,

            image_path=?,

            updated_at=CURRENT_TIMESTAMP


            WHERE id=?

            """,
            (
                name,
                category_id,
                location,
                description,
                image_path,
                item_id
            )
        )


        self.conn.commit()


# =================================================
# DELETE
# =================================================

    def delete_item(self, item_id):


        self.cursor.execute(
            """
            DELETE FROM item_history

            WHERE item_id=?
            """,
            (item_id,)
        )


        self.cursor.execute(
            """
            DELETE FROM items

            WHERE id=?
            """,
            (item_id,)
        )


        self.conn.commit()
        # =================================================
    # SEARCH
    # =================================================

    def search_items(self,text):

        value = f"%{text}%"


        self.cursor.execute(
            """
            SELECT

            items.id,
            items.name,
            categories.name,
            categories.icon,
            items.location,
            items.description,
            items.image_path


            FROM items


            LEFT JOIN categories

            ON categories.id=items.category_id


            WHERE

            items.name LIKE ?

            OR items.location LIKE ?

            OR items.description LIKE ?


            ORDER BY items.id DESC

            """,
            (
                value,
                value,
                value
            )
        )


        return [

            tuple(row)

            for row in self.cursor.fetchall()

        ]



    # =================================================
    # HISTORY
    # =================================================

    def add_history(
        self,
        item_id,
        action,
        location
    ):


        self.cursor.execute(
            """
            INSERT INTO item_history

            (
            item_id,
            action,
            location
            )

            VALUES(?,?,?)

            """,
            (
                item_id,
                action,
                location
            )
        )


        self.conn.commit()



    def get_item_history(self,item_id):

        self.cursor.execute(
            """
            SELECT

            action,
            location,
            created_at


            FROM item_history


            WHERE item_id=?


            ORDER BY id DESC

            """,
            (item_id,)
        )


        return [

            tuple(row)

            for row in self.cursor.fetchall()

        ]



    # =================================================
    # CLOSE
    # =================================================

    def close(self):

        if self.conn:

            self.conn.commit()

            self.conn.close()