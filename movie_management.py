
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class MovieManagementWindow(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.title('Movies')
        self.geometry('700x400')
        ttk.Label(self, text='Movie Management (basic)').pack()
