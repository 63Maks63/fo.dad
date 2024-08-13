import asyncio

from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties

from traidingview.browser import BrowserManager
from data.config import *


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))

browser_manager = BrowserManager()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)