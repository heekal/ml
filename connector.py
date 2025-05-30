import sqlite3
import numpy as np

file = r'local.db'

def init_db():
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            tipe TEXT,
            waktu INTEGER,
            nominal INTEGER,
            saldo INTEGER
        )
    ''')
    
    cursor.execute('SELECT COUNT(*) FROM user')
    
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO user (tipe, waktu, nominal, saldo) VALUES (?,?,?,?)', ('MASUK', 1747253244, 50000, 50000))
        
    conn.commit()
    cursor.close()
    conn.close()

def get_balance():
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    
    cursor.execute('SELECT saldo FROM user ORDER BY id DESC LIMIT 1')
    data = cursor.fetchone()[0]
    
    conn.close()
    return data or 0

def get_data():
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM user')
    data = cursor.fetchall()
    cursor.close()
    
    return data

def get_avg(batas):
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    
    cursor.execute('SELECT AVG(nominal) FROM user WHERE waktu < (?)', batas)
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return data

def get_std(batas):
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    
    cursor.execute('SELECT AVG(nominal) FROM user WHERE waktu < (?)', batas)
    avg = cursor.fetchone()[0]
    cursor.execute('SELECT nominal FROM user WHERE waktu < (?)', batas)
    values = [row[0] for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    n = len(values)
    std = np.sqrt(sum((x - avg) ** 2 for x in values) / n)
    
    return std

def get_zscore(batas):
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    
    # Get the last transaction's nominal and type
    cursor.execute('SELECT nominal, tipe FROM user ORDER BY id DESC LIMIT 1')
    last_trans_result = cursor.fetchone()
    
    if not last_trans_result:
        cursor.close()
        conn.close()
        return 0
    
    last_nominal, last_type = last_trans_result
    # Adjust the last nominal based on transaction type
    adjusted_last = last_nominal if last_type == 'MASUK' else -last_nominal
    
    # Get all transactions before 'batas' with their nominal and type
    cursor.execute('SELECT nominal, tipe FROM user WHERE waktu < ?', (batas,))
    rows = cursor.fetchall()
    
    if not rows:
        cursor.close()
        conn.close()
        return 0
    
    # Adjust nominals based on transaction type
    adjusted_values = []
    for nominal, tipe in rows:
        adjusted = nominal if tipe == 'MASUK' else -nominal
        adjusted_values.append(adjusted)
    
    # Calculate average and standard deviation of adjusted values
    avg = np.mean(adjusted_values)
    std = np.std(adjusted_values)  # Uses population std (ddof=0)
    
    if std == 0:
        cursor.close()
        conn.close()
        return 0
    
    zscore = (adjusted_last - avg) / std
    
    cursor.close()
    conn.close()
    
    return zscore

def get_last(tipe):
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    
    cursor.execute('SELECT (?) FROM user ORDER BY id DESC LIMIT 1')
    data = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    return data

def get_last_trans():
    """Get the last transaction type from the database"""
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    
    cursor.execute('SELECT waktu FROM user ORDER BY id DESC LIMIT 1')
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return result[0] if result else None

def get_last_nominal():
    """Get the last transaction nominal amount from the database"""
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    
    cursor.execute('SELECT nominal FROM user ORDER BY id DESC LIMIT 1')
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return result[0] if result else 0

def insert_data(tipe, waktu, nominal):
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    
    cursor.execute('SELECT saldo FROM user ORDER BY id DESC LIMIT 1')
        
    last_saldo = cursor.fetchone()
    last_saldo = last_saldo[0] if last_saldo else 0
    
    if tipe == 'TABUNGAN':
        saldo = last_saldo - nominal
    elif tipe == 'MASUK':
        saldo = last_saldo + nominal
    else:
        saldo = last_saldo
    
    cursor.execute('INSERT INTO user (tipe, waktu, nominal, saldo) VALUES (?, ?, ?, ?)',
                   (tipe, waktu, nominal, saldo))
        
    conn.commit()
    cursor.close()
    conn.close()