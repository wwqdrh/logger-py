import os
import sys
import logging

from loguru import logger as ll

VERSION = 0.1

ll.remove(0)

# 设置输出路径

ll.add(
    sys.stderr,
    format="<red>[{level}] | {extra[ip]} |</red> Message : <green>{message}</green> @ {time}",
    colorize=True,
)

ll.add("out.log")

ll.add("file_1.log", rotation="500 MB")    # Automatically rotate too big file
ll.add("file_2.log", rotation="12:00")     # New file is created each day at noon
ll.add("file_3.log", rotation="1 week")    # Once the file is too old, it's rotated

ll.add("file_X.log", retention="10 days")  # Cleanup after some time

ll.add("file_Y.log", compression="zip")    # Save some loved space

context_logger = ll.bind(ip="192.168.0.1") # add some addtion key

ll.success("Successfully changed format")


ll.remove(0)
ll.add("out.log", backtrace=True, diagnose=True)

def func(a, b):
  return (a / b) + func(a, b-1)

def nested(c):
    try:
        func(5, c)
    except ZeroDivisionError:
        ll.exception("Division by zero error!")

nested(2)


ll.remove(0)
ll.add(sys.stderr, format = "<green>{message}</green>", colorize = True)                      # Green font colour
ll.add(sys.stderr, format = "<r>{message}</r>", colorize = True)                              # Red font colour, using abbreviations
ll.add(sys.stderr, format = "<Y>{message}</Y>", colorize = True)                              # Yellow Bankground colours
ll.add(sys.stderr, format = "<fg 128,128,128>{message}</fg 128,128,128>", colorize = True)    # RBG color
ll.add(sys.stderr, format = "<fg 128,128,128><u><i>{message}</i></u></fg 128,128,128>", colorize = True)    #Styling

ll.info("test")



ll.remove()
ll.add(sys.stderr, format = "{time} | <lvl>{level}</lvl> {level.icon} | <lvl>{message}</lvl>", colorize = True)

new_level = ll.level("SNAKY", no=38, color="<yellow>", icon="🐍")

ll.log("SNAKY", "Here we go!")



@ll.catch
def my_function(x, y, z):
    # An error? It's caught anyway!
    return 1 / (x + y + z)

# campatiable standard logging
# handler = logging.handlers.SysLogHandler(address=('localhost', 514))
# ll.add(handler)

class PropagateHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger(record.name).handle(record)

ll.add(PropagateHandler(), format="{message}")

class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists.
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        ll.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)