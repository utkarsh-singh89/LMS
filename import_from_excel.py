
import pandas as pd
import sqlite3
import bcrypt

DB = 'library.db'

def db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def import_memberships(path):
    xl = pd.ExcelFile(path)
    if 'Master List of Memberships' not in xl.sheet_names:
        return 'No memberships sheet'
    df = pd.read_excel(path, sheet_name='Master List of Memberships')
    c = db(); cur = c.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS memberships (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, duration_months INTEGER, max_books INTEGER, fee REAL)')
    for _,r in df.iterrows():
        cur.execute('INSERT OR REPLACE INTO memberships (name,duration_months,max_books,fee) VALUES (?,?,?,?)',
                    (r.get('Name', ''), int(r.get('DurationMonths') or 0), int(r.get('MaxBooks') or 0), float(r.get('Fee') or 0)))
    c.commit(); c.close()
    return f'Imported {len(df)} memberships'

def import_books(path):
    xl = pd.ExcelFile(path)
    if 'Master List of Books' not in xl.sheet_names:
        return 'No books sheet'
    df = pd.read_excel(path, sheet_name='Master List of Books')
    c = db(); cur = c.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT, isbn TEXT UNIQUE, category TEXT, copies_total INTEGER, copies_available INTEGER, shelf TEXT, year INTEGER, publisher TEXT, tags TEXT)')
    for _,r in df.iterrows():
        cur.execute('INSERT OR REPLACE INTO books (title,author,isbn,category,copies_total,copies_available,shelf,year,publisher,tags) VALUES (?,?,?,?,?,?,?,?,?,?)',
                    (r.get('Title',''), r.get('Author',''), r.get('ISBN',None), int(r.get('CopiesTotal') or 1), int(r.get('CopiesAvailable') or 1), r.get('Shelf',''), int(r.get('Year') or 0), r.get('Publisher',''), r.get('Tags','')))
    c.commit(); c.close()
    return f'Imported {len(df)} books'

def import_movies(path):
    xl = pd.ExcelFile(path)
    if 'Master List of Movies' not in xl.sheet_names:
        return 'No movies sheet'
    df = pd.read_excel(path, sheet_name='Master List of Movies')
    c = db(); cur = c.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, director TEXT, category TEXT, year INTEGER, copies_total INTEGER, copies_available INTEGER)')
    for _,r in df.iterrows():
        cur.execute('INSERT OR REPLACE INTO movies (title,director,category,year,copies_total,copies_available) VALUES (?,?,?,?,?,?)',
                    (r.get('Title',''), r.get('Director',''), r.get('Category',''), int(r.get('Year') or 0), int(r.get('CopiesTotal') or 1), int(r.get('CopiesAvailable') or 1)))
    c.commit(); c.close()
    return f'Imported {len(df)} movies'

def import_users(path):
    xl = pd.ExcelFile(path)
    if 'Users' not in xl.sheet_names:
        return 'No users sheet'
    df = pd.read_excel(path, sheet_name='Users')
    c = db(); cur = c.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT UNIQUE, password_hash TEXT, role TEXT, membership_id INTEGER)')
    imported = 0
    for _,r in df.iterrows():
        name = r.get('Name') or r.get('name') or ''
        email = r.get('Email') or r.get('email') or None
        pw = r.get('Password') or 'password'
        role = r.get('Role') or 'user'
        if not email: continue
        hashed = bcrypt.hashpw(str(pw).encode('utf-8'), bcrypt.gensalt())
        try:
            cur.execute('INSERT OR REPLACE INTO users (name,email,password_hash,role) VALUES (?,?,?,?)',(name,email,hashed,role))
            imported += 1
        except:
            pass
    c.commit(); c.close()
    return f'Imported {imported} users'

def import_all(path):
    res = []
    res.append(import_memberships(path))
    res.append(import_books(path))
    res.append(import_movies(path))
    res.append(import_users(path))
    return '\n'.join(res)
