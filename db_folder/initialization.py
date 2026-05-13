import sqlite3

database = 'db_folder/qrshare.db'

def init_db():
    print('initializing....')
    conn =sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS transfers (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       filename TEXT,
                       ip TEXT,
                       device TEXT,
                       upload_time TEXT,
                       expiry REAL
                        )
                    ''')
    
    conn.commit()
    conn.close()