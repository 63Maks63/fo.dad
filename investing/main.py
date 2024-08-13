import aiohttp
import asyncio

async def get_advice(currency_pair, period='5m'):
    url = f'https://api.investing.com/api/financialdata/technical/analysis/{currency_pair}/{period}'
    headers = {
        "authority": "api.investing.com",
        "method": "OPTIONS",
        "path": f"/api/financialdata/technical/analysis/{currency_pair}/{period}",
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru,en;q=0.9",
        "access-control-request-headers": "content-type,domain-id",
        "access-control-request-method": "GET",
        "origin": "https://ru.investing.com",
        "priority": "u=1, i",
        "referer": "https://ru.investing.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
    }
    
    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36"}) as session:
        async with session.get(url, headers=headers) as response:
            text = await response.json()
            return text['summary']