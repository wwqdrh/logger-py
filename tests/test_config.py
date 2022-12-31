import os
import pathlib
import typing

import pydantic

from pykit.configer import NewSetting


def test_env_config() -> None:
    os.environ.setdefault("pykit.name", "env_pykit")
    os.environ.setdefault("pykit.app.port", "7000")

    sett = NewSetting(pathlib.Path(__file__).parents[0] / "testdata", "config")

    class App(pydantic.BaseModel):
        port: int

    class Conf(sett):  # type: ignore
        app: App
        name: str

    conf = Conf()

    print(conf.name, conf.app.port)
