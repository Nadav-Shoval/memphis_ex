import asyncio
import logging
from memphis import Memphis
import os
import redis.asyncio as redis

from common.consts import MEMPHIS_INDEX_HEADER, OUTPUT_FILENAME, REDIS_HOST_DEFAULT_VALUE, REDIS_HOST_ENV_KEY, \
    REDIS_PORT
from common.models import CsvRowData, init_config
from common.storage import CsvStorage
from storage_syncer import StorageSyncer

CONFIG = init_config()
CONFIG.csv_filepath = os.environ.get('CSV_FILEPATH', OUTPUT_FILENAME)  # PATCH

LOGGER = logging.getLogger(__name__)


async def msg_handler(msgs, error):
    storage = CsvStorage(filepath=CONFIG.csv_filepath,
                         headers=CsvRowData.get_fields())
    redis_host = os.environ.get(REDIS_HOST_ENV_KEY, REDIS_HOST_DEFAULT_VALUE)
    cache = redis.Redis(host=redis_host, port=REDIS_PORT)
    storage_syncer = StorageSyncer(storage=storage, cache=cache)
    try:
        for msg in msgs:
            await msg.ack()  # TODO: move down?
            headers = msg.get_headers()
            row_index = int(headers.get(MEMPHIS_INDEX_HEADER))
            data = msg.get_data()
            csv_row_data = CsvRowData.from_bytearry(data=data)
            LOGGER.info(
                msg=f"--- consume ---\n index: {row_index}\n csv_row_data: {csv_row_data}\n headers: {str(headers)}")
            await storage_syncer.write(row_index=row_index,
                                       csv_row_data=csv_row_data)
            if error:
                print(error)
    except Exception as e:
        print(e)
        return


async def main():
    try:
        memphis = Memphis()
        await memphis.connect(host=CONFIG.memphis_host,
                              username=CONFIG.memphis_username,
                              connection_token=CONFIG.memphis_token)
        consumer = await memphis.consumer(station_name=CONFIG.memphis_station_name,
                                          consumer_name=CONFIG.memphis_consumer_name,
                                          consumer_group=CONFIG.memphis_consumer_group_name)
        consumer.consume(msg_handler)
        await asyncio.Event().wait()
    except Exception as e:
        print(e)
    finally:
        await memphis.close()


if __name__ == '__main__':
    asyncio.run(main())
