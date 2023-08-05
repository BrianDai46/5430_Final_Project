import tkinter as tk
from scraper import Scraper
import asyncio
import json, os

class Application(tk.Frame):
    def __init__(self, master=None, loop=None):
        super().__init__(master)
        self.master = master
        self.loop = loop
        self.grid(sticky="nsew")
        self.urls = set()
        self.create_widgets()
        self.scraper = Scraper()
        self.pages = []
        
    def create_widgets(self): 
        # scraping frame
        frame1 = tk.Frame(self.master)
        frame1.grid(row=0, column=0, sticky="nsew")
        
        left_frame = tk.Frame(frame1)
        left_frame.grid(row=0, column=0, sticky="nsew")
        
        self.label = tk.Label(left_frame, text="NLP Application", font=("Helvetica", 16))
        self.label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        
        self.scrollbar = tk.Scrollbar(left_frame)
        self.output = tk.Text(left_frame, yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=2, rowspan=10, sticky="nsew")
        self.output.grid(row=0, column=1, rowspan=10, sticky="nsew")
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

        self.pages = [] # Stores the text for each page
        self.page_index = 0 # Stores the current page index

        self.page_label = tk.Label(left_frame, text="Current page number: {0}".format(self.page_index + 1))
        self.page_label.grid(row=4, column=0, columnspan=1, sticky="new")

        self.prev_button = tk.Button(left_frame, text="<< Prev", command=self.prevPage)
        self.prev_button.grid(row=5, column=0, sticky="new")

        self.next_button = tk.Button(left_frame, text="Next >>", command=self.nextPage)
        self.next_button.grid(row=6, column=0, sticky="new")
        
        self.quit = tk.Button(left_frame, text="QUIT", fg="red",
                              command=self.quitClient)
        self.quit.grid(row=8, column=0, columnspan=1, sticky="new")
        
        process_button = tk.Button(left_frame, text="Process Scraped Content", command=lambda: self.show_frame(frame2))
        process_button.grid(row=7, column=0, sticky="new")
        
        # processing frame
        frame2 = tk.Frame(self.master)
        frame2.grid(row=0, column=0, sticky="nsew")

        left_frame2 = tk.Frame(frame2)
        left_frame2.grid(row=0, column=0, sticky="nsew")

        self.label2 = tk.Label(left_frame2, text="NLP Application", font=("Helvetica", 16))
        self.label2.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        self.scrollbar2 = tk.Scrollbar(left_frame2)
        self.output2 = tk.Text(left_frame2, yscrollcommand=self.scrollbar2.set)
        self.scrollbar2.grid(row=0, column=2, rowspan=10, sticky="nsew")
        self.output2.grid(row=0, column=1, rowspan=10, sticky="nsew")
        self.scrollbar2.config(command=self.output2.yview)
        self.output2.config(state="disabled")

        self.ner_button = tk.Button(left_frame2, text="NER", command=self.nerProcessing)
        self.ner_button.grid(row=1, column=0, sticky="new")

        self.topic_classification_button = tk.Button(left_frame2, text="Topic Classification", command=self.topicClassification)
        self.topic_classification_button.grid(row=2, column=0, sticky="new")

        self.summarization_button = tk.Button(left_frame2, text="Summarization", command=self.summarization)
        self.summarization_button.grid(row=3, column=0, sticky="new")

        self.page_label_processing = tk.Label(left_frame2, text="Current page number: {0}".format(self.page_index + 1))
        self.page_label_processing.grid(row=4, column=0, columnspan=1, sticky="new")

        self.prev_button_processing = tk.Button(left_frame2, text="<< Prev", command=self.prevPageProcessing)
        self.prev_button_processing.grid(row=5, column=0, sticky="new")

        self.next_button_processing = tk.Button(left_frame2, text="Next >>", command=self.nextPageProcessing)
        self.next_button_processing.grid(row=6, column=0, sticky="new")

        back_button = tk.Button(left_frame2, text="Back", command=lambda: self.show_frame(frame1))
        back_button.grid(row=7, column=0, sticky="new")

        quit_button = tk.Button(left_frame2, text="QUIT", fg="red", command=self.quitClient)
        quit_button.grid(row=8, column=0, columnspan=1, sticky="new")

        self.scrollbar_processing = tk.Scrollbar(frame2)
        self.output_processing = tk.Text(frame2, yscrollcommand=self.scrollbar_processing.set)
        self.scrollbar_processing.grid(row=0, column=2, sticky="nsew")
        self.output_processing.grid(row=0, column=1, sticky="nsew")
        self.scrollbar_processing.config(command=self.output_processing.yview)
        self.output_processing.config(state="disabled")
        
        self.show_frame(frame1)
        
    def show_frame(self, frame):
        frame.tkraise()
    
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
            self.pages = [(idx, title, context) for idx, (title, context) in enumerate(content.items())]
            self.pageFormat()
            
    def pageFormat(self):
        self.updateOutput("Title: " + self.pages[self.page_index][1] + '\n\nArticle:\n' + self.pages[self.page_index][2])
    
    def prevPage(self):
        if self.page_index > 0:
            self.page_index -= 1
            self.pageFormat()
            self.page_label["text"] = "Current page number: {0}".format(self.page_index + 1)

    def nextPage(self):
        if self.page_index < len(self.pages) - 1:
            self.page_index += 1
            self.pageFormat()
            self.page_label["text"] = "Current page number: {0}".format(self.page_index + 1)
            
    def quitClient(self):
        if os.path.exists('output/output.json'):
            os.remove('output/output.json')
        self.master.destroy()
    
    def nerProcessing(self):
        pass
    
    def topicClassification(self):
        pass
    
    def summarization(self):
        pass
    
    def nextPageProcessing(self):
        pass
    
    def prevPageProcessing(self):
        pass
    
loop = asyncio.get_event_loop()     
root = tk.Tk()
root.geometry("755x317")
root.title("5430 Final Project")
app = Application(master=root, loop=loop)
app.mainloop()
# https://www.foxnews.com/politics/federal-judge-blocks-biden-administrations-asylum-policy-migrants
# https://www.foxnews.com/sports/ex-nfl-linebacker-dismisses-colin-kaepernicks-latest-comeback-attempt-senior-prom-was-years-ago