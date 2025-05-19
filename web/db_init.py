from mysql.connector import errorcode
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}


def init_db():
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        with open('init_db.sql', 'r') as f:
            sql = f.read()
            queries = sql.split(';')
            for query in queries:
                try:
                    if query.strip() != '':
                        cursor.execute(query)
                        conn.commit()
                        print("Query executed successfully!")
                except Exception as e:
                    print("Error executing query:", str(e))
        conn.commit()
        print("Database initialized successfully.")
    except mysql.connector.Error as err:
        print("Error initializing DB:", err)
        raise err
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    init_db()
