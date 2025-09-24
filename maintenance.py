
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from scripts import import_from_excel
import threading

class MaintenanceWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Maintenance')
        self.geometry('600x300')
        ttk.Label(self, text='Admin Maintenance - Import Excel').pack(pady=6)
        self.file_label = ttk.Label(self, text='No file selected')
        self.file_label.pack()
        ttk.Button(self, text='Select Excel File', command=self.select_file).pack(pady=4)
        ttk.Button(self, text='Import', command=self.import_file).pack(pady=4)
        self.log = tk.Text(self, height=10)
        self.log.pack(fill='both', expand=True)
        self.filepath = None

    def select_file(self):
        path = filedialog.askopenfilename(filetypes=[('Excel files','*.xlsx;*.xls')])
        if path:
            self.filepath = path
            self.file_label.config(text=path)

    def import_file(self):
        if not self.filepath:
            messagebox.showerror('Error','Select a file first'); return
        def run():
            self.log.insert('end','Starting import...\n')
            try:
                res = import_from_excel.import_all(self.filepath)
                self.log.insert('end', res + '\n')
                messagebox.showinfo('Import', 'Import completed')
            except Exception as e:
                self.log.insert('end', 'Error: '+str(e)+'\n')
                messagebox.showerror('Error', str(e))
        threading.Thread(target=run).start()
