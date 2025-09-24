
import tkinter as tk
from tkinter import ttk, messagebox
import app.models as models

class MembershipsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Memberships')
        self.geometry('600x400')
        self._build()

    def _build(self):
        top = ttk.Frame(self); top.pack(fill='both', expand=True, padx=8, pady=8)
        self.tree = ttk.Treeview(top, columns=('id','name','duration','maxbooks','fee'), show='headings')
        for h in ('id','name','duration','maxbooks','fee'):
            self.tree.heading(h, text=h.title())
        self.tree.pack(fill='both', expand=True)
        frm = ttk.Frame(top); frm.pack()
        ttk.Button(frm, text='Add', command=self.add).pack(side='left', padx=4)
        self.load()

    def load(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        rows = models.list_memberships()
        for r in rows:
            self.tree.insert('', 'end', values=(r['id'], r['name'], r['duration_months'], r['max_books'], r['fee']))

    def add(self):
        d = tk.Toplevel(self); d.title('Add Membership')
        name = tk.StringVar(); dur = tk.StringVar(); maxb = tk.StringVar(); fee = tk.StringVar()
        ttk.Label(d, text='Name').grid(row=0,column=0); ttk.Entry(d, textvariable=name).grid(row=0,column=1)
        ttk.Label(d, text='Duration (months)').grid(row=1,column=0); ttk.Entry(d, textvariable=dur).grid(row=1,column=1)
        ttk.Label(d, text='Max Books').grid(row=2,column=0); ttk.Entry(d, textvariable=maxb).grid(row=2,column=1)
        ttk.Label(d, text='Fee').grid(row=3,column=0); ttk.Entry(d, textvariable=fee).grid(row=3,column=1)
        def save():
            models.add_membership(name.get(), int(dur.get() or 0), int(maxb.get() or 0), float(fee.get() or 0.0))
            messagebox.showinfo('Added','Membership added'); d.destroy(); self.load()
        ttk.Button(d, text='Save', command=save).grid(row=4,column=0,columnspan=2)
