import datetime
import os
import shutil
import pytest

from pykit.logger import BasicLogger


@pytest.fixture(scope="session")
def delete_logs_dir():
    yield
    if os.path.exists("logs"):
        shutil.rmtree("logs")
    if os.path.exists("test_dir"):
        shutil.rmtree("test_dir")
    if os.path.exists("test_parent_dir"):
        shutil.rmtree("test_parent_dir")
    print("Logs directories deleted")


@pytest.fixture(scope="session")
def current_date() -> str:
    return datetime.datetime.today().strftime("%Y-%m-%d")


@pytest.fixture(scope="function")
def test_logger() -> BasicLogger:
    return BasicLogger.get_logger(level=1)
