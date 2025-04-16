import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Read values from .env
host = os.getenv("POSTGRES_HOST")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
new_db = os.getenv("NEW_DB_NAME")
new_user = os.getenv("NEW_DB_USER")
new_password = os.getenv("NEW_DB_PASSWORD")

# Connect to default postgres database
conn = psycopg2.connect(
    host=host,
    user=user,
    password=password
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Create a cursor
cursor = conn.cursor()

# Create database
try:
    cursor.execute(f"CREATE DATABASE {new_db};")
    print("Database created successfully!")
except psycopg2.errors.DuplicateDatabase:
    print("Database already exists.")

# Create user
try:
    cursor.execute(f"CREATE USER {new_user} WITH PASSWORD '{new_password}';")
    print("User created successfully!")
except psycopg2.errors.DuplicateObject:
    print("User already exists.")

# Grant privileges
try:
    cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {new_db} TO {new_user};")
    print("Privileges granted successfully!")
except Exception as e:
    print(f"Error granting privileges: {e}")

# Close everything
cursor.close()
conn.close()

print("Database setup complete!")