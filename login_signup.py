"""
This code uses the json module to store the users dictionary in a file named users.json. The load_users() function loads the user information from the file when the program starts, and the save_users() function saves the user information to the file after each registration.

When a user registers, their information is added to the users dictionary and saved to the file using save_users(). When a user logs in, their information is checked against the users dictionary as before.
"""


import json

users = {}

def load_users():
    try:
        with open("users.json", "r") as f:
            users.update(json.load(f))
    except FileNotFoundError:
        pass

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f)

def register():
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    users[username] = password
    save_users()
    print("Registration successful!")

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username in users and users[username] == password:
        print("Login successful!")
    else:
        print("Invalid username or password.")

load_users()

while True:
    choice = input("Enter 1 to register, 2 to login, or 3 to quit: ")
    if choice == "1":
        register()
    elif choice == "2":
        login()
    elif choice == "3":
        break

save_users()