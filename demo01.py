import asyncio
import time
import os

from openpyxl.styles.builtins import output, title
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
import smtplib
from email.mime.text import MIMEText


from email.mime.multipart import MIMEMultipart
async def my_page_to_pdf(url:str,output_path:str):
    async with Stealth().use_async(async_playwright()) as p:
        browse=await p.chromium.launch(headless=True)
        content=await browse.new_context(storage_state="cookies.json")
        page =await content.new_page()
        await page.goto(url,wait_until="networkidle",timeout=60000)
        await page.wait_for_timeout(3000)
        await page.pdf(path=output_path,format="A4")
        await browse.close()
async def send_email(attch_Path_str):
    mail_host = "smtp.163.com"
    mail_user = "13271706128@163.com"
    mail_pass = "QJwSVii9cGCxkTae"
    sender=mail_user
    recevier="2830274223@qq.com"
    attch_Path=attch_Path_str
    msg=MIMEMultipart()
    msg["from"]=sender
    msg["to"]=recevier
    msg["subject"]="test"
    with open(attch_Path,"rb") as f:
        attch=MIMEText(f.read(),"base64","utf-8")
        attch["Content-Type"]="application/octet-stream"
        attch["Content-Disposition"]="attachment;filename="+attch_Path
        msg.attach(attch)
    with smtplib.SMTP_SSL(mail_host,465) as sever:
        sever.login(mail_user,mail_pass)
        sever.send_message(msg)

async def get_favorite_pages(url:str):
    async with Stealth().use_async(async_playwright()) as p:
        browser=await p.chromium.launch(headless=True)
        content=await browser.new_context(storage_state="cookies.json")
        page=await content.new_page()
        await page.goto(url,wait_until="networkidle",timeout=60000)
        await page.wait_for_timeout(3000)
        last_height=await page.evaluate("document.body.scrollHeight")
        while True:
            await page.evaluate("window.scrollTo(0,document.body.scrollHeight)")
            await page.wait_for_timeout(3000)
            new_height=await page.evaluate("document.body.scrollHeight")
            if new_height ==last_height:
                break
            last_height=new_height
        link_locators=page.locator("h2.ContentItem-title a")
        count =await link_locators.count()
        if count==0:
            print("c错误")
        all_links=[]
        for i in range(count):
            locator=link_locators.nth(i)
            title=await locator.inner_text()
            links=await locator.get_attribute("href")
            if links.startswith("//"):
                links="https:"+links
            all_links.append({"title":title,"links":links})
        return all_links

async def main():
    time=os.times()
    url="https://www.zhihu.com/collection/967495634"
    all_links=await get_favorite_pages(url)
    for i,item in enumerate(all_links):
        title=item["title"]
        link=item["links"]
        output_path = "C:/Users/iiijj/Desktop/My_page_to_pdf/" + str(i) + ".pdf"
        await my_page_to_pdf(link,output_path)
        print("已经完成第"+str(i+1)+"个任务")
    print("完成")



if __name__=="__main__":
    asyncio.run(main())