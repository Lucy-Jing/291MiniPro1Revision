import sqlite3
from sqlalchemy import create_engine, MetaData
from sqlalchemy_schemadisplay import create_schema_graph
# Connect to the SQLite database (make sure the path is correct)
conn = sqlite3.connect('test.db')

# Create a cursor object
cursor = conn.cursor()



# def query(query:str):
#     cursor.execute(query)
#     conn.commit()
#     print(cursor.fetchall())

def query(query_string: str):
    # Split the query by semicolons and remove any empty strings after splitting
    queries = [q.strip() for q in query_string.split(';') if q.strip()]
    for q in queries:
        cursor.execute(q)
    conn.commit()
    print("Queries executed successfully.")
    print(cursor.fetchall())


def show_table():
    engine = create_engine('sqlite:///test.db')

    metadata = MetaData()
    metadata.reflect(bind=engine)

    graph = create_schema_graph(metadata=metadata, show_datatypes=True, rankdir='LR', engine=engine)
    graph.write(path="p2_schema.dot" , prog=None, format="raw", encoding=None) 
    with open('p2_schema.dot', 'w') as f:
        f.write(graph.to_string())

    graph.write_png('p2_schema.png')
def get_table():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        table_name = table[0]
        print(f"\nSchema for table: {table_name}")
        
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        print(f"{'Column Name':<20}{'Data Type':<15}{'Nullable':<10}{'Primary Key'}")
        for column in columns:
            col_name = column[1]
            col_type = column[2]
            col_nullable = 'Yes' if column[3] == 0 else 'No'
            col_primary_key = 'Yes' if column[5] == 1 else 'No'
            
            print(f"{col_name:<20}{col_type:<15}{col_nullable:<10}{col_primary_key}")

    conn.close()

if __name__ == "__main__":
    query('''
                SELECT t.tid, t.writer_id, t.text, t.tdate, t.ttime,
                       CASE WHEN r.tid IS NOT NULL THEN 'Retweet' ELSE 'Tweet' END AS tweet_type
                FROM tweets t
                LEFT JOIN retweets r ON t.tid = r.tid
                JOIN hashtag_mentions hm ON t.tid = hm.tid
                WHERE LOWER(hm.term) LIKE LOWER('#som')
                ORDER BY t.tdate DESC, t.ttime DESC
          ''')
    # show_table()
    # get_table()
# tweets 
# JOIN hashtag_mentions ON tweets.tid = hashtag_mentions.tid 
# WHERE LOWER(term) = LOWER('#NatureW');
