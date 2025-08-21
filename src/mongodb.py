from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

HOST="localhost"
PORT=27017
USER="lisahadmin"
CLS="L1s4hUn14nd3s"
DATABASE_NAME="lisah"
AUTH_SOURCE = "admin"

MONGO_URI = f"mongodb://{USER}:{CLS}@{HOST}:{PORT}/?authSource={AUTH_SOURCE}"
try:
    conn = AsyncIOMotorClient(MONGO_URI)
    print(conn)
except Exception as e:
    print("Error:", e)
finally:
    db = conn[DATABASE_NAME] 
