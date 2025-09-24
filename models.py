
import sqlite3
from datetime import date, timedelta, datetime
import bcrypt

DB = 'library.db'

def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

# User APIs
def create_user(name,email,password,role='user',membership_id=None):
    c = conn()
    cur = c.cursor()
    pw = password.encode('utf-8')
    hashed = bcrypt.hashpw(pw, bcrypt.gensalt())
    try:
        cur.execute('INSERT INTO users (name,email,password_hash,role,membership_id) VALUES (?,?,?,?,?)',
                    (name,email,hashed,role,membership_id))
        c.commit()
        return cur.lastrowid
    except Exception as e:
        c.close()
        raise
    finally:
        c.close()

def get_user_by_email(email):
    c = conn()
    cur = c.cursor()
    cur.execute('SELECT * FROM users WHERE email=?', (email,))
    r = cur.fetchone()
    c.close()
    return r

def get_user_by_id(uid):
    c = conn()
    cur = c.cursor()
    cur.execute('SELECT * FROM users WHERE id=?', (uid,))
    r = cur.fetchone()
    c.close()
    return r

def verify_user(email,password):
    u = get_user_by_email(email)
    if not u:
        return None
    if bcrypt.checkpw(password.encode('utf-8'), u['password_hash']):
        return u
    return None

def list_users(q=None):
    c = conn()
    cur = c.cursor()
    if q:
        like = f"%{q}%"
        cur.execute('SELECT * FROM users WHERE name LIKE ? OR email LIKE ?',(like,like))
    else:
        cur.execute('SELECT * FROM users')
    rows = cur.fetchall()
    c.close()
    return rows

def update_user(uid, name, role, membership_id, password=None):
    c = conn()
    cur = c.cursor()
    if password:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cur.execute('UPDATE users SET name=?, role=?, membership_id=?, password_hash=? WHERE id=?',
                    (name,role,membership_id,hashed,uid))
    else:
        cur.execute('UPDATE users SET name=?, role=?, membership_id=? WHERE id=?',
                    (name,role,membership_id,uid))
    c.commit()
    c.close()

def delete_user(uid):
    c = conn()
    cur = c.cursor()
    cur.execute('DELETE FROM users WHERE id=?', (uid,))
    c.commit()
    c.close()

# Memberships
def list_memberships():
    c = conn()
    cur = c.cursor()
    cur.execute('SELECT * FROM memberships')
    rows = cur.fetchall()
    c.close()
    return rows

def add_membership(name,duration_months,max_books,fee):
    c = conn()
    cur = c.cursor()
    cur.execute('INSERT INTO memberships (name,duration_months,max_books,fee) VALUES (?,?,?,?)',
                (name,duration_months,max_books,fee))
    c.commit()
    c.close()

# Books
def add_book(title,author,isbn,category,copies,shelf,year,publisher):
    c = conn()
    cur = c.cursor()
    cur.execute('INSERT INTO books (title,author,isbn,category,copies_total,copies_available,shelf,year,publisher) VALUES (?,?,?,?,?,?,?,?,?)',
                (title,author,isbn,category,copies,copies,shelf,year,publisher))
    c.commit()
    bid = cur.lastrowid
    c.close()
    return bid

def search_books(q=None, available_only=False):
    c = conn()
    cur = c.cursor()
    sql = 'SELECT * FROM books'
    params=[]
    where=[]
    if available_only:
        where.append('copies_available>0')
    if q:
        where.append('(title LIKE ? OR author LIKE ? OR isbn LIKE ?)')
        params.extend([f'%{q}%']*3)
    if where:
        sql += ' WHERE ' + ' AND '.join(where)
    cur.execute(sql, params)
    rows = cur.fetchall()
    c.close()
    return rows

def get_book(bid):
    c = conn()
    cur = c.cursor()
    cur.execute('SELECT * FROM books WHERE id=?', (bid,))
    r = cur.fetchone()
    c.close()
    return r

def update_book_copies(bid, delta):
    c = conn()
    cur = c.cursor()
    cur.execute('UPDATE books SET copies_available = copies_available + ? WHERE id=?', (delta,bid))
    c.commit()
    c.close()

# Issues & Transactions
FINE_RATE = 2.0  # per day

def issue_book(book_id, user_id, days=None):
    c = conn()
    cur = c.cursor()
    today = date.today()
    if days is None:
        # determine from membership
        u = get_user_by_id(user_id)
        if u and u['membership_id']:
            m = get_membership(u['membership_id'])
            if m and m['duration_months']:
                days = m['duration_months']*30
        if not days:
            days = 14
    due = today + timedelta(days=days)
    cur.execute('INSERT INTO issues (book_id,user_id,issue_date,due_date,status) VALUES (?,?,?,?,?)',
                (book_id,user_id,today.isoformat(),due.isoformat(),'issued'))
    cur.execute('UPDATE books SET copies_available = copies_available - 1 WHERE id=? AND copies_available>0', (book_id,))
    c.commit()
    iid = cur.lastrowid
    c.close()
    return iid

def return_book(issue_id, return_date=None):
    c = conn()
    cur = c.cursor()
    cur.execute('SELECT * FROM issues WHERE id=?', (issue_id,))
    issue = cur.fetchone()
    if not issue:
        c.close()
        return None
    if return_date:
        rd = datetime.fromisoformat(return_date).date()
    else:
        rd = date.today()
    due = datetime.fromisoformat(issue['due_date']).date()
    overdue = (rd - due).days
    fine = FINE_RATE * overdue if overdue>0 else 0
    cur.execute('UPDATE issues SET return_date=?, status=?, fine=? WHERE id=?', (rd.isoformat(), 'returned', fine, issue_id))
    cur.execute('UPDATE books SET copies_available = copies_available + 1 WHERE id=?', (issue['book_id'],))
    if fine>0:
        cur.execute('INSERT INTO transactions (user_id,type,amount,method,notes) VALUES (?,?,?,?,?)',
                    (issue['user_id'],'fine',fine,'pending',f'Fine for issue {issue_id}'))
    c.commit()
    c.close()
    return {'fine':fine, 'overdue_days': max(0, overdue)}

def list_issues(user_id=None, status=None):
    c = conn()
    cur = c.cursor()
    sql = 'SELECT * FROM issues'
    params=[]
    where=[]
    if user_id:
        where.append('user_id=?'); params.append(user_id)
    if status:
        where.append('status=?'); params.append(status)
    if where:
        sql += ' WHERE ' + ' AND '.join(where)
    cur.execute(sql, params)
    rows = cur.fetchall()
    c.close()
    return rows

# Helpers
def get_membership(mid):
    c = conn()
    cur = c.cursor()
    cur.execute('SELECT * FROM memberships WHERE id=?', (mid,))
    r = cur.fetchone()
    c.close()
    return r

def add_transaction(user_id, type_, amount, method='mock', notes=None):
    c = conn()
    cur = c.cursor()
    cur.execute('INSERT INTO transactions (user_id,type,amount,method,notes) VALUES (?,?,?,?,?)',
                (user_id,type_,amount,method,notes))
    c.commit()
    c.close()
