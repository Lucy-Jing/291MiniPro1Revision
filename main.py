from compose_tweets_darlene import compose_tweet, compose_retweet
from data_sample_lucy import insert_data
from  define_tables import  define_tables 
from list_followers_lucy import list_followers
from login_everyone import LogInPage
from search_for_tweets_khanh import search_tweets
from search_for_users_norman import search_user, show_user_info
import sqlite3
import string
import sys
from login_display_khanh import login_display
connection = None
cursor = None
user_id = None
is_show_more = 0
def connect(path):
    global connection, cursor
    
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return connection, cursor
def main():
    # Define variables
    global is_show_more
    isLogin = False

    if len(sys.argv) < 2:
        print("Error: Please provide a database name after main.py.")
        sys.exit(1)
    # Connect to the database
    print("db name: " + str(sys.argv[1]))
    connection, cursor = connect(sys.argv[1])
    
    while True:  # Infinite loop to allow re-login after logout

        while not isLogin:
            curr_user, isLogin = LogInPage(connection, cursor)
            if isLogin:
                user_id = curr_user
            else:
                print("Login failed. Please try again.")
                
        print("=" * 50)
        print("/\\/\\/\\/\\/\\   WELCOME BACK!  /\\/\\/\\/\\/\\\\".center(50))
        login_display(connection, cursor, user_id, is_show_more)
        # Main interaction loop for logged-in users
        while isLogin:
            # print(user_id, is_show_more)
            
            print('=' * 50)
            user_input = input("What do you want to do: ").lower()
            print('=' * 50)

            if user_input == "search tweet":
                search_tweets(connection, cursor, user_id)
                print('=' * 50)
            elif user_input == "tweet":
                compose_tweet(connection, cursor, user_id)
            elif user_input == "retweet":
                tid = input("Enter the tweet ID you currently view: ")
                compose_retweet(connection, cursor, user_id, tid)
            elif user_input == "reply":
                replyto_tid = input("Enter the tweet ID you want to reply to: ")
                compose_tweet(connection, cursor, user_id, replyto_tid)
            elif user_input == "list followers":
                list_followers(cursor, user_id)
                print('=' * 50)
            elif user_input == "search user":
                keyword = input("Enter the user name you want to search for: ")
                search_user(connection, cursor, keyword, user_id)
                print('=' * 50)
            elif user_input == "logout" or user_input == "log out":
                isLogin = False
                user_id = None
                print("...")
                print("You have been logged out.".center(50))
                print('=' * 50)
            elif user_input == "next tweets":
                is_show_more+=1
                if login_display(connection, cursor, user_id, is_show_more) ==[]:
                    print("No more tweets to display, revert to previous page")
                    print("==================================================")
                    is_show_more-=1
                    login_display(connection, cursor, user_id, is_show_more)
                else: login_display(connection, cursor, user_id, is_show_more)
            elif user_input == "previous tweets":
                if is_show_more >=0:
                    is_show_more-=1
                    login_display(connection, cursor, user_id, is_show_more)
                else:
                    print("cant go back with the tweets further more")
                    print("==================================================")
                    login_display(connection, cursor, user_id, is_show_more)
            elif user_input == "exit":
                connection.close()
                return
            else:
                print("Invalid option. Please try again.")

    # Close the connection when done (will only be reached if loop breaks)
    connection.close()



def print_all_data(cursor):

# List of tables in the database
    tables = ["users", "follows", "tweets", "lists", "include", "retweets", "hashtag_mentions"]

    for table in tables:
        print(f"\nTable: {table}")
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("No data available")

    return ""

if __name__ == "__main__":
    main()

    # conn, cursor = connect("test.db")

    # print_all_data(cursor)
