# Darlene Nguyen
# Last update: Nov 14, 2024

import sqlite3
import time
import datetime
import string

def connect(path):
    global connection, cursor
    
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

def define_tables():
    global connection, cursor
    
    users_query = '''CREATE TABLE users (
    usr INT,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15),
    pwd VARCHAR(100),
    PRIMARY KEY (usr))'''
    
    follows_query = '''CREATE TABLE follows (
    flwer INT,
    flwee INT,
    start_date DATE,
    PRIMARY KEY (flwer,flwee),
    FOREIGN KEY (flwer) REFERENCES users,
    FOREIGN KEY (flwee) REFERENCES users)'''

    tweets_query = '''CREATE TABLE tweets (
    tid INT,
    writer_id INT,
    text TEXT,
    tdate DATE,
    ttime TIME,
    replyto_tid INT,
    PRIMARY KEY (tid, writer_id, replyto_tid),
    FOREIGN KEY (writer_id) REFERENCES users
    FOREIGN KEY (replyto_tid) REFERENCES tweets)'''    
    
    lists_query = '''CREATE TABLE lists (
    owner_id INT,
    lname VARCHAR(100),
    PRIMARY KEY (owner_id),
    FOREIGN KEY (owner_id) REFERENCES users)'''    
    
    include_query = '''CREATE TABLE include (
    owner_id INT,
    lname VARCHAR(100),
    tid INT,
    PRIMARY KEY (owner_id, tid),
    FOREIGN KEY (owner_id) REFERENCES users
    FOREIGN KEY (tid) REFERENCES tweets)'''
    
    retweets_query = '''CREATE TABLE retweets (
    tid INT,
    retweeter_id INT,
    writer_id INT,
    spam INT,
    rdate DATE,
    PRIMARY KEY (tid, retweeter_id, writer_id),
    FOREIGN KEY (tid) REFERENCES tweets
    FOREIGN KEY (retweeter_id) REFERENCES users
    FOREIGN KEY (writer_id) REFERENCES users)'''
    
    hashtag_mentions_query = '''CREATE TABLE hashtag_mentions (
    tid INT,
    term TEXT,
    PRIMARY KEY (tid, term),
    FOREIGN KEY (tid) REFERENCES tweets)'''
    
    cursor.execute(users_query)
    cursor.execute(follows_query)
    cursor.execute(tweets_query)
    cursor.execute(lists_query)
    cursor.execute(include_query)
    cursor.execute(retweets_query)
    cursor.execute(hashtag_mentions_query)
    connection.commit()
    
    return

def compose_tweet(connection, cursor, user_id, replyto_tid = None):
    '''
    Compose an original tweet or a reply to a tweet
    
    Constraints: One tweet can have multiple hashtags but not multiple instances of the same hashtag.id
                 Info about hashtags must be stored in table hashtag_mentions.
    
    Parameter: replyto_tid (default = None)
    
    Return: True
    '''
    # global connection, cursor, user_id
    # Receive Input 
    print("=" * 50)
    print("What's happening? What's on your mind?".center(50))
    print("=" * 50)
    text = input()
    
    # Record Tweet's ID
    cursor.execute('''SELECT MAX(recent.tid) FROM tweets recent''')
    recent = cursor.fetchone()
    if len(recent) != 0:
        tid = recent[0] + 1 # Incrementing ID for each new tweet
    else:
        tid = 101 # First ever tweet is created if there are none tweets created before  
    
    # Record Date & Time
    tdate = datetime.datetime.now().strftime("%Y-%m-%d")
    ttime = datetime.datetime.now().strftime("%H:%M:%S")
    
    # INVALID TWEET w/ same multiple #hashtag
    words = text.split()
    terms = [] # all #terms reasonate w/ current tid
    for word in words:
        # remove punctuations first
        word = word.rstrip(string.punctuation)
        if word.startswith('#'):
            terms.append(word)
    # check for duplicate terms
    if len(terms) != len(set(terms)):
        print("=" * 50)
        print("Invalid Tweet!".center(50))
        print("Error: multiple instances of the same hashtag.".center(50))
        print("Please try again :)".center(50))
        print("=" * 50)
        return
    
    # Insert Values to Table tweets
    # tweets(tid, writer_id, text, tdate, ttime, replyto_tid)
    cursor.execute('''INSERT INTO tweets VALUES (?, ?, ?, ?, ?, ?);
                   ''', (tid, user_id, text, tdate, ttime, replyto_tid))
    connection.commit()    

    # Check & Store Hashtage to Table hashtag_mentions
    # hashtag_mentions(tid,term)
    for term in terms:
        if len(term) > 1: # '#' is not a hashtag
            cursor.execute('''INSERT INTO hashtag_mentions VALUES (?,?);''', (tid, term)) # handle case-sensitive
            connection.commit()

    # If successfully posted!
    print("=" * 50)
    print("Tweet Id:" + str(tid))
    print("Your tweet has been posted.".center(50))
    print("=" * 50)
    print()
    
    return True

def compose_retweet(connection, cursor, user_id, tid):
    '''
    Compose a retweet of an original tweet
    
    Constraints: There must be an original tweet to be retweeted
    
    Parameter: tid (tweet ID of the original tweet)
    
    Return: True
    '''
    # global connection, cursor, user_id
    # Receive Input
    print("=" * 50)
    print("Do you want to share this tweet? Y/N".center(50))
    print("=" * 50)
    text = input() 
    # handle case-sensitive
    if text.upper() == 'N':
        print("=" * 50)
        print("This retweet has been cancelled.".center(50))
        print("=" * 50)
        return
    
    # Get the writer_id
    cursor.execute('''SELECT writer_id FROM tweets WHERE tid = ?''', (tid, ))
    writer_id = cursor.fetchone()[0]
    
    # Record Date & Time
    rdate = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Check if a spam
    cursor.execute('''SELECT COUNT(*) FROM retweets 
    WHERE tid = ? AND retweeter_id = ?''', (tid, user_id))
    occur = cursor.fetchone()[0]
    if occur == 1:      
        spam = 1 # Update flag if it's a spam
        cursor.execute('''UPDATE retweets SET spam = ? 
        WHERE tid = ? AND retweeter_id = ?''', (spam, tid, user_id))
        connection.commit()
    else:
        spam = 0
        # Insert Values to Table tweets
        # retweets(tid, retweeter_id, writer_id, spam, rdate)
        cursor.execute('''INSERT INTO retweets VALUES (?, ?, ?, ?, ?);
                       ''', (tid, user_id, writer_id, spam, rdate))
        connection.commit() 
                
    # If successfully posted!
    print("=" * 50)
    print("Retweets id: " + str(tid))
    print("Your retweet has been posted.".center(50))
    print("=" * 50)
    print()
    
    return True

def print_all_data():
    global cursor
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
