from loader import loop, bot

from data.config import *
from handlers.main import start_trading, send_daily_report

if __name__ == "__main__":

    print('Бот запущен!')

    loop.create_task(send_daily_report())
    loop.run_until_complete(start_trading())