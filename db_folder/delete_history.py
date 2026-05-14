import sqlite3

database = 'db_folder/qrshare.db'

def select_data(id):
    conn = sqlite3.connect(database)

    cursor = conn.cursor()

    cursor.execute('''

        SELECT filename

        FROM transfers

        WHERE id = ?

    ''', (

        id,

    ))

    result = cursor.fetchone()

    conn.close()
    return result

def delete_history(id):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('''
                    DELETE FROM transfers
                    WHERE id =?
                    ''',(id,))
    
    conn.commit()
    conn.close()