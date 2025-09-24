import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import app.models as models

class BookManagementWindow(tk.Toplevel):
    def __init__(self, parent, current_user=None):
        super().__init__(parent)
        self.title('Books')
        self.geometry('900x500')
        self.current_user = current_user
        self._build()

    def _is_admin(self):
        """Return True if current_user is admin or if no user provided (admin context)."""
        u = self.current_user
        if not u:
            return True
        # try mapping-style access (sqlite3.Row or dict)
        try:
            role = u['role']
        except Exception:
            # try attribute access
            role = getattr(u, 'role', None)
        return role == 'admin'

    def _build(self):
        top = ttk.Frame(self); top.pack(fill='both', expand=True, padx=8, pady=8)
        sframe = ttk.Frame(top); sframe.pack(fill='x')
        ttk.Label(sframe, text='Search:').pack(side='left')
        self.q = tk.StringVar()
        ttk.Entry(sframe, textvariable=self.q).pack(side='left', padx=4)
        ttk.Button(sframe, text='Search', command=self.load).pack(side='left', padx=4)

        # Add Book button only for admins
        if self._is_admin():
            ttk.Button(sframe, text='Add Book', command=self.add_book).pack(side='right')

        self.tree = ttk.Treeview(top, columns=('id','title','author','avail'), show='headings')
        for h in ('id','title','author','avail'):
            self.tree.heading(h, text=h.title())
            self.tree.column(h, width=60 if h=='id' else 250)
        self.tree.pack(fill='both', expand=True)
        btns = ttk.Frame(top); btns.pack(pady=6)

        # Issue / Return buttons only for admins
        if self._is_admin():
            ttk.Button(btns, text='Issue', command=self.issue).pack(side='left', padx=4)
            ttk.Button(btns, text='Return', command=self.return_book).pack(side='left', padx=4)

        # Load initially (show all books)
        self.load()

    def load(self):
        """Populate the tree with search results (or all books if blank)."""
        for i in self.tree.get_children():
            self.tree.delete(i)

        q = self.q.get().strip() or None
        rows = models.search_books(q, available_only=False)

        # rows is a list of sqlite rows or dict-like rows
        for r in rows:
            # safe access for both sqlite3.Row and dict
            try:
                bid = r['id']
                title = r['title']
                author = r['author']
                avail = r['copies_available']
            except Exception:
                # fallback if r is tuple-like
                bid = r[0]
                title = r[1]
                author = r[2]
                # copies_available may be at index 5 depending on schema
                avail = r[5] if len(r) > 5 else ''
            self.tree.insert('', 'end', values=(bid, title, author, avail))

    def add_book(self):
        dlg = tk.Toplevel(self); dlg.title('Add Book')
        entries = {}
        labels = ['Title','Author','ISBN','Category','Copies','Shelf','Year','Publisher']
        for idx,label in enumerate(labels):
            ttk.Label(dlg, text=label).grid(row=idx,column=0, sticky='e', padx=6, pady=2)
            sv = tk.StringVar(); ttk.Entry(dlg,textvariable=sv).grid(row=idx,column=1, padx=6, pady=2)
            entries[label]=sv
        def submit():
            title = entries['Title'].get().strip()
            if not title:
                messagebox.showerror('Validation','Title required')
                return
            try:
                copies = int(entries['Copies'].get() or 1)
            except ValueError:
                messagebox.showerror('Validation','Copies must be a number')
                return
            models.add_book(
                title,
                entries['Author'].get(),
                entries['ISBN'].get() or None,
                entries['Category'].get(),
                copies,
                entries['Shelf'].get(),
                int(entries['Year'].get() or 0),
                entries['Publisher'].get()
            )
            messagebox.showinfo('Added','Book added')
            dlg.destroy()
            self.load()
        ttk.Button(dlg, text='Save', command=submit).grid(row=len(labels),column=0,columnspan=2, pady=8)

    def issue(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('Select','Select a book')
            return
        bid = self.tree.item(sel[0])['values'][0]
        # Admin must specify user email or issue on behalf
        email = simpledialog.askstring('User email','Enter user email to issue to:')
        if not email:
            return
        user = models.get_user_by_email(email)
        if not user:
            messagebox.showerror('Not found','User not found')
            return
        uid = user['id']
        if messagebox.askyesno('Confirm','Issue selected book?'):
            iid = models.issue_book(bid, uid)
            messagebox.showinfo('Issued', f'Issue created id {iid}')
            self.load()

    def return_book(self):
        iid = simpledialog.askinteger('Issue id','Enter issue id to return:')
        if not iid:
            return
        if messagebox.askyesno('Confirm','Return this issue?'):
            res = models.return_book(iid)
            if res is None:
                messagebox.showerror('Error','Issue not found')
            else:
                fine = res.get('fine') if isinstance(res, dict) else res['fine']
                messagebox.showinfo('Returned', f'Fine: ₹{fine}')
                self.load()
