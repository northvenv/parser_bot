import asyncpg

class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_data(self, user_id, user_name, coins):
        query = f"INSERT INTO data_users (user_id, user_name, coins) VALUES ({user_id}, '{user_name}', {coins}) \
                ON CONFLICT (user_id) DO UPDATE SET user_name='{user_name}'"
        await self.connector.execute(query)

    # async def coins_count(self, coins):







