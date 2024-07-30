from __future__ import annotations
import asyncio
import aiohttp


# self.__proxy = 'http://user130949:fduqey@185.137.15.218:5771'
# self.__proxy = 'https://141.94.17.33:22222'

class RequestAiohttp:
    def __init__(
            self, session: aiohttp.ClientSession,
            method, url, cookies, headers, data=None, params=None, proxy=None
    ):
        self.__cookies = cookies
        self.__headers = headers
        self.__method: str = method
        self.__url: str = url
        self.__params = params
        self.__data: dict = data
        self.__proxy = proxy
        self.__session = session

    async def __request_async(self):
        if self.__method.lower() == 'post':
            return await self.__session.post(
                url=self.__url, params=self.__params, cookies=self.__cookies,
                headers=self.__headers, data=self.__data, proxy=self.__proxy
            )
        elif self.__method.lower() == 'get':
            return await self.__session.get(
                url=self.__url, params=self.__params, cookies=self.__cookies,
                headers=self.__headers, data=self.__data, proxy=self.__proxy
            )

    async def get_data_server(self):
        response: None | aiohttp.client.ClientResponse = None
        count_server_disconnected = 0
        count_connection_reset_error = 0
        count_no_200 = 0

        while True:
            try:
                response = await self.__request_async()

            except aiohttp.ServerDisconnectedError:
                count_server_disconnected += 1
                print({"error": f"[{count_server_disconnected}] Server Disconnected Error"})
                if count_server_disconnected >= 2: return 501
                await asyncio.sleep(10)
                continue
            except OSError:
                count_connection_reset_error += 1
                print({"error": f"[{count_connection_reset_error}] Connection Reset Error"})
                if count_connection_reset_error >= 2: return 502
                await asyncio.sleep(10)
                continue

            if response.status == 200:
                break
            elif response.status == 400:
                break
            elif response.status == 429:
                return 429
            elif response.status == 405:
                return 405
            elif response.status == 403:
                return 403
            elif response.status == 402:
                return 402
            else:
                await asyncio.sleep(5)
                count_no_200 += 1
                if count_no_200 == 3:
                    print({"error": f"Response Status {response.status}"})
                    break

        # print(f"Content Type: {response.content_type}")
        if response.content_type == 'text/html':
            data_server = await response.text()
            content_type = 'html'
        else:
            data_server = await response.json()
            content_type = 'json'

        return data_server

    async def session_close(self):
        await self.__session.close()
# ==================================================================================================================== #
