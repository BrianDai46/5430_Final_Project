import tkinter as tk
from scraper import Scraper
import asyncio
import json

class Application(tk.Frame):
    def __init__(self, master=None, loop=None):
        super().__init__(master)
        self.master = master
        self.loop = loop
        self.grid(sticky="nsew")
        self.urls = set()
        self.create_widgets()
        self.scraper = Scraper()
        
    def create_widgets(self): 
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=3)
        self.master.rowconfigure(0, weight=1)
        
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
        self.url_entry.insert(0, "Enter the Article URL:")
        self.url_entry.config(fg="grey")
        self.url_entry.bind("<FocusIn>", self.clearPlaceholder)
        self.url_entry.grid(row=1, column=0, sticky="new")
        
        self.enter_button = tk.Button(left_frame, text="Enter", command=self.storeUrl)
        self.enter_button.grid(row=2, column=0, sticky="new") 
        
        self.scrape_urls = tk.Button(left_frame)
        self.scrape_urls["text"] = "Scrape\nURL"
        self.scrape_urls["command"] = self.startScraping
        self.scrape_urls.grid(row=3, column=0, columnspan=1, sticky="new")

        self.quit = tk.Button(left_frame, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row=4, column=0, columnspan=1, sticky="new")
        
    def storeUrl(self):
        url = self.url_entry.get()
        if url and url != "Enter the Article URL:":
            self.urls.add(url)
            print(self.urls)
        self.url_entry.delete(0, 'end')
        
    def clearPlaceholder(self, event):
        if self.url_entry.get() == "Enter the Article URL:":
            self.url_entry.delete(0, "end")
            self.url_entry.config(fg="black")
            
    def updateOutput(self, text):
        self.clearOutput()
        self.output.config(state="normal")
        self.output.insert("end", text)
        self.output.config(state="disabled")
        
    def clearOutput(self):
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.config(state="disabled")
        
    def onScraping(self):
        self.scrape_urls["text"] = "Scraping..."
        self.scrape_urls["state"] = "disabled"
        self.enter_button["state"] = "disabled"
        
    def doneScraping(self):
        self.scrape_urls["text"] = "Scrape\nURL"
        self.scrape_urls["state"] = "normal"
        self.enter_button["state"] = "normal"
        
    def startScraping(self):
        self.onScraping()
        self.loop.create_task(self.scrapeUrls(self.urls))
        
    def scrapeUrls(self, urls):
        self.scraper.scrape_urls(urls)
        self.onScrapingDone()
        
    def onScrapingDone(self):
        self.doneScraping()
        with open('output/output.json', 'r') as f:
            content = json.load(f)
        for title, context in content.items():
            self.updateOutput(title + ':\n\n' + context)
            break
    
loop = asyncio.get_event_loop()     
root = tk.Tk()
root.geometry("755x317")
root.title("5430 Final Project")
app = Application(master=root, loop=loop)
app.mainloop()
