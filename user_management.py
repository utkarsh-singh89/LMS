
import tkinter as tk
from tkinter import ttk, messagebox
import app.models as models

class UserManagementWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("User Management")
        self.geometry("900x520")
        self.parent = parent
        self._build()

    def _build(self):
        top = ttk.Frame(self, padding=8)
        top.pack(fill='both', expand=True)
        search_frame = ttk.Frame(top)
        search_frame.pack(fill='x')
        ttk.Label(search_frame, text='Search Name/Email:').pack(side='left')
        self.search_var = tk.StringVar()
        ent = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        ent.pack(side='left', padx=5)
        ent.bind('<KeyRelease>', lambda e: self.load_users())
        ttk.Button(search_frame, text='New', command=self.new_user).pack(side='left', padx=5)

        self.tree = ttk.Treeview(top, columns=('id','name','email','role','membership'), show='headings')
        for c in ('id','name','email','role','membership'):
            self.tree.heading(c, text=c.title())
        self.tree.pack(fill='both', expand=True, pady=8)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        form = ttk.Frame(top)
        form.pack(fill='x', pady=5)
        self.mode_var = tk.StringVar(value='new')
        ttk.Radiobutton(form, text='New user', variable=self.mode_var, value='new').grid(row=0,column=0)
        ttk.Radiobutton(form, text='Existing user', variable=self.mode_var, value='existing').grid(row=0,column=1)

        ttk.Label(form, text='Name').grid(row=1,column=0, sticky='e')
        self.name_var = tk.StringVar(); ttk.Entry(form, textvariable=self.name_var, width=30).grid(row=1,column=1)
        ttk.Label(form, text='Email').grid(row=2,column=0, sticky='e')
        self.email_var = tk.StringVar(); ttk.Entry(form, textvariable=self.email_var, width=30).grid(row=2,column=1)
        ttk.Label(form, text='Password').grid(row=3,column=0, sticky='e')
        self.pw_var = tk.StringVar(); ttk.Entry(form, textvariable=self.pw_var, show='*', width=30).grid(row=3,column=1)
        ttk.Label(form, text='Role').grid(row=4,column=0, sticky='e')
        self.role_cb = ttk.Combobox(form, values=['admin','user'], width=27); self.role_cb.grid(row=4,column=1)
        ttk.Label(form, text='Membership').grid(row=5,column=0, sticky='e')
        self.mem_cb = ttk.Combobox(form, values=[m['name'] for m in models.list_memberships()] if models.list_memberships() else [], width=27); self.mem_cb.grid(row=5,column=1)

        btnf = ttk.Frame(top); btnf.pack()
        ttk.Button(btnf, text='Save', command=self.save).pack(side='left', padx=5)
        ttk.Button(btnf, text='Delete', command=self.delete).pack(side='left', padx=5)
        ttk.Button(btnf, text='Clear', command=self.clear).pack(side='left', padx=5)

        self.load_users()

    def load_users(self):
        q = self.search_var.get().strip()
        rows = models.list_users(q if q else None)
        for i in self.tree.get_children(): self.tree.delete(i)
        for r in rows:
            mem = None
            if r['membership_id']:
                mem_obj = models.get_membership(r['membership_id'])
                mem = mem_obj['name'] if mem_obj else ''
            self.tree.insert('', 'end', values=(r['id'], r['name'], r['email'], r['role'], mem))

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel[0])['values']
        self.mode_var.set('existing')
        self.name_var.set(vals[1])
        self.email_var.set(vals[2])
        self.role_cb.set(vals[3])
        self.mem_cb.set(vals[4] if vals[4] else '')

    def new_user(self):
        self.mode_var.set('new')
        self.clear()

    def clear(self):
        self.name_var.set(''); self.email_var.set(''); self.pw_var.set(''); self.role_cb.set(''); self.mem_cb.set('')

    def save(self):
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        pw = self.pw_var.get()
        role = self.role_cb.get() or 'user'
        mem_name = self.mem_cb.get() or None
        if not name:
            messagebox.showerror('Validation','Name required'); return
        mem_id = None
        if mem_name:
            mlist = models.list_memberships()
            for m in mlist:
                if m['name']==mem_name:
                    mem_id = m['id']
        if self.mode_var.get()=='new':
            if not email or not pw:
                messagebox.showerror('Validation','Email & Password required for new user'); return
            try:
                models.create_user(name,email,pw,role,mem_id)
                messagebox.showinfo('Success','User created')
                self.load_users(); self.clear()
            except Exception as e:
                messagebox.showerror('Error', str(e))
        else:
            sel = self.tree.selection()
            if not sel:
                messagebox.showerror('Error','Select user to update'); return
            uid = self.tree.item(sel[0])['values'][0]
            try:
                models.update_user(uid,name,role,mem_id,pw if pw else None)
                messagebox.showinfo('Success','User updated')
                self.load_users(); self.clear()
            except Exception as e:
                messagebox.showerror('Error', str(e))

    def delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror('Error','Select user to delete'); return
        uid = self.tree.item(sel[0])['values'][0]
        if messagebox.askyesno('Confirm','Delete user?'):
            models.delete_user(uid)
            messagebox.showinfo('Deleted','User removed')
            self.load_users()
