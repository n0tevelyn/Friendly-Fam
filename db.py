import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'duckduckgoose',
    'database': 'firstdatabase'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def init_db():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(200) NOT NULL
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INT AUTO_INCREMENT PRIMARY KEY,
        host VARCHAR(100) NOT NULL,
        description VARCHAR(200) NOT NULL,
        day VARCHAR(50) NOT NULL,
        time VARCHAR(50) NOT NULL
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(200) NOT NULL
    );
    """)
    connection.commit()
    cursor.close()
    connection.close()

class Login:
    @staticmethod
    def add(username, password):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO login (username, password) VALUES (%s, %s)",
            (username, password)
        )
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def get_by_username(username):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM login WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        return user

class Event:
    @staticmethod
    def add(host, description, day, time):
        connection = get_db_connection()
        cursor = connection.cursor()
        
        print(f"Inserting event: host={host}, description={description}, day={day}, time={time}")
        
        cursor.execute(
            "INSERT INTO events (host, description, day, time) VALUES (%s, %s, %s, %s)",
            (host, description, day, time)
        )
        
        connection.commit()
        print("Event added successfully!")
        cursor.close()
        connection.close()
    @staticmethod
    def get_by_id(event_id):
        """Retrieve an event by its ID."""
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
        event = cursor.fetchone()
        cursor.close()
        connection.close()
        return event
    @staticmethod
    def get_all():
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()

        print(f"Fetched events: {events}")
        cursor.close()
        connection.close()
        return events

    @staticmethod
    def get_by_host(host):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM events WHERE host = %s", (host,))
        events = cursor.fetchall()
        print(f"Fetched events for host {host}: {events}")
        cursor.close()
        connection.close()
        return events
    
    @staticmethod
    def delete(event_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
            connection.commit()
            print(f"Deleted event with ID: {event_id}")
        except Exception as e:
            print(f"Error deleting event: {e}")
            raise
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update(event_id, description, day, time):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            query = """
            UPDATE events
            SET description = %s, day = %s, time = %s
            WHERE id = %s
            """
            cursor.execute(query, (description, day, time, event_id))
            connection.commit()
            print(f"Updated event with ID: {event_id}")
        except Exception as e:
            print(f"Error updating event: {e}")
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()



class User:
    @staticmethod
    def add(username, password):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO login (username, password) VALUES (%s, %s)",
            (username, password)
        )
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def get_by_username(username):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM login WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        return user


def add(host, description, day, time):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:

        print(f"Inserting event: host={host}, description={description}, day={day}, time={time}")
        query = """
        INSERT INTO events (host, description, day, time) 
        VALUES (%s, %s, %s, %s)
        """
        values = (host, description, day, time)
        
        cursor.execute(query, values)
        connection.commit()
        

        event_id = cursor.lastrowid
        print(f"Event added successfully with ID: {event_id}")
        return event_id
    
    except mysql.connector.Error as err:

        print(f"MySQL Error: {err}")
        print(f"Error Code: {err.errno}")
        print(f"SQL State: {err.sqlstate}")
        print(f"Error Message: {err.msg}")
        
        connection.rollback()

    
    finally:
        cursor.close()
        connection.close()
init_db()
