import bcrypt
import jwt,datetime

def user_exists(user_id: int,users_collection) -> bool:
    """
    Checks if a user exists in the MongoDB collection by user_id.
    
    Parameters:
        user_id (int): The user ID to search for.
    
    Returns:
        bool: True if the user exists, False otherwise.
    """
    # Query to find the user by user_id
    user = users_collection.find_one({"user_id": user_id})
    
    # Return True if the user exists, False if not
    return user is not None


def verify_jwt_token(token: str, secret_key: str, algorithms: list = ["HS256"]) -> dict:
    """
    Verifies and decodes a JWT token.
    
    Parameters:
        token (str): The JWT token to verify.
        secret_key (str): The secret key to verify the token.
        algorithms (list): List of algorithms to use for verification (default is ["HS256"]).
    
    Returns:
        dict: The decoded payload if the token is valid.
    
    Raises:
        jwt.ExpiredSignatureError: If the token has expired.
        jwt.InvalidTokenError: If the token is invalid.
    """
    try:
        decoded_payload = jwt.decode(token, secret_key, algorithms=algorithms)
        return decoded_payload
    except jwt.ExpiredSignatureError:
        print("Token has expired!")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token!")
        return None


def create_jwt_token(payload: dict, secret_key="vdfuycwbeinhhvq4b6719t3y89n5y340tputh3c mrew    uvygn847ytv798`34yc04tn`y347yvtn1034tyv`n830y4t8-`y4ty0813ytn8y3-t89n4-89177tv80y837t5gyn18ovtuyo3  btg4p   4ny9t]  9n4tu   3[4ty08qvb5y9t  [b34yv-9348]]", algorithm: str = "HS256") -> str:
    """
    Generates a JWT token.
    
    Parameters:
        payload (dict): The data to encode in the token.
        secret_key (str): The secret key to sign the token.
        algorithm (str): The algorithm to use for signing the token (default is "HS256").
    
    Returns:
        str: The generated JWT token.
    """
    # Set an expiration time for the token
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    payload["exp"] = expiration
    
    # Encode the payload to create the JWT token
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

def encrypt_password(password: str) -> str:
    """
    Encrypts a password using bcrypt hashing.
    
    Parameters:
        password (str): The plain text password to encrypt.
    
    Returns:
        str: The hashed password.
    """
    # Generate a salt
    salt = bcrypt.gensalt()
    
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    # Return the hashed password as a string
    return hashed_password.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies a password against a given hashed password.
    
    Parameters:
        password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.
    
    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    # Compare the provided password with the stored hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


