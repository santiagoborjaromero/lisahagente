import psycopg2
try:
    conn = psycopg2.connect(
        database="lisah",
        user="lisahadmin",
        password="L1s4hUn14nd3s",
        host="127.0.0.1", 
        port=5432
    )
    print("Connected to PostgreSQL successfully!")

except psycopg2.Error as e:
    print(f"Error connecting to PostgreSQL: {e}")