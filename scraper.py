import asyncio
from pyppeteer import launch

class Scraper():
    def __init__(self) -> None:
        pass

    async def extract_body_text(self, url):
        browser = await launch()
        page = await browser.newPage()

        await page.goto(url, timeout=60000)
        await asyncio.sleep(3)

        title = await page.evaluate('''() => {
            let element = document.querySelector('h1'); 
            return element.innerText;
        }''')
        # await page.waitForNavigation(waitUntil='networkidle0')
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
        print(f'Title:\n{title}')
        print(f'Body:\n{body}')
        await browser.close()
    
example = 'https://www.foxnews.com/politics/federal-judge-blocks-biden-administrations-asylum-policy-migrants'  

url_list = [
    example,
]

scraper = Scraper()

for url in url_list:
    asyncio.get_event_loop().run_until_complete(scraper.extract_body_text(url))

