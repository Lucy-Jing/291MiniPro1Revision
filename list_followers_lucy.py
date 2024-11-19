# Lucy
# Last update: Nov 14, add comment.

import sqlite3
from datetime import datetime


def show_follower_details(cursor, follower_id, current_user_id):
    """
    Displays detailed information about a selected follower.
    """
    try:
        # Query for the number of tweets
        cursor.execute('''
            SELECT COUNT(*) FROM tweets WHERE writer_id = ?
        ''', (follower_id,))
        tweet_count = cursor.fetchone()[0]#Use fetchone to retrieve the actual count
    
        # Query for the number of retweets
        cursor.execute('''
            SELECT COUNT(*) FROM retweets WHERE retweeter_id = ?
        ''', (follower_id,))
        retweet_count = cursor.fetchone()[0]
    
        # Total number of tweets including retweets
        total_tweet_count = tweet_count + retweet_count
    
        # Query for the number of users the follower is following
        cursor.execute('''
            SELECT COUNT(*) FROM follows WHERE flwer = ?
        ''', (follower_id,))
        followee_count = cursor.fetchone()[0]
    
        # Query for the number of followers
        cursor.execute('''
            SELECT COUNT(*) FROM follows WHERE flwee = ?
        ''', (follower_id,))
        follower_count = cursor.fetchone()[0]
    
        # Display follower details
        print("\nFollower Details:")
        print(f"Number of tweets (including retweets): {total_tweet_count}")#This num includes retweets as stated in the carification.
        print(f"Number of users they follow: {followee_count}")
        print(f"Number of followers: {follower_count}")
    
        # Retrieve tweets and retweets
        tweets = []
    
        # Get tweets
        cursor.execute('''
            SELECT 'Tweet' AS type, tid, text, tdate, ttime
            FROM tweets
            WHERE writer_id = ?
        ''', (follower_id,))
        tweets.extend(cursor.fetchall())
    
        # Get retweets
        cursor.execute('''
            SELECT 'Retweet' AS type, t.tid, t.text, r.rdate, NULL
            FROM retweets r
            JOIN tweets t ON r.tid = t.tid
            WHERE r.retweeter_id = ?
        ''', (follower_id,))
        tweets.extend(cursor.fetchall())
    
        
        def parse_datetime(date_str, time_str):
            '''
            This function takes the date string and time string retrieved and convert it to datetime value in Python.
            '''
            if not date_str:
                raise ValueError("Date string is empty or None.")
            if not time_str:
                time_str = '00:00:00'
            datetime_str = f"{date_str} {time_str}"
            try:
                parsed_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
                '''
                The format refered to:
                date_str = '2023-02-28 14:30:00'
                date_format = '%Y-%m-%d %H:%M:%S'
                date_obj = datetime.strptime(date_str, date_format)
                '''
                return parsed_datetime
            except ValueError as e:
                print(f"Error parsing datetime string '{datetime_str}': {e}")
                # Handle or re-raise the exception as appropriate
                raise

    
        if tweets:
            tweets.sort(key=lambda x: parse_datetime(x[3], x[4]), reverse=True)

            #Displaying the tweets.
            index = 0
            total_tweets = len(tweets)
            while index < total_tweets:
                print("\nMost Recent Tweets and Retweets:")
                for i in range(index, min(index + 3, total_tweets)):
                    item = tweets[i]
                    tweet_type = item[0]
                    text = item[2]
                    date = item[3]
                    time = item[4] if item[4] else ''
                    print(f"{i + 1}. {tweet_type} - Date: {date}, Time: {time}, Text: {text}")
                index += 3

                if index < total_tweets:
                    see_more = input("Do you want to see more tweets? (yes/no): ").strip().lower()
                    while see_more not in ('yes', 'no'):
                        print("Invalid input. Please enter 'yes' or 'no'.")
                        see_more = input("Do you want to see more tweets? (yes/no): ").strip().lower()
                    if see_more != 'yes':
                        break
                else:
                    break
        else:
            print("This user has no tweets or retweets.")
    
        # Option to follow the user
        while True:
            choose_follow = input("\nDo you want to follow this user? (yes/no): ").strip().lower()
            if choose_follow == 'yes':
                follow_user(cursor, current_user_id, follower_id)
                break
            elif choose_follow == 'no':
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")



