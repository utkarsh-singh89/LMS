
import tkinter as tk
from tkinter import ttk, messagebox
import app.models as models

class ReportsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Reports')
        self.geometry('600x400')
        ttk.Button(self, text='Summary', command=self.summary).pack(pady=10)
        self.txt = tk.Text(self); self.txt.pack(fill='both', expand=True)

    def summary(self):
        books = models.search_books()
        issues = models.list_issues()
        overdue = [i for i in issues if i['status']!='returned' and i['due_date'] < None]
        self.txt.delete('1.0','end')
        self.txt.insert('end', f'Total books: {len(books)}\nTotal issues: {len(issues)}\n')
