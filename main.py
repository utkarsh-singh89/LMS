
import tkinter as tk
from tkinter import ttk, messagebox
import app.models as models

def open_admin(root,user):
    from app.user_management import UserManagementWindow
    from app.maintenance import MaintenanceWindow
    from app.book_management import BookManagementWindow
    from app.memberships import MembershipsWindow
    from app.transactions import TransactionsWindow
    from app.reports import ReportsWindow
    win = tk.Toplevel(root); win.title('Admin Home')
    ttk.Label(win, text=f'Welcome Admin: {user["name"]}').pack()
    ttk.Button(win, text='User Management', command=lambda: UserManagementWindow(win)).pack(fill='x')
    ttk.Button(win, text='Maintenance', command=lambda: MaintenanceWindow(win)).pack(fill='x')
    ttk.Button(win, text='Books', command=lambda: BookManagementWindow(win)).pack(fill='x')
    ttk.Button(win, text='Memberships', command=lambda: MembershipsWindow(win)).pack(fill='x')
    ttk.Button(win, text='Transactions', command=lambda: TransactionsWindow(win)).pack(fill='x')
    ttk.Button(win, text='Reports', command=lambda: ReportsWindow(win)).pack(fill='x')

def open_user(root, user):
    # user: sqlite Row (mapping)
    from app.book_management import BookManagementWindow
    from app.transactions import TransactionsWindow

    win = tk.Toplevel(root)
    win.title('User Home')
    ttk.Label(win, text=f'Welcome User: {user["name"]}').pack(pady=8)

    # Pass current_user to BookManagementWindow so it hides admin actions
    ttk.Button(win, text='Search Books', command=lambda: BookManagementWindow(win, current_user=user)).pack(fill='x', padx=8, pady=4)

    # My Transactions should show only the user's transactions and no return button
    ttk.Button(win, text='My Transactions', command=lambda: TransactionsWindow(win, current_user=user)).pack(fill='x', padx=8, pady=4)


class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Library Management - Login')
        self.geometry('400x250')
        frame = ttk.Frame(self, padding=10); frame.pack(expand=True)
        ttk.Label(frame, text='Email').pack()
        self.email = ttk.Entry(frame); self.email.pack()
        ttk.Label(frame, text='Password').pack()
        self.pw = ttk.Entry(frame, show='*'); self.pw.pack()
        ttk.Button(frame, text='Login', command=self.login).pack(pady=8)
        ttk.Button(frame, text='Quit', command=self.destroy).pack()

    def login(self):
        email = self.email.get().strip()
        pw = self.pw.get()
        user = models.get_user_by_email(email)
        if not user:
            messagebox.showerror('Error','Invalid credentials')
            return
        # verify password using bcrypt check
        import bcrypt
        if not bcrypt.checkpw(pw.encode('utf-8'), user['password_hash']):
            messagebox.showerror('Error','Invalid credentials'); return
        if user['role']=='admin':
            open_admin(self, user)
        else:
            open_user(self, user)

if __name__ == '__main__':
    app = LoginApp()
    app.mainloop()
