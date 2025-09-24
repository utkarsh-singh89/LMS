import tkinter as tk
from tkinter import ttk, messagebox
import app.models as models

class TransactionsWindow(tk.Toplevel):
    def __init__(self, parent, current_user=None):
        super().__init__(parent)
        self.title('Transactions / Issues')
        self.geometry('800x500')
        self.current_user = current_user
        self._build()

    def _is_admin(self):
        u = self.current_user
        if not u:
            return True
        try:
            role = u['role']
        except Exception:
            role = getattr(u, 'role', None)
        return role == 'admin'

    def _build(self):
        top = ttk.Frame(self); top.pack(fill='both', expand=True,padx=8,pady=8)
        self.tree = ttk.Treeview(top, columns=('id','book_id','user_id','issue_date','due_date','status','fine'), show='headings')
        for h in ('id','book_id','user_id','issue_date','due_date','status','fine'):
            self.tree.heading(h, text=h.title())
            self.tree.column(h, width=100)
        self.tree.pack(fill='both', expand=True)
        frm = ttk.Frame(top); frm.pack(pady=6)
        ttk.Button(frm, text='Refresh', command=self.load).pack(side='left', padx=4)
        # Only admins get the Return Selected button
        if self._is_admin():
            ttk.Button(frm, text='Return Selected', command=self.return_selected).pack(side='left', padx=4)
        self.load()

    def load(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        # If a regular user is viewing, show only their transactions
        if self.current_user and not self._is_admin():
            rows = models.list_issues(user_id=self.current_user['id'])
        else:
            rows = models.list_issues()
        for r in rows:
            self.tree.insert('', 'end', values=(r['id'], r['book_id'], r['user_id'], r['issue_date'], r['due_date'], r['status'], r['fine']))

    def return_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('Select','Select an issue')
            return
        iid = self.tree.item(sel[0])['values'][0]
        if messagebox.askyesno('Confirm','Return this issue?'):
            res = models.return_book(iid)
            if res:
                messagebox.showinfo('Returned', f'Fine: ₹{res.get("fine",0)}')
                self.load()
            else:
                messagebox.showerror('Error','Issue not found')
