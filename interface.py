import tkinter as tk
from scraper import Scraper
import threading

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(sticky="nsew")
        self.urls = set()
        self.create_widgets()
        self.scraper = Scraper()
        
    def create_widgets(self): 
        self.master.columnconfigure(0, weight=1)  # Left column should grow
        self.master.columnconfigure(1, weight=3)  # Right column should grow more
        self.master.rowconfigure(0, weight=1)  # Only one row that should grow
        
        left_frame = tk.Frame(self)
        left_frame.grid(row=0, column=0, sticky="nsew")
        
        self.label = tk.Label(left_frame, text="NLP Application", font=("Helvetica", 16))
        self.label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        
        self.scrollbar = tk.Scrollbar(self)
        self.output = tk.Text(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=2, rowspan=5, sticky="nsew")
        self.output.grid(row=0, column=1, rowspan=4, sticky="nsew")
        self.scrollbar.config(command=self.output.yview)
        self.output.config(state="disabled")

        self.url_entry = tk.Entry(left_frame)
        self.url_entry.insert(0, "Enter the Article URL:")  # Default text
        self.url_entry.config(fg="grey")  # Change the text color to grey
        self.url_entry.bind("<FocusIn>", self.clear_placeholder)  # Clear when the box is clicked
        self.url_entry.grid(row=1, column=0, sticky="new")  # position the entry box
        
        self.enter_button = tk.Button(left_frame, text="Enter", command=self.store_url)
        self.enter_button.grid(row=2, column=0, sticky="new") 
        
        self.scrape_urls = tk.Button(left_frame)
        self.scrape_urls["text"] = "Scrape\nURL"
        self.scrape_urls["command"] = self.start_scraping
        self.scrape_urls.grid(row=3, column=0, columnspan=1, sticky="new")

        self.quit = tk.Button(left_frame, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row=4, column=0, columnspan=1, sticky="new")
        
        
        
    def store_url(self):
        # Get the current text in url_entry
        url = self.url_entry.get()
        # Only store url if the box is not empty or containing the default text
        if url and url != "Enter the Article URL:":
            self.urls.add(url)
            print(self.urls)
        self.url_entry.delete(0, 'end')
        
    def clear_placeholder(self, event):
        if self.url_entry.get() == "Enter the Article URL:":
            self.url_entry.delete(0, "end")
            self.url_entry.config(fg="black")
            
    def update_output(self, text):
        self.clear_output()
        self.output.config(state="normal")  # Enable the Text widget
        self.output.insert("end", text)  # Insert text at the end
        self.output.config(state="disabled")
        
    def clear_output(self):
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.config(state="disabled")
        
    def start_scraping(self):
        self.scrape_urls["text"] = "Scraping..."  # Change the button text to show that scraping is in progress
        self.scrape_urls["state"] = "disabled"  # Disable the button while scraping is in progress
        # Start the scraping in a separate thread
        threading.Thread(target=self.scrape_urls, args=(self.urls,), daemon=True).start()
        
    def scrape_urls(self, urls):
        self.scraper.scrape_urls(urls)  # Call the scrape_urls method of the Scraper instance
        # After scraping is done, update the GUI in the main thread
        self.master.after(0, self.on_scraping_done)
        
    def on_scraping_done(self):
        self.scrape_urls["text"] = "Scrape\nURL"  # Change the button text back to the original text
        self.scrape_urls["state"] = "normal"
    
"""     def text_scrape(self, setUrls):
        self.scraper.scrape_urls(setUrls)
        if self.scraper.url_texts:
            self.update_output(self.scraper.url_texts.items()[0][0] + ":\n\n" + self.scraper.url_texts.items()[0][1])
        self.urls = set() """
    
    
        
root = tk.Tk()
root.geometry("700x300")
root.title("5430 Final Project")
app = Application(master=root)
app.mainloop()