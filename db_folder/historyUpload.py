import sqlite3
database = 'db_folder/qrshare.db'
import time

def upload(x,y,z,p):
    conn = sqlite3.connect(database)

    cursor = conn.cursor()

    cursor.execute('''

    INSERT INTO transfers (
        filename,
        ip,
        device,
        upload_time,
        expiry
    )

    VALUES (?, ?, ?, ?, ?)

    ''', (

        x,

        y,

        z,

        p,

        time.time() + 3600
    ))

    conn.commit()

    conn.close()