from fastapi import FastAPI, HTTPException
import model
from pymongo import MongoClient, errors
import utilities
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
# Use the MONGO_URL environment variable
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
db = client["ipo"]
collection = db["user_info"]

# Initialize FastAPI app
app = FastAPI()

# Login endpoint
@app.post("/login")
def login(info: model.Login):
    try:
        # Check if user exists

        if utilities.user_exists(info.user_id, collection)==False:
            raise HTTPException(status_code=404, detail="User not found. Please sign up first.")
        # Retrieve user data
        data = collection.find_one({"email": info.email})
        if not data:
            raise HTTPException(status_code=404, detail="User email not found. Please check and try again.")

        # Verify password
        if not utilities.verify_password(info.password, data['password']):
            raise HTTPException(status_code=401, detail="Incorrect password. Please try again.")
        # Generate JWT token
        token = utilities.create_jwt_token({"user_id": data['user_id']})
        return {
            "message": "Welcome",
            "token": token
        }
    
    except HTTPException as e:
        # Re-raise specific HTTPExceptions to handle them as intended
        raise e
    except errors.PyMongoError as e:
        # Handle MongoDB-specific errors
        raise HTTPException(status_code=500, detail="Database error occurred.")
    except Exception as e:
        # General exception for other unexpected errors
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

# Signup endpoint
@app.post("/signup")
def sign(info: model.signup):
    try:
        # Check if user already exists
        if utilities.user_exists(info.user_id, collection):
            raise HTTPException(status_code=409, detail="User already exists. Please log in instead.")

        # Encrypt password and create user data
        encrypted_password = utilities.encrypt_password(info.password)
        data = {
            "first_name": info.first_name,
            "last_name": info.last_name,
            "email": info.email,
            "password": encrypted_password,
            "user_id": info.user_id
        }

        # Insert user data into MongoDB
        collection.insert_one(data)

        # Generate JWT token
        token = utilities.create_jwt_token({"user_id": info.user_id})
        return {
            "message": "The user has been added to the database.",
            "token": token
        }
    
    except HTTPException as e:
        # Re-raise specific HTTPExceptions to handle them as intended
        raise e
    except errors.PyMongoError as e:
        # Handle MongoDB-specific errors
        raise HTTPException(status_code=500, detail="Database error occurred.")
    except Exception as e:
        # General exception for other unexpected errors
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
