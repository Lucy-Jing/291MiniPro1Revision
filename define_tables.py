# Darlene Nguyen
# Last Update: Nov 12, 2024
import sqlite3
import time
import datetime

connection = None
cursor = None


def connect(path):
    global connection, cursor
    
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return connection, cursor

def define_tables():
    global connection, cursor
    
    users_query = '''CREATE TABLE users (
    usr         int,
    name        text,
    email       text,
    phone       int,
    pwd         text,
    primary key (usr)
    )'''
    
    follows_query = '''CREATE TABLE follows (
    flwer       int,
    flwee       int,
    start_date  date,
    primary key (flwer,flwee),
    foreign key (flwer) references users(usr) ON DELETE CASCADE,
    foreign key (flwee) references users(usr) ON DELETE CASCADE)'''

    tweets_query = '''CREATE TABLE tweets (
    tid         int,
    writer_id   int,
    text        text,
    tdate       date, 
    ttime       time,
    replyto_tid int,
    PRIMARY KEY (tid),
    FOREIGN KEY (writer_id) REFERENCES users(usr) ON DELETE CASCADE,
    FOREIGN KEY (replyto_tid) REFERENCES tweets(tid) ON DELETE CASCADE)'''    
    
    lists_query = '''CREATE TABLE lists (
    owner_id    int,
    lname       text,
    PRIMARY KEY (owner_id, lname),
    FOREIGN KEY (owner_id) REFERENCES users(usr) ON DELETE CASCADE)'''    
    
    include_query = '''CREATE TABLE include (
    owner_id    int,
    lname       text,
    tid         int,
    PRIMARY KEY (owner_id, lname, tid),
    FOREIGN KEY (owner_id, lname) REFERENCES lists(owner_id, lname) ON DELETE CASCADE,
    FOREIGN KEY (tid) REFERENCES tweets(tid) ON DELETE CASCADE)'''
    
    retweets_query = '''CREATE TABLE retweets (
    tid         int,
    retweeter_id   int, 
    writer_id      int, 
    spam        int,
    rdate       date,
    PRIMARY KEY (tid, retweeter_id),
    FOREIGN KEY (tid) REFERENCES tweets(tid) ON DELETE CASCADE,
    FOREIGN KEY (retweeter_id) REFERENCES users(usr) ON DELETE CASCADE,
    FOREIGN KEY (writer_id) REFERENCES users(usr) ON DELETE CASCADE)'''
    
    hashtag_mentions_query = '''CREATE TABLE hashtag_mentions (
    tid         int,
    term        text,
    primary key (tid, term),
    FOREIGN KEY (tid) REFERENCES tweets(tid) ON DELETE CASCADE)'''
    
    cursor.execute(users_query)
    cursor.execute(follows_query)
    cursor.execute(tweets_query)
    cursor.execute(lists_query)
    cursor.execute(include_query)
    cursor.execute(retweets_query)
    cursor.execute(hashtag_mentions_query)
    connection.commit()
    
    return
