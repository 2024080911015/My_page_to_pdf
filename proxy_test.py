import asyncio

from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def proxy_tset(url:str):
    async with Stealth().use_async(async_playwright() )as p:
        browser = await p.chromium.launch(headless=False,proxy={"server":"socks5://127.0.0.1:8080"})
        content=await browser.new_context(storage_state="cookies.json")
        page=await content.new_page()
        await page.goto(url=url,wait_until="networkidle",timeout=60000)
        input()
        browser.close()
async def main():
    await proxy_tset("https://www.zhihu.com")
if __name__ == '__main__':
    asyncio.run(main())