def follow_user(cursor, current_user_id, user_to_follow):
    """
    Allows the current user to follow another user.
    """
    try:
        if current_user_id == user_to_follow:
            print("You cannot follow yourself.")
            return

        # Check if already following
        cursor.execute('''
            SELECT 1 FROM follows WHERE flwer = ? AND flwee = ?
        ''', (current_user_id, user_to_follow))
        if cursor.fetchone():
            print("You are already following this user.")
            return

        # Insert into follows table
        start_date = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT INTO follows (flwer, flwee, start_date) VALUES (?, ?, ?)
        ''', (current_user_id, user_to_follow, start_date))
        cursor.connection.commit()
        print("You are now following this user.")
    except sqlite3.Error as e:
        print(f"An error occurred while following the user: {e}")



def list_followers(cursor, usr):
    """
    Lists all users who follow the logged-in user.
    Allows selection of a follower to see more details and interact.
    """
    try:
        # Query to get the list of followers for the logged-in user.
        cursor.execute('''
            SELECT u.usr, u.name
            FROM follows f
            JOIN users u ON f.flwer = u.usr
            WHERE f.flwee = ?
            ORDER BY u.name COLLATE NOCASE;
        ''', (usr,))
        list_followers_info = cursor.fetchall()#Has the form: [(usr,name),(),()...]

        #print out the message if the user has no follower.
        if not list_followers_info:
            print("You have no followers.")
            return

        # Display followers in groups of 5
        index = 0
        total_followers = len(list_followers_info)
        while index < total_followers:
            print("\nFollowers:")
            # Prints a page of 5 users.
            for i in range(index, min(index + 5, total_followers)):
                print(f"{i + 1}. User ID: {list_followers_info[i][0]}, Name: {list_followers_info[i][1]}")
            index += 5
            if index < total_followers:
                view_more = input("Do you want to see more followers? (yes/no): ").strip().lower()
                while view_more not in ('yes', 'no'):
                    print("Invalid input. Please enter 'yes' or 'no'.")
                    view_more = input("Do you want to see more followers? (yes/no): ").strip().lower()
                if view_more != 'yes':
                    break

        # Prompt to select a follower by name for more details
        while True:
            follower_name = input("\nEnter the name of a follower to see more details (or 'exit' to return): ").strip()
            if follower_name.lower() == 'exit':
                return
            elif follower_name:

                # Search for followers matching the entered name (case-insensitive). 
                # Besides, making the list of matching followers.
                matching_followers = []
                for follower_info in list_followers_info:
                    if follower_info[1] and follower_info[1].lower() == follower_name.lower():
                        matching_followers.append(follower_info)#[(uid,name),(),()...]

                if not matching_followers:
                    print("No follower found with that name. Please try again.")
                    continue  # Skip to the next loop. Ask again.

                # If there is only one matching follower.
                elif len(matching_followers) == 1:
                    show_follower_details(cursor, matching_followers[0][0], usr)
                    break

                else:
                    print("Multiple followers found with that name:")
                    # Displaying all the matching followers.
                    for i in range (0,len(matching_followers),1):
                        print(f"{i+1}. User ID: {matching_followers[i][0]}, Name: {matching_followers[i][1]}")
                    # Prompt user to select by User ID
                    while True:
                        selected_id_input = input("Please enter the User ID of the follower you wish to view (or 'exit' to cancel): ").strip()
                        if selected_id_input.lower() == 'exit':
                            return
                        elif selected_id_input.isdigit():
                            selected_id = int(selected_id_input)
                            # Check if the selected ID is in the matching followers
                            found = False
                            for y in range (0, len(matching_followers),1):
                                if matching_followers[y][0]==selected_id:
                                    found = True
                                    break
                            if found:
                                show_follower_details(cursor, selected_id, usr)
                                break
                            else:
                                print("Invalid User ID. No match is found.")
                        else:
                            print("Invalid User ID. Please enter one of the displayed User IDs.")
                    break
            else:
                print("Invalid input. Please enter a valid name or 'exit' to return.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
