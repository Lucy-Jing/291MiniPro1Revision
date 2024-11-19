# Lucy 
# Last update: Nov 12, 2024
import sqlite3
import time
import datetime
from define_tables import connect
connection = None
cursor = None


def insert_data(connection, cursor):
    # global connection, cursor

    # Insert data into 'users' table starting from user ID 4
    insert_users = '''
        INSERT INTO users (usr, name, email, phone, pwd) VALUES
            (4, 'Alice', 'alice@example.com', 1234567890, 'password4'),
            (5, 'Bob', 'bob@example.com', 2345678901, 'password5'),
            (6, 'Stitch', 'X626Stitch@Disney.com', 8885188888, 'Hawaii'),
            (7, 'alice', 'ALICE@example.com', NULL, 'password7'),
            (8, 'Eve', 'eve@example.com', 5678901234, 'password8'),
            (9, 'Mallory', 'mallory@example.com', 6789012345, 'password9'),
            (10, 'Trent', 'trent@example.com', 7890123456, 'password10'),
            (11, 'Oscar', 'oscar@example.com', 8901234567, 'password11'),
            (12, 'Peggy', 'peggy@example.com', 9012345678, 'password12');
    '''

    # Insert data into 'tweets' table
    insert_tweets = '''
        INSERT INTO tweets (tid, writer_id, text, tdate, ttime, replyto_tid) VALUES
            (1, 4, 'Hello world!', '2023-10-01', '12:00:00', NULL),
            (2, 5, 'Good morning!', '2023-10-02', '08:30:00', NULL),
            (3, 4, 'Replying to tweet 2', '2023-10-02', '09:00:00', 2),
            (4, 7, 'Testing edge cases', '2023-10-03', NULL, NULL),
            (5, 8, 'Edge case tweet', '2023-10-04', '10:00:00', NULL),
            (6, 9, 'This is a very long tweet that exceeds the usual character limit to test how the system handles long texts.', '2023-10-05', '11:00:00', NULL),
            (7, 4, 'Another tweet from Alice', '2023-10-06', '12:00:00', NULL),
            (8, 9, 'Special characters !@#$%^&*() in tweet', '2023-10-07', '13:00:00', NULL),
            (9, 10, 'Tweet with #hashtag', '2023-10-08', '14:00:00', NULL),
            (10, 11, 'Tweet with duplicate hashtags #test #test', '2023-10-09', '15:00:00', NULL);
    '''

    # Insert data into 'follows' table
    insert_follows = '''
        INSERT INTO follows (flwer, flwee, start_date) VALUES
            (4, 5, '2023-09-01'),
            (5, 4, '2023-09-02'),
            (6, 4, '2023-09-03'),   -- Stitch follows Alice
            (4, 7, '2023-09-04'),
            (4, 4, '2023-09-05'),
            (8, 4, '2023-09-06'),
            (9, 4, '2023-09-07'),
            (10, 4, '2023-09-08'),
            (11, 4, '2023-09-09'),
            (12, 4, '2023-09-10');
    '''

    # Insert data into 'lists' table
    insert_lists = '''
        INSERT INTO lists (owner_id, lname) VALUES
            (4, 'Favorites'),
            (5, 'Interesting'),
            (7, 'Edge Cases');
    '''

    # Insert data into 'include' table
    insert_include = '''
        INSERT INTO include (owner_id, lname, tid) VALUES
            (4, 'Favorites', 2),
            (5, 'Interesting', 1),
            (7, 'Edge Cases', 4);
    '''

    # Insert data into 'retweets' table
    insert_retweets = '''
        INSERT INTO retweets (tid, retweeter_id, writer_id, spam, rdate) VALUES
            (1, 5, 4, 0, '2023-10-02'),
            (1, 6, 4, 0, '2023-10-03'),  -- Stitch retweets Alice's tweet
            (5, 8, 8, 1, '2023-10-04'),
            (6, 9, 9, 0, '2023-10-05');
    '''

    # Insert data into 'hashtag_mentions' table
    insert_hashtag_mentions = '''
        INSERT INTO hashtag_mentions (tid, term) VALUES
            (1, 'hello'),
            (2, 'morning'),
            (3, 'reply'),
            (8, 'special'),
            (9, 'hashtag'),
            (10, 'test'); 
    '''
    cursor.execute(insert_users)
    cursor.execute(insert_tweets)
    cursor.execute(insert_follows)
    cursor.execute(insert_lists)
    cursor.execute(insert_include)
    cursor.execute(insert_retweets)
    cursor.execute(insert_hashtag_mentions)
    connection.commit()

    return

if __name__ == "__main__":
    connection, cursor = connect("test.db")
    insert_data(connection, cursor)