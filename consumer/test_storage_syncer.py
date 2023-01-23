import pytest
from mockito import mock, when
from redis.client import Redis

from common.consts import REDIS_INDEX_LOCK_KEY
from common.models import CsvRowData
from common.storage import CsvStorage
from consumer.storage_syncer import StorageSyncer


@pytest.fixture
def storage() -> CsvStorage:
    return mock(CsvStorage)


@pytest.fixture
def cache() -> Redis:
    return mock(Redis)


@pytest.fixture
def csv_row_data() -> CsvRowData:
    return mock(CsvRowData)


@pytest.fixture
def storage_syncer(storage: CsvStorage, cache: Redis) -> StorageSyncer:
    return StorageSyncer(storage=storage, cache=cache)


@pytest.mark.asyncio
async def test_write_when_create_output_file_failed_then_raise_exception(storage_syncer: StorageSyncer,
                                                                         csv_row_data: CsvRowData) -> None:
    # arrange
    when(storage_syncer._storage).create_output_file().thenRaise(FileExistsError)

    # act + assert
    with pytest.raises(FileExistsError):
        await storage_syncer.write(row_index=0, csv_row_data=csv_row_data)


@pytest.mark.asyncio
async def test_write_when_cache_set_failed_then_raise_exception(storage_syncer: StorageSyncer,
                                                                csv_row_data: CsvRowData) -> None:
    # arrange
    when(storage_syncer._cache).set(REDIS_INDEX_LOCK_KEY, '0').thenRaise(Exception)

    # act + assert
    with pytest.raises(Exception):
        await storage_syncer.write(row_index=0, csv_row_data=csv_row_data)
