import tkinter as tk
from scraper import Scraper

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(sticky="nsew")
        self.create_widgets()

    def create_widgets(self): 
        self.master.columnconfigure(0, weight=1)  # Left column should grow
        self.master.columnconfigure(1, weight=3)  # Right column should grow more
        self.master.rowconfigure(0, weight=1)  # Only one row that should grow
        
        left_frame = tk.Frame(self)
        left_frame.grid(row=0, column=0, sticky="nsew")
        # 
        self.label = tk.Label(left_frame, text="NLP Application", font=("Helvetica", 16))
        self.label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        self.url_entry = tk.Entry(left_frame)
        self.url_entry.insert(0, "Enter the Article URL:")  # Default text
        self.url_entry.config(fg="grey")  # Change the text color to grey
        self.url_entry.bind("<FocusIn>", self.clear_placeholder)  # Clear when the box is clicked
        self.url_entry.grid(row=1, column=0, sticky="new")  # position the entry box
        
        self.enter_button = tk.Button(left_frame, text="Enter")
        self.enter_button.grid(row=2, column=0, sticky="new") 
        
        self.hi_there = tk.Button(left_frame)
        self.hi_there["text"] = "Scrape\nURL"
        self.hi_there["command"] = self.say_hi
        self.hi_there.grid(row=3, column=0, columnspan=1, sticky="new")

        self.quit = tk.Button(left_frame, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row=4, column=0, columnspan=1, sticky="new")
        
        self.output = tk.Text(self)
        # Place it in the right column. It spans 5 rows so it will be the same height as the other widgets
        self.output.grid(row=0, column=1, rowspan=4, sticky="nsew")
        self.output.config(state="disabled")

    def say_hi(self):
        print("hi there, everyone!")
        
    def clear_placeholder(self, event):
        if self.url_entry.get() == "Enter the Article URL:":
            self.url_entry.delete(0, "end")
            self.url_entry.config(fg="black")
        
root = tk.Tk()
root.geometry("700x300")
root.title("5430 Final Project")
app = Application(master=root)
app.mainloop()