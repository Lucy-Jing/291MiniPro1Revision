# Norman Wong
# Last update: Nov 14, 2024

import sqlite3
from datetime import datetime 

def search_user(connection, cursor, keyword,current_user_id, offset = 0, limit = 5):

    cursor.execute('''
        SELECT usr, name
        FROM users
        WHERE LOWER(name) LIKE ?
        ORDER BY LENGTH(name) ASC
        LIMIT ? OFFSET ? 
    ''', (f"%{keyword}%", limit, offset))

    results = cursor.fetchall()
    
    if not results and offset == 0:
        print("No matching users found.")
    elif not results and offset > 0:
        print("No more matching users found.")
    else:
        print("Matching users:")
        for i, (user_id, username) in enumerate(results, start = offset + 1):
            print(f"{i}. ID: {user_id}, Username: {username}")
        print("\nDo you want to see more results? (y/n)")
        choice = input().strip().lower()
        if choice == 'y':
            new_offset = offset + limit
            search_user(connection, cursor, keyword, current_user_id, new_offset, limit)
        elif choice == 'n':
            loop_state = True
            while loop_state:
                print("\nEnter the ID of the user you would like to know more about. To exit, type 'exit'.")
                selected = input().strip().lower()
                if selected == 'exit':
                    loop_state = False
                    return
                try:
                    selected = int(selected)
                    cursor.execute('''
                        SELECT usr, name
                        FROM users
                        WHERE usr LIKE ?
                    ''', (f"%{selected}%",))
                    selected_user_info = cursor.fetchone()
                    selected_user_id = selected_user_info[0]
                    print(selected_user_info)
                    if selected_user_info:
                        show_user_info(connection, cursor, current_user_id, selected_user_id, selected_user_info, 0)
                except ValueError:
                    print("Invalid user ID. Please try again.")
        else:
            print("Invalid input. Please try again.")


def show_user_info(connection, cursor, current_user_id, user_id, user_info, offset=5):
    cursor.execute("""
        SELECT COUNT(*)
        FROM tweets
        WHERE writer_id = ?
    """, (user_id,))
    tweet_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM follows
        WHERE flwer = ?
    """, (user_id,))
    following_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM follows
        WHERE flwee = ?
    """, (user_id,))
    follower_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT text
        FROM tweets
        WHERE writer_id = ?
        ORDER BY tdate DESC, ttime DESC
        LIMIT 3 OFFSET ?
    """, (user_id, offset))
    recent_tweets = [tweet[0] for tweet in cursor.fetchall()]

    print(f"User: {user_info[1]}")
    print(f"Tweet count: {tweet_count}")
    print(f"Following: {following_count}")
    print(f"Followers: {follower_count}")
    if len(recent_tweets) == 0 and offset == 0:
        print('This user has not posted any tweets.')
    elif len(recent_tweets) == 0 and offset > 0:
        print('There are no more tweets.')
    else: 
        print(f"Recent Tweets: {recent_tweets}")

    loop_state = True
    while loop_state:
        print("To follow this user, type 'follow'. To see more tweets, type 'see more'. To exit, type 'exit'.")
        choice = input().strip().lower()
        if choice == 'exit':
            loop_state = False
            return
        
        elif choice == 'follow':    # This is the follow functionality 

            # Check if you are trying to follow yourself
            if current_user_id == user_id:
                print("You cannot follow yourself.")
                return
            
            # Check if already following
            cursor.execute('''
                SELECT 1 FROM follows 
                WHERE flwer = ? AND flwee = ?
            ''', (current_user_id, user_id))
            if cursor.fetchone():
                print("You are already following this user.")
                return

            start_date = datetime.now().strftime('%Y-%m-%d')
            cursor.execute("""
                INSERT INTO follows 
                (flwer, flwee, start_date) VALUES (?, ?, ?)
            """, (current_user_id, user_id, start_date)) 
            connection.commit()
            print("You are now following this user.")
            return

        elif choice == 'see more':  # This is how we see more tweets from the specified user
            new_offset = offset + 3
            show_user_info(connection, cursor, current_user_id, user_id, user_info, new_offset)
        else:
            print("Invalid input. Please try again.")
