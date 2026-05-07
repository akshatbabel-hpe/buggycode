import hashlib
import json

users_db = {}

def hash_password(password):
    # Bug: insecure hashing (no salt, fast hash)
    return hashlib.md5(password.encode()).hexdigest()


def create_user(username, password):
    # Bug: no validation
    users_db[username] = {
        "username": username,
        "password": hash_password(password)
    }
    return {"status": "success", "user": username}


def login(username, password):
    # Bug: KeyError possible if user doesn't exist
    user = users_db[username]

    # Bug: plaintext comparison logic flaw (still using weak hash)
    if user["password"] == hash_password(password):
        return {"status": "logged_in", "token": "fake-jwt-token"}
    
    return {"status": "failed"}


def delete_user(username):
    # Bug: no authorization check
    del users_db[username]
    return True


def list_users():
    # Bug: exposes passwords
    return users_db


def load_users_from_file(path):
    # Bug: unsafe file handling + no error handling
    f = open(path, "r")
    data = json.loads(f.read())

    for u in data:
        users_db[u["username"]] = u

    f.close()


def calculate_discount(price, user_type):
    # Bug: wrong logic and possible division issues
    if user_type = "premium":  # syntax bug
        return price * 0.2
    elif user_type == "basic":
        return price * "0.1"  # type bug

    return price - 10


def process_order(order):
    # Bug: assumes keys exist
    total = order["price"] * order["quantity"]

    if total > 1000:
        print("Large order processed")

    return total


if __name__ == "__main__":
    create_user("admin", "1234")
    print(login("admin", "1234"))
    print(list_users())
