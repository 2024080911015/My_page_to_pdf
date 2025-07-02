import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser=await p.firefox.launch(headless=False)
        content=await browser.new_context()
        page=await content.new_page()
        await page.goto(url="https://www.bilibili.com")
        input()
        cookies_bilibili=await content.storage_state(path="cookies_bilibili.json")
        await browser.close()
if __name__=="__main__":
    asyncio.run(main())
