# Khanh Bui
# Last update: Nov 11, 2024

import sqlite3
from compose_tweets_darlene import compose_retweet, compose_tweet

is_show_more = 0

def connect(path):
    global connection, cursor
    
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    connection.commit()
    return connection, cursor

def search_tweets(connection, cursor, current_user):
    keywords = input("search: ")
    keyword_list = keywords.split()
    results = []
    global is_show_more
    for keyword in keyword_list:
        if keyword.startswith("#"):
            query = '''
                SELECT t.tid, t.writer_id, t.text, t.tdate, t.ttime,
                       CASE WHEN r.tid IS NOT NULL THEN 'Retweet' ELSE 'Tweet' END AS tweet_type
                FROM tweets t
                LEFT JOIN retweets r ON t.tid = r.tid
                JOIN hashtag_mentions hm ON t.tid = hm.tid
                WHERE LOWER(hm.term) LIKE LOWER(?)
                ORDER BY t.tdate DESC, t.ttime DESC
            '''
            cursor.execute(query, (keyword.lower() + '%',))
            results.extend(cursor.fetchall())
        else:
            query = '''
                SELECT t.tid, t.writer_id, t.text, t.tdate, t.ttime,
                       CASE WHEN r.tid IS NOT NULL THEN 'Retweet' ELSE 'Tweet' END AS tweet_type
                FROM tweets t
                LEFT JOIN retweets r ON t.tid = r.tid
                WHERE t.text LIKE ?
                ORDER BY t.tdate DESC, t.ttime DESC
            '''
            cursor.execute(query, (f'%{keyword}%',))
            results.extend(cursor.fetchall())
    
    # Remove duplicates and sort by date (latest first)
    unique_results = sorted(set(results), key=lambda x: (x[3], x[4]), reverse=True)
    display_tweets(unique_results,is_show_more)
    # Display first 5 results and prompt for more if necessary
    while True:
        print("==================================================")
        print("Sub-section in search results, Select your option ")
        user_input = input("(rt: retweet, sm: show more tweets, prv: previous tweets r: reply, exit: exit sub-section, see stat: see tweet stat): ")
        print("==================================================")
        if user_input.lower() == 'sm':
            is_show_more+=1
            if display_tweets(unique_results,is_show_more) ==[]:
                print("No more tweets to display, revert to previous page")
                print("==================================================")
                is_show_more-=1
                display_tweets(unique_results,is_show_more)

        if user_input.lower() == 'prv':
            if is_show_more >=0:
                is_show_more-=1
                display_tweets(unique_results,is_show_more)
            else:
                print("cant go back with the tweets further more")
                print("==================================================")
                display_tweets(unique_results,is_show_more)          

        if user_input.lower() == 'rt':
            # will not check this yet
            tid = input("Tweet Id to retweet?: ")
            compose_retweet(connection, cursor, current_user, tid)
        elif user_input.lower() == 'r':
            replyto_tid = input("Tweet Id to reply?: ")
            compose_tweet(connection, cursor, current_user, replyto_tid)
        elif user_input.lower() == 'exit':
            return
        elif user_input.lower() == 'see stat':
            tweet_id = input("Tweet Id to see stat?: ") 
            display_tweet_statistics(connection, cursor, tweet_id, current_user)


def display_tweets(tweet_list,is_show_more):
    start_index = is_show_more * 5
    end_index = start_index + 5    
    if start_index >= len(tweet_list):
        return []  
        
    # Display tweets in the current batch (from start_index to end_index)
    for i, tweet in enumerate(tweet_list[start_index:end_index], start=start_index + 1):
        tweet_type = 'Retweet' if tweet[5].lower() == 'retweet' else 'Tweet'  
        print(f"{i}. [{tweet_type}] Tweet ID: {tweet[0]}, Author ID: {tweet[1]}, Date: {tweet[3]}, Time: {tweet[4]}")
        print(f" Text:  {tweet[2]}")

    # Return the current batch of tweets for verification purposes
    return tweet_list[start_index:end_index]

def display_tweet_statistics(connection, cursor, tweet_id, current_user):
    # Query for retweet and reply statistics
    query = '''
        SELECT 
            t.tid AS tweet_id,
            t.writer_id AS tweet_writer_id,
            t.text AS tweet_text,
            t.tdate AS tweet_date,
            t.ttime AS tweet_time,
            (SELECT COUNT(*) FROM retweets r WHERE r.tid = t.tid) AS retweet_count,
            (SELECT COUNT(*) FROM tweets t2 WHERE t2.replyto_tid = t.tid) AS reply_count
        FROM 
            tweets t
        WHERE 
            t.tid = ?
    '''
    cursor.execute(query, (tweet_id,))
    stats = cursor.fetchone()

    if stats:
        print(f"\nTweet ID: {stats[0]} Statistics:")
        print(f"   Writer ID: {stats[1]}")
        print(f"   Text: {stats[2]}")
        print(f"   Date: {stats[3]}")
        print(f"   Time: {stats[4]}")
        print(f"   Number of retweets: {stats[5]}")
        print(f"   Number of replies: {stats[6]}")
    else:
        print(f"No data found for Tweet ID: {tweet_id}")
    
    # Option to reply or retweet
    action = input("\nWould you like to (R)eply or (RT) retweet this tweet? (or press Enter to skip): ").lower()
    if action == 'r':
        compose_tweet(connection, cursor, current_user, tweet_id)
    elif action == 'rt':
        compose_retweet(connection, cursor, current_user, tweet_id)


if __name__=='__main__':
    connection, cursor = connect('test.db')

    search_tweets(connection, cursor, "4")  
    cursor.close()
    connection.close()
