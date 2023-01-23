import json
import logging
import os
from dataclasses import dataclass, fields
from typing import NamedTuple, Dict

logging.basicConfig()  # TODO: add format
logging.root.setLevel(logging.INFO)


@dataclass
class CsvRowData:
    first_name: str
    last_name: str
    age: int

    @staticmethod
    def get_fields():
        return [field.name for field in fields(CsvRowData)]

    @classmethod
    def from_named_tuple(cls, named_tuple: NamedTuple) -> 'CsvRowData':
        return cls(first_name=named_tuple.first_name,
                   last_name=named_tuple.last_name,
                   age=named_tuple.age)

    @classmethod
    def from_bytearry(cls, data: bytearray) -> 'CsvRowData':
        decoded_data = data.decode('utf8').replace("'", '"')
        jsn = json.loads(decoded_data)
        return cls(first_name=jsn.get('first_name', ''),
                   last_name=jsn.get('last_name', ''),
                   age=int(jsn.get('age', '-1')))

    def to_dict(self) -> Dict:
        return {'first_name': self.first_name,
                'last_name': self.last_name,
                'age': self.age}

    def to_bytearry(self) -> bytearray:
        return bytearray(str(self.to_dict()), 'utf-8')


@dataclass
class MemphisConfig:
    csv_filepath: str = "../common/csv_example.csv"
    memphis_host: str = "localhost:6666/"
    memphis_username: str = "root"
    memphis_token: str = "memphis"
    memphis_station_name: str = "local_station"
    memphis_producer_name: str = "local_producer"
    memphis_consumer_name: str = "local_consumer"
    memphis_consumer_group_name: str = "local_consumer_group"


def init_config() -> MemphisConfig:
    config = MemphisConfig()
    config.csv_filepath = os.environ.get('CSV_FILEPATH', config.csv_filepath)
    config.memphis_host = os.environ.get('MEMPHIS_HOST', config.memphis_host)
    config.memphis_username = os.environ.get('MEMPHIS_USERNAME', config.memphis_username)
    config.memphis_token = os.environ.get('MEMPHIS_TOKEN', config.memphis_token)
    config.memphis_station_name = os.environ.get('MEMPHIS_STATION_NAME', config.memphis_station_name)
    config.memphis_producer_name = os.environ.get('MEMPHIS_PRODUCER_NAME', config.memphis_producer_name)
    config.memphis_consumer_name = os.environ.get('HOSTNAME', config.memphis_consumer_name)
    config.memphis_consumer_group_name = os.environ.get('MEMPHIS_CONSUMER_GROUP_NAME',
                                                        config.memphis_consumer_group_name)

    return config
