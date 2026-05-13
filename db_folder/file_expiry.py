import sqlite3
import time
import os

database = 'db_folder/qrshare.db'

def cleanup_expired_files(shared_folder):

    conn = sqlite3.connect(database)

    cursor = conn.cursor()

    current_time = time.time()

    cursor.execute('''
        SELECT filename
        FROM transfers
        WHERE expiry < ?
    ''', (current_time,))

    expired_files = cursor.fetchall()

    for file_tuple in expired_files:

        filename = file_tuple[0]

        path = os.path.join(
            shared_folder,
            filename
        )

        if os.path.exists(path):
            os.remove(path)

    cursor.execute('''
        DELETE FROM transfers
        WHERE expiry < ?
    ''', (current_time,))

    conn.commit()

    conn.close()