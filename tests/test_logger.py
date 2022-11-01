from pathlib import Path

import pytest

from wwqdrh.logger import setup_logger

testdata = Path(__file__).parents[0] / "testdata"

def test_logger_output():
    ll = setup_logger(str(testdata/"log"/"basic.log"))
    ll.info("this is a info message")
    ll.debug("this is a debug message")
    ll.warning("this is a warning message")
    ll.error("this is a error message")
