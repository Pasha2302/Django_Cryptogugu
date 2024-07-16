import re

from cryptogugu.api_coins_data.Tools import toolbox
from UseDB.async_mysql_database import AsyncMySQLManager

USE_DB = "coinmooner"
PATH_CONFIG = '/home/pavelpc/PycharmProjects/Working_Projects/Django_Cryptogugu/UseDB/db_config/db_config_local.json'
db_config_mooner_local = toolbox.download_json_data(path_file=PATH_CONFIG)


class CoinmoonerDB:
    db_coinmooner = AsyncMySQLManager(db_config_mooner_local, use_db=USE_DB)


    async def search_coin(self, name, symbol=None) -> list[dict]:
        query = f"SELECT * FROM coin WHERE name='{name}'"
        if symbol: query += f" AND symbol='{symbol}'"

        result = await self.db_coinmooner.execute_query(query=query, fetch=True)
        if result and self.is_valid_address(address=result[0]['contractAddress']): print("\nValid address: True")
        return result


    async def show_table(self, tables: list[str], columns: list[str] = None, limit: int = None):
        await self.db_coinmooner.show_table_data(tables, columns, limit)


    @staticmethod
    def show_coins(coins: list[dict]):
        print(f"Записей найдено: {len(coins)}")
        for coin in coins:
            for k, v in coin.items():
                print(f"{k}:  {v}")
            print('--' * 40)
        print('==' * 40)


    @staticmethod
    def is_valid_address(address):
        """
        Проверяет, является ли адрес корректным адресом контракта в сети BSC.
        """
        pattern = re.compile(r'^0x[a-fA-F0-9]{40}$')
        return bool(pattern.match(address))

    async def connect(self):
        await self.db_coinmooner.connect()

    async def disconnect(self):
        await self.db_coinmooner.disconnect()


async def main():
    db_coinmooner = CoinmoonerDB()

    try:
        await db_coinmooner.connect()
        await db_coinmooner.show_table(tables=['mainCoin',], limit=10)
        # db_coinmooner.show_coins( await db_coinmooner.search_coin(name='BTC') )
    finally:
        await db_coinmooner.disconnect()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
