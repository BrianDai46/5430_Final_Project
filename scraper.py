import asyncio
from pyppeteer import launch

class Scraper():
    def __init__(self) -> None:
        self.url_texts = dict()
        self.browser = None

    async def extract_body_text(self, url):
        page = await self.browser.newPage()

        await page.goto(url, timeout=60000)
        await asyncio.sleep(3)

        title = await page.evaluate('''() => {
            let element = document.querySelector('h1'); 
            return element.innerText;
        }''')
        
        body = await page.evaluate('''() => {
            let texts = [];
            let elements = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, span'); // specify here the tags you want to include

            for (let i = 0; i < elements.length; i++) {
                let element = elements[i];
                texts.push(element.innerText);
            }

            return texts.join(" ");
        }''')
        title = ' '.join(title.split())
        body = ' '.join(body.split())
        self.url_texts[title] = body.encode('utf-8')
        await page.close()
    
    async def setup(self):
        self.browser = await launch()
        
    async def teardown(self):
        await self.browser.close()
    
    def scrape_urls(self, urls):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.setup())
        for url in urls:
            loop.run_until_complete(self.extract_body_text(url))
        loop.run_until_complete(self.teardown())

""" example = {'https://www.foxnews.com/politics/federal-judge-blocks-biden-administrations-asylum-policy-migrants',
           'https://www.foxnews.com/sports/ex-nfl-linebacker-dismisses-colin-kaepernicks-latest-comeback-attempt-senior-prom-was-years-ago'} 

scraper = Scraper()
scraper.scrape_urls(example) """



