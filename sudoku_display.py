import tkinter as tk
from tkinter import Tk,ttk,Label,Entry,Button,mainloop,Text,Frame,StringVar
import os
from PIL import Image, ImageTk, ImageDraw
from text_window import TextWriter

class Display:
    def __init__(self,parent):
        self.parent = parent
        self.main_font = ("Courier", 22, "bold")
        self.max_win_size = (1915,960)
        self.setup_window()
    def setup_window(self):
        self.primary_window = Tk()
        self.primary_window.wm_title("Sudoku Solver Tree")
        self.primary_window.geometry('913x960+1000+82')
        self.primary_window.minsize(width=110, height=30)
        self.primary_window.maxsize(width=self.max_win_size[0], height=self.max_win_size[1])
        
        textbox=Text(self.primary_window, background="#000000",foreground="#00AA00",width=110,height=28)
        textbox.config(font = self.main_font)
        textbox.pack()
        self.textbox = TextWriter(textbox,center=False)