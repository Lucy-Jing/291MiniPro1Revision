import sqlite3
from define_tables import connect

def insert_additional_data(connection, cursor):
    # Starting IDs based on the last IDs used in your current data
    # Assuming the last usr ID is 12 and the last tid is 113
    # Adjust these numbers if necessary to avoid conflicts

    # Insert data into 'users' table
    insert_users = '''
        INSERT INTO users (usr, name, email, phone, pwd) VALUES
            (13, 'Aha', 'aha@example.com', 1234886668, 'IwantToFly'),
            (14, 'Ben', 'ben@example.com', 1234886669, 'password14'),
            (15, 'Cara', 'cara@example.com', 1234886670, 'password15'),
            (16, 'Dan', 'dan@example.com', 1234886671, 'password16'),
            (17, 'Eve', 'eve3@example.com', 1234886672, 'password17'),
            (18, 'Frank', 'frank2@example.com', 1234886673, 'password18'),
            (19, 'Grace', 'grace2@example.com', 1234886674, 'password19'),
            (20, 'Heidi', 'heidi2@example.com', 1234886675, 'password20'),
            (21, 'Ivan', 'ivan2@example.com', 1234886676, 'password21'),
            (22, 'Judy', 'judy2@example.com', 1234886677, 'password22'),
            (23, 'Mallory', 'mallory3@example.com', 1234886678, 'password23'),
            (24, 'Niaj', 'niaj2@example.com', 1234886679, 'password24'),
            (25, 'Olivia', 'olivia2@example.com', 1234886680, 'password25'),
            (26, 'Peggy', 'peggy3@example.com', 1234886681, 'password26'),
            (27, 'Sybil', 'sybil2@example.com', 1234886682, 'password27'),
            (28, 'Trent', 'trent3@example.com', 1234886683, 'password28'),
            (29, 'Victor', 'victor2@example.com', 1234886684, 'password29'),
            (30, 'Walter', 'walter2@example.com', 1234886685, 'password30'),
            (31, 'Alice', 'alice4@example.com', 1234886686, 'password31'),  -- Duplicate name 'Alice'
            (32, 'Bob', 'bob4@example.com', 1234886687, 'password32'),      -- Duplicate name 'Bob'
            (33, 'Yvonne', 'yvonne2@example.com', 1234886688, 'password33'),
            (34, 'Zara', 'zara2@example.com', 1234886689, 'password34'),
            (35, 'Oscar', 'oscar3@example.com', 1234886690, 'password35'),
            (36, 'Uma', 'uma2@example.com', 1234886691, 'password36'),
            (37, 'Quentin', 'quentin2@example.com', 1234886692, 'password37'),
            (38, 'Rachel', 'rachel2@example.com', 1234886693, 'password38'),
            (39, 'Steve', 'steve2@example.com', 1234886694, 'password39'),
            (40, 'Tom', 'tom@example.com', 1234886695, 'password40'),
            (41, 'Uma', 'uma3@example.com', 1234886696, 'password41'),      -- Duplicate name 'Uma'
            (42, 'Victor', 'victor3@example.com', 1234886697, 'password42'); -- Duplicate name 'Victor'
    '''

    # Adjusted tweet IDs starting from 114
    insert_tweets = '''
        INSERT INTO tweets (tid, writer_id, text, tdate, ttime, replyto_tid) VALUES
            (114, 13, 'Starting my journey at the university! #university #education', '2023-10-20', '08:00:00', NULL),
            (115, 14, 'Excited for the semester #university', '2023-10-20', '09:00:00', NULL),
            (116, 15, 'First lecture today #learning #university', '2023-10-20', '10:00:00', NULL),
            (117, 16, 'Meeting new people #friends', '2023-10-20', '11:00:00', NULL),
            (118, 17, 'Campus tour was fun #university #campus', '2023-10-21', '12:00:00', NULL),
            (119, 18, 'Library is impressive #study #education', '2023-10-21', '13:00:00', NULL),
            (120, 19, 'Joined a club #studentlife #university', '2023-10-21', '14:00:00', NULL),
            (121, 20, 'Group project assigned #teamwork #learning', '2023-10-21', '15:00:00', NULL),
            (122, 21, 'Coffee break #student', '2023-10-22', '10:30:00', NULL),
            (123, 22, 'Late night studying #exams #study', '2023-10-22', '22:00:00', NULL),
            (124, 23, 'Weekend getaway #relax', '2023-10-23', '16:00:00', NULL),
            (125, 24, 'Back to lectures #university', '2023-10-24', '09:00:00', NULL),
            (126, 25, 'Preparing for midterms #study', '2023-10-24', '17:00:00', NULL),
            (127, 26, 'Learning new programming languages #coding #education', '2023-10-25', '11:00:00', NULL),
            (128, 27, 'Attending workshops #learning', '2023-10-25', '14:00:00', NULL),
            (129, 28, 'Sports day was exciting #fun #university', '2023-10-26', '13:00:00', NULL),
            (130, 29, 'Group discussions are helpful #education', '2023-10-26', '15:00:00', NULL),
            (131, 30, 'Looking forward to holidays #excited', '2023-10-27', '16:00:00', NULL),
            (132, 31, 'Participated in a hackathon #university #coding', '2023-10-27', '18:00:00', NULL),
            (133, 32, 'Volunteering at campus events #community #studentlife', '2023-10-28', '12:00:00', NULL),
            (134, 33, 'Exploring new subjects #learning #university', '2023-10-28', '14:00:00', NULL),
            (135, 34, 'Graduation day! #achievement', '2023-10-29', '10:00:00', NULL),
            (136, 35, 'Farewell friends #memories #university', '2023-10-29', '11:00:00', NULL),
            (137, 36, 'Starting a new job #future #career', '2023-10-30', '09:00:00', NULL),
            (138, 37, 'Travel plans ahead #adventure', '2023-10-30', '15:00:00', NULL),
            (139, 38, 'Reflecting on university life #nostalgia #university', '2023-10-31', '17:00:00', NULL),
            (140, 39, 'Thankful for the experiences #gratitude', '2023-10-31', '19:00:00', NULL),
            (141, 40, 'Continuous learning #growth #education', '2023-11-01', '08:00:00', NULL),
            (142, 41, 'Hello world! #coding #programming', '2023-11-01', '09:00:00', NULL),
            (143, 42, 'Networking is key #career #future', '2023-11-01', '10:00:00', NULL);
    '''

    # Insert data into 'follows' table remains unchanged
    insert_follows = '''
        INSERT INTO follows (flwer, flwee, start_date) VALUES
            (13, 4, '2023-10-20'),
            (14, 5, '2023-10-20'),
            (15, 6, '2023-10-20'),
            (16, 7, '2023-10-20'),
            (17, 4, '2023-10-21'),
            (18, 5, '2023-10-21'),
            (19, 6, '2023-10-21'),
            (20, 7, '2023-10-21'),
            (21, 4, '2023-10-22'),
            (22, 5, '2023-10-22'),
            (23, 6, '2023-10-23'),
            (24, 7, '2023-10-24'),
            (25, 4, '2023-10-24'),
            (26, 5, '2023-10-25'),
            (27, 6, '2023-10-25'),
            (28, 7, '2023-10-26'),
            (29, 4, '2023-10-26'),
            (30, 5, '2023-10-27'),
            (31, 6, '2023-10-27'),
            (32, 7, '2023-10-28'),
            (33, 4, '2023-10-28'),
            (34, 5, '2023-10-29'),
            (35, 6, '2023-10-29'),
            (36, 7, '2023-10-30'),
            (37, 4, '2023-10-30'),
            (38, 5, '2023-10-31'),
            (39, 6, '2023-10-31'),
            (40, 7, '2023-11-01'),
            (41, 4, '2023-11-01'),
            (42, 5, '2023-11-01');
    '''

    # Update 'include' table with new tweet IDs
    insert_include = '''
        INSERT INTO include (owner_id, lname, tid) VALUES
            (13, 'Aha\'s List', 114),
            (14, 'Ben\'s List', 115),
            (15, 'Cara\'s List', 116),
            (16, 'Dan\'s List', 117),
            (17, 'Eve\'s List', 118),
            (18, 'Frank\'s List', 119),
            (19, 'Grace\'s List', 120),
            (20, 'Heidi\'s List', 121),
            (21, 'Ivan\'s List', 122),
            (22, 'Judy\'s List', 123),
            (23, 'Mallory\'s List', 124),
            (24, 'Niaj\'s List', 125),
            (25, 'Olivia\'s List', 126),
            (26, 'Peggy\'s List', 127),
            (27, 'Sybil\'s List', 128),
            (28, 'Trent\'s List', 129),
            (29, 'Victor\'s List', 130),
            (30, 'Walter\'s List', 131),
            (31, 'Alice\'s New List', 132),
            (32, 'Bob\'s New List', 133),
            (33, 'Yvonne\'s List', 134),
            (34, 'Zara\'s List', 135),
            (35, 'Oscar\'s List', 136),
            (36, 'Uma\'s List', 137),
            (37, 'Quentin\'s List', 138),
            (38, 'Rachel\'s List', 139),
            (39, 'Steve\'s List', 140),
            (40, 'Tom\'s List', 141),
            (41, 'Uma\'s Second List', 142),
            (42, 'Victor\'s Second List', 143);
    '''

    # Update 'retweets' table with new tweet IDs
    insert_retweets = '''
        INSERT INTO retweets (tid, retweeter_id, writer_id, spam, rdate) VALUES
            (114, 14, 13, 0, '2023-10-20'),
            (115, 15, 14, 0, '2023-10-20'),
            (116, 16, 15, 0, '2023-10-20'),
            (117, 17, 16, 0, '2023-10-20'),
            (118, 18, 17, 0, '2023-10-21'),
            (119, 19, 18, 0, '2023-10-21'),
            (120, 20, 19, 0, '2023-10-21'),
            (121, 21, 20, 0, '2023-10-21'),
            (122, 22, 21, 0, '2023-10-22'),
            (123, 23, 22, 0, '2023-10-22'),
            (124, 24, 23, 0, '2023-10-23'),
            (125, 25, 24, 0, '2023-10-24'),
            (126, 26, 25, 0, '2023-10-24'),
            (127, 27, 26, 0, '2023-10-25'),
            (128, 28, 27, 0, '2023-10-25'),
            (129, 29, 28, 0, '2023-10-26'),
            (130, 30, 29, 0, '2023-10-26'),
            (131, 31, 30, 0, '2023-10-27'),
            (132, 32, 31, 0, '2023-10-27'),
            (133, 33, 32, 0, '2023-10-28'),
            (134, 34, 33, 0, '2023-10-28'),
            (135, 35, 34, 0, '2023-10-29'),
            (136, 36, 35, 0, '2023-10-29'),
            (137, 37, 36, 0, '2023-10-30'),
            (138, 38, 37, 0, '2023-10-30'),
            (139, 39, 38, 0, '2023-10-31'),
            (140, 40, 39, 0, '2023-10-31'),
            (141, 41, 40, 0, '2023-11-01'),
            (142, 42, 41, 0, '2023-11-01'),
            (143, 13, 42, 0, '2023-11-01');
    '''

    # Update 'hashtag_mentions' table with new tweet IDs
    insert_hashtag_mentions = '''
        INSERT INTO hashtag_mentions (tid, term) VALUES
            (114, '#university'),
            (114, '#education'),
            (115, '#university'),
            (116, '#learning'),
            (116, '#university'),
            (117, '#friends'),
            (118, '#university'),
            (118, '#campus'),
            (119, '#study'),
            (119, '#education'),
            (120, '#studentlife'),
            (120, '#university'),
            (121, '#teamwork'),
            (121, '#learning'),
            (122, '#student'),
            (123, '#exams'),
            (123, '#study'),
            (124, '#relax'),
            (125, '#university'),
            (126, '#study'),
            (127, '#coding'),
            (127, '#education'),
            (128, '#learning'),
            (129, '#fun'),
            (129, '#university'),
            (130, '#education'),
            (131, '#excited'),
            (132, '#university'),
            (132, '#coding'),
            (133, '#community'),
            (133, '#studentlife'),
            (134, '#learning'),
            (134, '#university'),
            (135, '#achievement'),
            (136, '#memories'),
            (136, '#university'),
            (137, '#future'),
            (137, '#career'),
            (138, '#adventure'),
            (139, '#nostalgia'),
            (139, '#university'),
            (140, '#gratitude'),
            (141, '#growth'),
            (141, '#education'),
            (142, '#coding'),
            (142, '#programming'),
            (143, '#career'),
            (143, '#future');
    '''

    # Insert data into 'lists' table remains unchanged
    insert_lists = '''
        INSERT INTO lists (owner_id, lname) VALUES
            (13, 'Aha\'s List'),
            (14, 'Ben\'s List'),
            (15, 'Cara\'s List'),
            (16, 'Dan\'s List'),
            (17, 'Eve\'s List'),
            (18, 'Frank\'s List'),
            (19, 'Grace\'s List'),
            (20, 'Heidi\'s List'),
            (21, 'Ivan\'s List'),
            (22, 'Judy\'s List'),
            (23, 'Mallory\'s List'),
            (24, 'Niaj\'s List'),
            (25, 'Olivia\'s List'),
            (26, 'Peggy\'s List'),
            (27, 'Sybil\'s List'),
            (28, 'Trent\'s List'),
            (29, 'Victor\'s List'),
            (30, 'Walter\'s List'),
            (31, 'Alice\'s New List'),
            (32, 'Bob\'s New List'),
            (33, 'Yvonne\'s List'),
            (34, 'Zara\'s List'),
            (35, 'Oscar\'s List'),
            (36, 'Uma\'s List'),
            (37, 'Quentin\'s List'),
            (38, 'Rachel\'s List'),
            (39, 'Steve\'s List'),
            (40, 'Tom\'s List'),
            (41, 'Uma\'s Second List'),
            (42, 'Victor\'s Second List');
    '''

    # Execute the insert statements
    try:
        cursor.executescript(insert_users)
        cursor.executescript(insert_tweets)
        cursor.executescript(insert_follows)
        cursor.executescript(insert_lists)
        cursor.executescript(insert_include)
        cursor.executescript(insert_retweets)
        cursor.executescript(insert_hashtag_mentions)
        connection.commit()
        print("Inserted 30 new users and associated data into the database.")
    except sqlite3.IntegrityError as e:
        print(f"IntegrityError occurred while inserting data: {e}")
    except sqlite3.Error as e:
        print(f"An error occurred while inserting data: {e}")

if __name__ == "__main__":
    connection, cursor = connect("test.db")
    insert_additional_data(connection, cursor)
    cursor.close()
    connection.close()
