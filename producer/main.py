import asyncio
import logging
from memphis import Memphis
from memphis.memphis import Producer, Headers

from common.consts import MEMPHIS_INDEX_HEADER
from common.models import CsvRowData, init_config
from common.storage import CsvStorage

LOGGER = logging.getLogger(__name__)


async def publish(storage: CsvStorage, producer: Producer) -> None:
    headers = Headers()
    for i, row in enumerate(storage.read()):
        headers.add(MEMPHIS_INDEX_HEADER, str(i))
        data = CsvRowData.from_named_tuple(row)
        message = data.to_bytearry()
        LOGGER.info(msg=f"--- produce ---\n index: {i}\n message: {message}\n headers: {str(headers.headers)}")
        await producer.produce(message=message, headers=headers)


async def main() -> None:
    config = init_config()
    storage = CsvStorage(filepath=config.csv_filepath,
                         headers=CsvRowData.get_fields())
    try:
        memphis = Memphis()
        await memphis.connect(host=config.memphis_host,
                              username=config.memphis_username,
                              connection_token=config.memphis_token)
        producer = await memphis.producer(station_name=config.memphis_station_name,
                                          producer_name=config.memphis_producer_name)
        await publish(storage=storage,
                      producer=producer)
    except Exception:
        raise
    finally:
        await memphis.close()


if __name__ == '__main__':
    asyncio.run(main())
