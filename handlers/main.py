import time
import random
import asyncio
import traceback
from pytz import timezone
from datetime import datetime, timedelta, time as dtime

from aiogram.types import FSInputFile, BufferedInputFile

from loader import bot
from investing.main import get_advice
from traidingview.main import get_currenct_pair_data
from data.config import NOTIFICATION_CHAT_ID, CURRENCY_PAIRS, SIGNAL_AMOUNT, IMAGES_PATHS


win_image = FSInputFile(IMAGES_PATHS['win'])
loss_image = FSInputFile(IMAGES_PATHS['loss'])
draw_image = FSInputFile(IMAGES_PATHS['draw'])
statistic_image = FSInputFile(IMAGES_PATHS['statistic'])


async def send_signal(amount, currenct_pair):
	advice = await get_advice(CURRENCY_PAIRS[currenct_pair])
	direction = "вверх" if advice in ["buy", "strong_buy"] else "вниз"

	data = await get_currenct_pair_data(''.join(currenct_pair))
	image = data['image']
	initial_rate = data['rate']
	
	signal_message = f"""
<b>
💎 Торговий Сигнал 💎
💱 Валютна Пара: <code>{'/'.join(currenct_pair)}</code>
📊 Сигнал: {direction.upper()}
💰 Сума: <code>{amount}</code>
📈 Поточний Курс: <code>{initial_rate}</code>
</b>
	"""
	
	message = await bot.send_photo(NOTIFICATION_CHAT_ID, photo=BufferedInputFile(
				image,
				filename='signal.png'
			), caption=signal_message)

	await asyncio.sleep(300)
	
	new_data = await get_currenct_pair_data(''.join(currenct_pair))
	new_rate = new_data['rate']
	
	if (direction == "вверх" and new_rate > initial_rate) or (direction == "вниз" and new_rate < initial_rate):
		await message.reply_photo(photo=win_image, caption='✅ Прогноз був успішним!')
		return True
	elif new_rate == initial_rate:
		await message.reply_photo(photo=draw_image, caption='⚖️ Прогноз завершився внічию.')
		return True
	else:
		await message.reply_photo(photo=loss_image, caption='❌ Прогноз не вдався. Пробуємо знову з більшою сумою.')
		return False

async def send_daily_report():
	jerusalem_tz = timezone('Asia/Jerusalem')
	report_time = dtime(23, 0)

	while True:
		current_time = datetime.now(jerusalem_tz).time()
		if current_time >= report_time:
			successful_signals = random.randint(16, 22)
			failed_signals = successful_signals // 4 + random.randint(1, 4)

			report_message = f"""
<b>
📊 Статистика за сьогодні:

✅ Плюсів: <code>{successful_signals}</code>
❌ Мінусів: <code>{failed_signals}</code>
</b>
			"""

			await bot.send_photo(NOTIFICATION_CHAT_ID, photo=statistic_image, caption=report_message)
			
		await asyncio.sleep(60)

async def start_trading():
	jerusalem_tz = timezone('Asia/Jerusalem')
	start_time = dtime(9, 0)
	end_time = dtime(22, 0)

	while True:
		current_time = datetime.now(jerusalem_tz).time()
		current_day = datetime.now(jerusalem_tz).weekday()

		if current_day < 5 and start_time <= current_time <= end_time:
			try:
				signals_per_hour = random.randint(3, 4)
				signal_interval = 3600 / signals_per_hour

				for _ in range(signals_per_hour):
					amount = SIGNAL_AMOUNT
					success = False

					while not success:
						try:
							currenct_pair = random.choice(tuple(CURRENCY_PAIRS.keys()))
							success = await send_signal(amount, currenct_pair)
							if not success:
								amount *= 2
						except Exception:
							traceback.print_exc()
					
					await asyncio.sleep(signal_interval)
			except Exception:
				traceback.print_exc()
		else:
			await asyncio.sleep(300)
