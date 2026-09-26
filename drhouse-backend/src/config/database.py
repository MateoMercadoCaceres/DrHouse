from pymongo import MongoClient
from pymongo.database import Database
import os

class MongoDB:
    client: MongoClient = None
    database: Database = None

db = MongoDB()

def get_database() -> Database:
    """Get database instance"""
    if db.database is None:
        raise Exception("Database not initialized. Call connect_to_mongo() first.")
    return db.database

def connect_to_mongo():
    """Create database connection"""
    mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    db_name = os.getenv("DB_NAME", "userapi")
    
    try:
        print(f"🔄 Connecting to MongoDB at {mongo_url}...")
        db.client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
        
        # Test the connection
        db.client.admin.command('ping')
        print("✅ MongoDB connection successful")
        
        db.database = db.client[db_name]
        print(f"✅ Using database: {db_name}")
        
        # Create indexes (with error handling)
        try:
            db.database.users.create_index("username", unique=True)
            db.database.users.create_index("email", unique=True)
            print("✅ Database indexes created")
        except Exception as index_error:
            print(f"⚠️  Warning creating indexes: {index_error}")
        
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        db.client = None
        db.database = None
        raise

def close_mongo_connection():
    """Close database connection"""
    if db.client is not None:
        db.client.close()
        db.client = None  
        db.database = None
        print("✅ MongoDB connection closed")
