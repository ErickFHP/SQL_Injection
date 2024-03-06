import sqlite3

def start_Db():
    CREATE_TABLE_USERS = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        pass VARCHAR(255) NOT NULL
    );
    """
    INSERT_USER1 = """
    INSERT INTO users (id, name, email, pass) VALUES
    (1, 'Juan', 'usuario1@ejemplo.com', '123') ON CONFLICT DO NOTHING;
    """
    INSERT_USER2 = """
    INSERT INTO users (id, name, email, pass) VALUES
    (2, 'Luz', 'usuario2@ejemplo.com', '456') ON CONFLICT DO NOTHING;
    """

    INSERT_USER3 = """
    INSERT INTO users (id, name, email, pass) VALUES
    (3, 'Hugo', 'usuario3@ejemplo.com', '789') ON CONFLICT DO NOTHING;
    """

    conn=sqlite3.connect("db.sqlite3")
    cursor=conn.cursor()
    cursor.execute(CREATE_TABLE_USERS)
    cursor.execute(INSERT_USER1)
    cursor.execute(INSERT_USER2)
    cursor.execute(INSERT_USER3)
    conn.commit()
    conn.close()
