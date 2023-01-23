import logging
import os
from csv import DictWriter  # https://stackoverflow.com/questions/63324327/write-a-csv-file-asynchronously-in-python
from dask import dataframe  # python -m pip install "dask[dataframe]" --upgrade
from typing import Iterable, Dict, List

LOGGER = logging.getLogger(__name__)


class CsvStorage:

    def __init__(self, filepath: str, headers: List) -> None:
        self._filepath = filepath
        self._headers = headers

    def create_output_file(self) -> None:
        if not os.path.exists(self._filepath):
            with open(self._filepath, 'w') as f:
                writer = DictWriter(f, fieldnames=self._headers)
                writer.writeheader()

    def read(self) -> Iterable:
        csv_dataframe = dataframe.read_csv(urlpath=self._filepath)
        return csv_dataframe.itertuples()

    def write(self, dict_to_write: Dict):
        with open(self._filepath, 'a') as f:
            writer = DictWriter(f, fieldnames=self._headers)
            writer.writerow(dict_to_write)
