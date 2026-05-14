import sqlite3

database = 'db_folder/qrshare.db'

def ocr_search(query):

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute('''
                    SELECT DISTINCT original_filename
                    FROM transfers
                    WHERE LOWER(ocr_text) like LOWER(?)
                    ''',(f'%{query}%',))
    
    results =cursor.fetchall()

    conn.close()

    return results