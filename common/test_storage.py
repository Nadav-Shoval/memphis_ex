import os
import pytest

from csv import DictWriter
from dask import dataframe
from typing import List

from common.storage import CsvStorage


@pytest.fixture
def mock_csv_filepath() -> str:
    return "mock.csv"


@pytest.fixture
def templates() -> List:
    return [{"col1": "val11", "col2": "val12"},
            {'col1': "val21", 'col2': "val22"}]


@pytest.fixture
def headers() -> List:
    return ["col1", "col2"]


@pytest.fixture
def storage(mock_csv_filepath: str,
            templates: List,
            headers: List) -> CsvStorage:
    return CsvStorage(filepath=mock_csv_filepath,
                      headers=headers)


def test_read_when_happy_path_then_none(mock_csv_filepath: str,
                                        storage: CsvStorage,
                                        templates: List,
                                        headers: List) -> None:
    # arrange
    with open(mock_csv_filepath, 'w') as f:
        writer = DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for d in templates:
            writer.writerow(d)

    # act + assert
    for i, row in enumerate(storage.read()):
        assert row.col1 == templates[i]['col1']
        assert row.col2 == templates[i]['col2']

    # cleanup
    os.remove(mock_csv_filepath)


def test_create_output_file_when_file_is_not_exists_then_create(mock_csv_filepath: str,
                                                                storage: CsvStorage) -> None:
    # act
    storage.create_output_file()

    # assert
    assert os.path.exists(storage._filepath)

    # cleanup
    os.remove(mock_csv_filepath)


def test_create_output_file_when_file_is_exists_then_assert_no_headers(mock_csv_filepath: str,
                                                                       storage: CsvStorage,
                                                                       headers: List) -> None:
    # arrange
    with open(mock_csv_filepath, 'w'):
        pass

    # act
    storage.create_output_file()

    # assert
    with open(mock_csv_filepath, 'r') as f:
        assert f.read() == ""

    # cleanup
    os.remove(mock_csv_filepath)


def test_write_when_happy_path_then_none(mock_csv_filepath: str,
                                         storage: CsvStorage,
                                         templates: List,
                                         headers: List) -> None:
    # arrange
    with open(mock_csv_filepath, 'w') as f:
        writer = DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerow(templates[0])

    # act
    storage.write(dict_to_write=templates[1])

    # assert
    csv_dataframe = dataframe.read_csv(urlpath=mock_csv_filepath)
    for i, row in enumerate(csv_dataframe.itertuples()):
        assert row.col1 == templates[i]['col1']
        assert row.col2 == templates[i]['col2']

    # cleanup
    os.remove(mock_csv_filepath)
