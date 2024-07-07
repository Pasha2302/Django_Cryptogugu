import aiohttp

from api_dexscreener.Tools import toolbox
from api_dexscreener.module_aiorequest import RequestAiohttp

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'origin': 'https://coinpaprika.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://coinpaprika.com/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}


async def get_contract(search: str='ICECOIN'):
    url = f'https://api.coinpaprika.com/v1/search/?q={search}&c=currencies,icos,people,exchanges,tags&limit=250'
    async with toolbox.AiohttpSession(limit=5, total=600).create_session() as session:
        session: aiohttp.ClientSession
        req = RequestAiohttp(
            session=session, method='get', url=url, headers=headers, cookies=None, proxy='https://141.94.17.33:22222',
        )
        data_server = await req.get_data_server()

    print(f"\n{data_server=}")

