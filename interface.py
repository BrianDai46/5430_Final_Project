import tkinter as tk
from scraper import Scraper

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self): 
        self.label = tk.Label(self, text="5430 Final Project")
        self.label.pack(side="top")
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")
        
root = tk.Tk()
root.geometry("1720x1080")
root.title("5430 Final Project")
app = Application(master=root)
app.mainloop()