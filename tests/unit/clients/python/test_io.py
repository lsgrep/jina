from pathlib import Path

import numpy as np
import pytest

from jina.clients.python import PyClient
from jina.clients.python.io import input_files, input_lines, input_numpy


@pytest.fixture(scope='function')
def filepath(tmpdir):
    input_filepath = Path(tmpdir) / 'input_file.csv'
    with open(input_filepath, 'w') as input_file:
        input_file.writelines(["1\n", "2\n", "3\n"])
    return input_filepath


def test_input_lines_with_filepath(filepath):
    result = list(input_lines(filepath=filepath, size=2))
    assert len(result) == 2
    assert result[0] == "1\n"
    assert result[1] == "2\n"


def test_input_lines_with_lines():
    lines = ["1", "2", "3"]
    result = list(input_lines(lines=lines, size=2))
    assert len(result) == 2
    assert result[0] == "1"
    assert result[1] == "2"


def test_input_lines_with_empty_filepath_and_lines():
    with pytest.raises(ValueError):
        lines = input_lines(lines=None, filepath=None)
        for _ in lines:
            pass


@pytest.mark.parametrize(
    'patterns, recursive, size, sampling_rate, read_mode',
    [
        ('*.*', True, None, None, None),
        ('*.*', False, None, None, None),
        ('*.*', True, 2, None, None),
        ('*.*', True, 2, None, 'rb'),
        ('*.*', True, None, 0.5, None),
    ]
)
def test_input_files(patterns, recursive, size, sampling_rate, read_mode):
    PyClient.check_input(
        input_files(
            patterns=patterns,
            recursive=recursive,
            size=size,
            sampling_rate=sampling_rate,
            read_mode=read_mode
        )
    )


def test_input_files_with_invalid_read_mode():
    with pytest.raises(RuntimeError):
        PyClient.check_input(input_files(patterns='*.*', read_mode='invalid'))


@pytest.mark.parametrize('array', [np.random.random([100, 4, 2]), ['asda', 'dsadas asdasd']])
def test_input_numpy(array):
    PyClient.check_input(input_numpy(array))
