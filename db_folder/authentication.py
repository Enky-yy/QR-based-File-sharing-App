import sqlite3

database = "db_folder/qrshare.db"

def signup(username , hash_password):

    conn = sqlite3.connect(database)

    cursor = conn.cursor()

    cursor.execute('''
                    INSERT INTO users(
                        username,
                        password
                        )
                        VALUES(?,?)
                    ''',(
                        username, hash_password
                    ))
    
    conn.commit()
    conn.close()


def login(username):
    conn = sqlite3.connect(database)

    cursor = conn.cursor()

    cursor.execute('''
                    SELECT id, password FROM users WHERE username=?
                    ''',(
                        username,
                    ))
    
    user =cursor.fetchone()

    conn.close()

    return user