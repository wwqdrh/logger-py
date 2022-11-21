from pathlib import Path
import datetime, os

from loguru import logger

from wwqdrh.logger import setup_logger, BasicLogger


testdata = Path(__file__).parents[0] / "testdata"


def test_logger_output():
    ll = setup_logger(str(testdata / "log" / "basic.log"))
    ll.info("this is a info message")
    ll.debug("this is a debug message")
    ll.warning("this is a warning message")
    ll.error("this is a error message")


def test_set_log_level(current_date):
    test_logger = BasicLogger.get_logger(level=1)
    test_logger.debug("Test")
    assert not os.path.exists(f"./logs/{current_date}/debug.log")
    test_logger.info("Test")
    test_logger.warning("Test")
    assert os.path.exists(f"./logs/{current_date}/warning.log")
    test_logger.error("Test")
    assert os.path.exists(f"./logs/{current_date}/error.log")


def test_my_logger(delete_logs_dir, test_logger):
    assert test_logger.log("INFO", "test log") is None
    assert test_logger.info("test info") is None
    assert test_logger.warning("test warning") is None
    assert test_logger.debug("test debug") is None
    assert test_logger.error("test error") is None
    assert test_logger.success("test success") is None
    assert test_logger.exception("test exception") is None


def test_my_logger_with_another_logs_dir(delete_logs_dir):
    logger_test = (
        BasicLogger(logger, logs_dir="test_dir").get_default().get_new_logger()
    )
    logger_test.error("test")
    assert os.path.exists("test_dir")


def test_my_logger_with_another_parent_dir(delete_logs_dir):
    logger_test = (
        BasicLogger(logger, parent_dir="test_parent_dir").get_default().get_new_logger()
    )

    logger_test.error("test")
    assert os.path.exists("test_parent_dir")


def test_my_logger_without_date_dir(delete_logs_dir, test_logger):
    logger_test = BasicLogger(logger, date_dir=False).get_default().get_new_logger()
    logger_test.error("test")
    assert not os.path.exists(datetime.datetime.today().strftime("%Y-%m-%d"))


def test_my_logger_default_log_level(delete_logs_dir, test_logger):
    logger_test = BasicLogger(logger, level=1).get_default().get_new_logger()
    assert logger_test.error("test") is None
