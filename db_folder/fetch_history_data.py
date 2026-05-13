import sqlite3

database = 'db_folder/qrshare.db'

def history():

    conn = sqlite3.connect(database)

    cursor = conn.cursor()

    cursor.execute('''
        SELECT filename,
               ip,
               device,
               upload_time
        FROM transfers
        ORDER BY id DESC
    ''')

    history_data = cursor.fetchall()

    conn.close()

    return history_data