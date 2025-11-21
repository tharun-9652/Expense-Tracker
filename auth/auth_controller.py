from models.user import register_user, authenticate
from utils.jwt_utils import create_token

def register(username, password):
    ok = register_user(username, password)
    return ok

def login(username, password):
    user = authenticate(username, password)
    if not user:
        return None
    return create_token(user["id"])
