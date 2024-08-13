import io
import asyncio
import traceback

from loader import browser_manager

async def navigate_to_chart(page, symbols):
    await page.goto(f'https://tradingview.com/chart/?symbol={symbols}')
    await page.wait_for_selector('xpath=/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]', timeout=5000)

async def open_pivot_points(page):
    await page.click('xpath=/html/body/div[2]/div[3]/div/div/div[3]/div[1]/div/div/div/div/div[4]/div/button')
    await page.click('xpath=//div[@data-value="5"]')
    await page.wait_for_timeout(1000)

async def capture_screenshot_to_bytes(page, element):
    screenshot = await element.screenshot()
    byte_stream = io.BytesIO(screenshot)
    byte_stream.seek(0)
    return byte_stream.getvalue()

async def get_text_from_selector(page, selector):
    element = await page.query_selector(selector)
    text = await element.inner_text()
    return text

async def execute_tradingview_analysis(symbols):
    page = await browser_manager.get_page()
    await navigate_to_chart(page, symbols)
    await open_pivot_points(page)

    element = await page.query_selector('body > div.js-rootresizer__contents.layout-with-border-radius > div.layout__area--center > div.chart-container.single-visible.top-full-width-chart.active > div.chart-container-border')
    screenshot_bytes = await capture_screenshot_to_bytes(page, element)

    rate_selector = 'body > div.js-rootresizer__contents.layout-with-border-radius > div.layout__area--right > div > div.widgetbar-pages > div.widgetbar-pagescontent > div.widgetbar-page.active > div.widget-X9EuSe_t.widgetbar-widget.widgetbar-widget-detail > div.widgetbar-widgetbody > div > div.wrapper-Tv7LSjUz > div.container-qWcO4bp9.widgetWrapper-BSF4XTsE.userSelectText-BSF4XTsE.offsetDisabled-BSF4XTsE > span.priceWrapper-qWcO4bp9 > span.highlight-maJ2WnzA.price-qWcO4bp9'
    rate = await get_text_from_selector(page, rate_selector)
    
    rate = float(rate)

    return dict(image=screenshot_bytes, rate=rate)

async def get_currenct_pair_data(symbols):
    while True:
        try:
            data = await execute_tradingview_analysis(symbols)
            break
        except Exception:
            traceback.print_exc()
            continue

    
    return data