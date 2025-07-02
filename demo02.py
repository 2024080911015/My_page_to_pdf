import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def vedio(url: str, output_path: str):
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.firefox.launch(
            headless=False,
            # Firefox不需要Chrome的启动参数
            firefox_user_prefs={
                'media.autoplay.default': 0,  # 允许自动播放
                'media.autoplay.blocking_policy': 0,  # 禁用自动播放阻止
                'media.volume_scale': '1.0',  # 设置音量
                'media.eme.enabled': True,  # 启用加密媒体扩展
                'media.gmp-manager.updateEnabled': True  # 启用GMP更新
            }
        )
        content = await browser.new_context(
            storage_state="cookies_bilibili.json",
            record_video_dir="D:/My_page_to_pdf/",  # 视频保存目录
            record_video_size={"width": 1280, "height": 720}
            # 移除权限设置，因为playwright-stealth不支持
        )
        page = await content.new_page()
        
        # 注入JavaScript来强制启用HTML5播放器
        await page.add_init_script("""
            // 隐藏webdriver特征
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            // 强制启用HTML5播放器
            Object.defineProperty(HTMLMediaElement.prototype, 'canPlayType', {
                value: function(type) {
                    if (type.includes('mp4') || type.includes('webm') || type.includes('flv')) {
                        return 'probably';
                    }
                    return 'maybe';
                }
            });
        """)
        
        await page.goto(url, wait_until="networkidle", timeout=60000)
        
        # 等待页面加载
        await page.wait_for_timeout(5000)
        
        # 等待视频开始播放
        await page.wait_for_timeout(9000)
        await page.screenshot(path=output_path)
        await browser.close()

async def main():
    await vedio(
        url="https://www.bilibili.com/video/BV1SfK9zPEL3/?spm_id_from=333.1007.tianma.13-2-48.click",
        output_path="D:/My_page_to_pdf/test.png"
    )

if __name__ == "__main__":
    asyncio.run(main())





