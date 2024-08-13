import json
import asyncio
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

class BrowserManager:
    def __init__(self):
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        self.playwright = None

    async def initialize(self, headless=True, add_cookies_status=True):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        
        if add_cookies_status:
            await self.add_cookies()

    async def add_cookies(self, cookies_path='data/cookies.txt'):
        try:
            with open(cookies_path, 'r') as cookies_file:
                cookies_list = json.loads(cookies_file.read())
                for cookie in cookies_list:
                    if cookie.get('sameSite') == 'unspecified':
                        cookie['sameSite'] = 'None'
                        if cookie['sameSite'] == 'None':
                            cookie['secure'] = True
                    try:
                        await self.context.add_cookies([cookie])
                    except Exception:
                        continue
        except FileNotFoundError:
            print("Cookies file not found. Proceeding without adding cookies.")

    async def close(self):
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def get_page(self) -> Page:
        if not self.browser:
            await self.initialize()
        return self.page

