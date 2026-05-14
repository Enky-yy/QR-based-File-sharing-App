import sqlite3
database = 'db_folder/qrshare.db'
import time

def upload(x,y,z,p,q,r,s):
    conn = sqlite3.connect(database)

    cursor = conn.cursor()

    cursor.execute('''

    INSERT INTO transfers (
        id,
        filename,
        original_filename,
        ip,
        device,
        upload_time,
        expiry,
        ocr_text
    )

    VALUES (?, ?, ?, ?, ?,?,?,?)

    ''', (
 
        x,

        y,

        z,

        p,

        q,

        r,

        time.time() + 3600,
        s
    ))

    conn.commit()

    conn.close()