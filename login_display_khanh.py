import sqlite3
def login_display(conn, cursor,curr_user,remain=0):
    query = """
        SELECT *
        FROM (
            SELECT 
                t.tid,
                t.writer_id,
                t.text,
                t.tdate,
                t.ttime,
                t.replyto_tid,
                NULL AS retweeter_id,
                NULL AS spam,
                t.tdate || ' ' || t.ttime AS full_datetime
            FROM tweets t
            JOIN follows f ON f.flwee = t.writer_id
            WHERE f.flwer = ?
            
            UNION ALL
            
            SELECT 
                r.tid,
                r.writer_id,
                NULL AS text,
                r.rdate AS tdate,
                NULL AS ttime,
                NULL AS replyto_tid,
                r.retweeter_id,
                r.spam,
                r.rdate AS full_datetime
            FROM retweets r
            JOIN follows f ON f.flwee =  r.retweeter_id
            WHERE f.flwer = ?
        )
        ORDER BY full_datetime DESC
        
"""
    cursor.execute(query, (curr_user, curr_user))
    output = cursor.fetchall()

    # Calculate the start and end indices for the current batch
    start_index = remain * 5
    end_index = start_index + 5

    for i, tweet in enumerate(output[start_index:end_index]):
        tid = tweet[0]
        writer_id = tweet[1]
        text = tweet[2] if tweet[2] else "No text available"
        tdate = tweet[3]
        ttime = tweet[4]
        print(f"{i + 1:2}. Tweet ID: {tid}, Author ID: {writer_id}, Date: {tdate}, Time: {ttime}, Text: {text.strip() if text else 'No text'}")

    return output[start_index:end_index]

if __name__ == "__main__":
    conn = sqlite3.connect('test.db')

# Create a cursor object
    cursor = conn.cursor()
    # First 5
    print("First 5 tweets:")
    print(login_display(conn, cursor, "4", 0))

    # Next 5
    print("\nNext 5 tweets:")
    print(login_display(conn, cursor, "4", 1))

    # Next Next 5
    print("\nNext next 5 tweets:")
    login_display(conn, cursor, "4", 2)


