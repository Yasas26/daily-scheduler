import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="daily_scheduler",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
