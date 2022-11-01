import os
import sys
import logging

from loguru import logger as ll

def setup_logger(f: str, rotation: str = "00:00"):
    """Set up stderr logging format.

    f: 输出日志路径
    rotation: 归档，"12:00" ｜ "500 MB" "1 week"
    """
    ll.remove()  # Remove the default setting

    # Set up the preferred logging colors and format unless overridden by its environment variable
    ll.level("INFO", color=os.environ.get("LOGURU_INFO_COLOR") or "<white>")
    ll.level("DEBUG", color=os.environ.get("LOGURU_DEBUG_COLOR") or "<d><white>")
    log_format = os.environ.get("LOGURU_FORMAT") or (
        # "<green>{time:YYYY-MM-DD HH:mm:ss}</green> "
        "<b><level>{level: <8}</level></b> "
        "| <level>{message}</level>"
    )
    ll.add(sys.stderr, format=log_format)
    ll.add(f, rotation=rotation)
    # By default all the logging messages are disabled
    ll.enable("charger") 
    return ll