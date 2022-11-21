import os
import datetime
import sys
from typing import List, Any

from loguru import logger as default_logger
from loguru._logger import Logger


class BasicLogger:
    def __init__(
        self,
        logger: "Logger" = default_logger,
        parent_dir: str = "",
        logs_dir: str = "logs",
        date_dir: bool = True,
        serialize: bool = False,
        level: int = 1,
    ):
        parent_dir = parent_dir if parent_dir else os.getcwd()
        self._LOGGING_DIRECTORY: str = os.path.join(parent_dir, logs_dir)
        if date_dir:
            current_date = datetime.datetime.today().strftime("%Y-%m-%d")
            self._LOGGING_DIRECTORY = os.path.join(
                self._LOGGING_DIRECTORY, current_date
            )
        self.serialize = serialize
        self._LOGGING_LEVEL = level
        self.levels: List[dict] = []
        self._logger: "Logger" = logger

    @classmethod
    def get_logger(
        cls,
        level: int = 20,
        parent_dir: str = "",
        logs_dir: str = "logs",
        add_date_dir: bool = True,
        serialize_errors: bool = False,
    ):
        return (
            cls(
                level=level,
                parent_dir=parent_dir,
                logs_dir=logs_dir,
                date_dir=add_date_dir,
                serialize=serialize_errors,
            )
            .get_default()
            .get_new_logger()
        )

    @property
    def logger(self) -> "Logger":
        return self._logger

    def add_level(
        self, name: str, color: str = "<white>", no: int = 0, log_filename: str = ""
    ):
        """Add new logging level to loguru.logger config
        :param name - logging level name
        :param color  - color for logging level
        :param no - minimal logging level
        :param log_filename - filename for current level
        """

        if not log_filename:
            log_filename = f"{name}.log".lower()
        level_data: dict = {
            "config": {"name": name, "color": color},
            "path": os.path.join(self._LOGGING_DIRECTORY, log_filename),
        }
        if no:
            level_data["config"].update(no=no)
        if not self._is_level_exists(name):
            self._logger.configure(levels=[level_data["config"]])
        self.levels.append(level_data)

    def _is_level_exists(self, name: str) -> bool:
        level_names = tuple(
            level.get("config", {}).get("name") for level in self.levels
        )
        return name in level_names

    def add_logger(self, **kwargs):
        """Add new logging settings to loguru.logger
        :param level int | str - logging level (level=5 or level="DEBUG")
        :param sink - interace for logging out (filepath, stdout, etc),
            default: 'parent_dir/logs/date_dir/"level_name".log
        :param: More read loguru docs
        """

        level: int | str = kwargs.get("level", self._LOGGING_LEVEL)
        sink: Any = kwargs.get("sink")
        if not sink:
            sink = tuple(
                elem for elem in self.levels if elem["config"]["name"] == level
            )[0]["path"]
            kwargs.update(sink=sink)
        self.logger.add(**kwargs)

    def log(self, *args, **kwargs):
        return self.logger.log(*args, **kwargs)

    def trace(self, *args, **kwargs):
        return self.logger.trace(*args, **kwargs)

    def catch(self, *args, **kwargs):
        return self.logger.catch(*args, **kwargs)

    def info(self, text, *args, **kwargs):
        return self.logger.info(text, *args, **kwargs)

    def debug(self, text, *args, **kwargs):
        return self.logger.debug(text, *args, **kwargs)

    def error(self, text, *args, **kwargs):
        return self.logger.error(text, *args, **kwargs)

    def warning(self, text, *args, **kwargs):
        return self.logger.warning(text, *args, **kwargs)

    def success(self, text, *args, **kwargs):
        return self.logger.success(text, *args, **kwargs)

    def exception(self, text, *args, **kwargs):
        return self.logger.exception(text, *args, **kwargs)

    def get_new_logger(self) -> "Logger":
        """Returns updated loguru.logger instance"""

        return self._logger

    def get_default(self) -> "BasicLogger":
        """Returns self instance with default settings"""

        self._logger.remove()
        self.add_level("DEBUG", "<white>")
        self.add_level("INFO", "<fg #afffff>")
        self.add_level("WARNING", "<light-yellow>")
        self.add_level("ERROR", "<red>")
        self.add_logger(sink=sys.stdout, level="DEBUG")
        self.add_logger(enqueue=True, level="WARNING", rotation="50 MB")
        self.add_logger(enqueue=True, level="ERROR", rotation="50 MB")
        if self.serialize:
            self.add_logger(
                enqueue=True, level="ERROR", rotation="50 MB", serialize=True
            )

        return self
