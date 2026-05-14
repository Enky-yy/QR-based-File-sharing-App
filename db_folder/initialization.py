import sqlite3

database = 'db_folder/qrshare.db'

def init_db():
    print('initializing....')
    conn =sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS transfers (
                       id TEXT PRIMARY KEY,
                       filename TEXT,
                       original_filename TEXT,
                       ip TEXT,
                       device TEXT,
                       upload_time TEXT,
                       expiry REAL,
                       ocr_text TEXT
                        )
                    ''')
    
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT
                        )   
                    ''')
    
    conn.commit()
    conn.close()