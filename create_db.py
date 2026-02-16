from dotenv import load_dotenv
import os, sys, sqlite3

# Load environment variables
load_dotenv()
db = os.getenv("DB_PATH")

# Check environment variables existence
if db is None or db=="":
    sys.exit("Fatal error: database path not set. Insert it in your .env file.")
else:
    print("Database path loaded: " + db)

# Open connection (and creates db if not existing)
con = sqlite3.connect(db)



# Queries to create the four tables
con.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    name CHAR(32),
    username CHAR(32)
    );
    """
)
con.execute(
    """
    CREATE TABLE IF NOT EXISTS fairs (
    fair_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(32),
    description TEXT
    );
    """
)
con.execute(
    """
    CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fair_id INTEGER,
    owner_id INTEGER,
    name CHAR(32),
    description TEXT,
    FOREIGN KEY(fair_id) REFERENCES fairs(fair_id),
    FOREIGN KEY(owner_id) REFERENCES users(user_id)
    );
    """
)
con.execute(
    """
    CREATE TABLE IF NOT EXISTS slots (
    slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER,
    user_id INTEGER,
    start_time TEXT,
    end_time TEXT,
    FOREIGN KEY(event_id) REFERENCES events(event_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id)
    );
    """
)
# NOTE: 'start_time' and 'end_time' are datetime objects represented as
# a time string in the ISO-8601 format.



# Commit queries and close connection
con.commit()
con.close()
print("Database created successfully.")
