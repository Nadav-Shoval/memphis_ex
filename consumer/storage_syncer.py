import redis.asyncio as redis
from time import sleep

from common.consts import REDIS_INDEX_LOCK_KEY, CONSUMER_SLEEP_TIME
from common.models import CsvRowData
from common.storage import CsvStorage


class StorageSyncer:
    def __init__(self, storage: CsvStorage, cache: redis.Redis) -> None:
        self._storage = storage
        self._cache = cache

    async def write(self, row_index: int, csv_row_data: CsvRowData) -> None:
        if row_index == 0:
            self._storage.create_output_file()
            await self._cache.set(REDIS_INDEX_LOCK_KEY, '0')
        await self._lock(row_index=row_index)
        self._storage.write(dict_to_write=csv_row_data.to_dict())
        await self._release(row_index=row_index)

    async def _lock(self, row_index: int) -> None:
        while row_index != int(await self._cache.get(REDIS_INDEX_LOCK_KEY)):
            sleep(CONSUMER_SLEEP_TIME)

    async def _release(self, row_index: int) -> None:
        await self._cache.set(REDIS_INDEX_LOCK_KEY, str(row_index + 1))
