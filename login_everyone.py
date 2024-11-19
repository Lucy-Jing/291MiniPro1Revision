# Khanh, Darlene, Norman,Lucy
# Last update: Nov 12, 2024

# login_everyone.py

'''import sys
import getpass
import sqlite3'''

def LogInPage(connection, cursor):
    login_state = False
    while not login_state:
        inputs = input("Are you registered? (y/n): ").strip().lower()
        if inputs == "y":
            if sys.stdin.isatty():
                print("Enter your login ")
                user_id = input("Enter your user ID: ").strip()
                password = getpass.getpass("Enter your password: ").strip()
                
                # Check if the 'users' table exists
                cursor.execute("""
                    SELECT name FROM sqlite_master WHERE type='table' AND name='users';
                """)
                if not cursor.fetchone():
                    print("Error: The 'users' table does not exist. Please initialize your database.")
                    return None, False
                
                # Query to check if the user exists
                query = """
                    SELECT 1 FROM users WHERE usr = ? AND pwd = ?;
                """
                cursor.execute(query, (user_id, password))
                result = cursor.fetchone()
                if result:
                    login_state = True
                    print("Logged in successfully.")
                    return user_id, login_state
                else:
                    print("Invalid user ID or password. Please try again.")
        elif inputs == "n":
            if sys.stdin.isatty():
                print("Register a new account")
                name = input("Enter your name: ").strip()

                # Validate email
                while True:
                    email = input("Enter your email: ").strip()
                    if '@' in email and '.' in email:
                        break
                    else:
                        print("Invalid email. Please include '@' and '.' in your email address.")

                # Validate phone number
                while True:
                    phone = input("Enter your phone: ").strip()
                    if phone.isdigit():
                        break
                    else:
                        print("Your phone number should contain only digits. Please try again.")

                pwd = getpass.getpass("Enter your password: ").strip()
                
                user_id = get_user_length(cursor)

                # Insert the new user into the 'users' table
                query = """
                    INSERT INTO users (usr, name, email, phone, pwd) VALUES (?, ?, ?, ?, ?);
                """
                cursor.execute(query, (user_id, name, email, phone, pwd))
                connection.commit()
                print(f"Registration successful. Your user ID is: {user_id}")
                login_state = True
                return user_id, login_state
        elif inputs == "exit":
            sys.exit()
        else:
            print("Invalid input, please enter 'y', 'n', or 'exit' to cancel.")

def get_user_length(cursor):
    query = """
        SELECT MAX(usr) FROM users;
    """
    cursor.execute(query)
    output = cursor.fetchone()
    # If there are no users, start with ID 1
    return (output[0] or 0) + 1
