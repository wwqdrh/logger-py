"""
1、yaml配置
"""
import typing
import json
from configparser import ConfigParser
from pathlib import Path

import yaml
from pydantic import BaseSettings
from pydantic.env_settings import SettingsSourceCallable


class CustomSettingsSource:
    """
    自定义的配置文件来源基类
    """

    def __init__(self, path: Path):
        self.path = path

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(path={self.path!r})"


class JsonSettingsSource(CustomSettingsSource):
    """
    json文件来源导入配置项
    """

    def __call__(self, settings: BaseSettings) -> dict[str, typing.Any]:
        encoding = settings.__config__.env_file_encoding
        return json.loads(self.path.read_text(encoding))


class IniSettingsSource(CustomSettingsSource):
    """
    ini文件来源导入配置项
    """

    def __call__(self, settings: BaseSettings) -> dict[str, typing.Any]:
        encoding = settings.__config__.env_file_encoding
        parser = ConfigParser()
        parser.read(self.path, encoding)
        return getattr(parser, "_sections", {}).get("settings", {})


class YamlSettingsSource(CustomSettingsSource):
    """
    ini文件来源导入配置项
    """

    def __call__(self, settings: BaseSettings) -> dict[str, typing.Any]:
        encoding = settings.__config__.env_file_encoding
        return yaml.safe_load(self.path.read_text(encoding))


def NewSetting(datapath: Path, name: str, mode: str = ""):
    class SettingsBase(BaseSettings):
        """
        项目设置的基类
        """

        class Config:
            env_file = str(datapath / ".env")
            env_file_encoding = "utf-8"
            env_nested_delimiter = "__"

            @classmethod
            def customise_sources(
                cls,
                init_settings: SettingsSourceCallable,
                env_settings: SettingsSourceCallable,
                file_secret_settings: SettingsSourceCallable,
            ) -> tuple[SettingsSourceCallable, ...]:
                # 默认的设置
                default_settings = {
                    init_settings,
                    env_settings,
                    file_secret_settings,
                }

                json_file = datapath / f"{name}.json"
                if mode != "":
                    json_file = datapath / f"{name}.{mode}.json"
                if json_file.exists():
                    json_settings_source = JsonSettingsSource(json_file)
                    default_settings.add(json_settings_source)

                # ini配置文件
                ini_file = datapath / f"{name}.ini"
                if mode != "":
                    json_file = datapath / f"{name}.{mode}.ini"
                if ini_file.exists():
                    ini_settings_source = IniSettingsSource(ini_file)
                    default_settings.add(ini_settings_source)

                # yaml配置文件
                yaml_file = datapath / f"{name}.yaml"
                if mode != "":
                    json_file = datapath / f"{name}.{mode}.yaml"
                if yaml_file.exists():
                    yaml_settings_source = YamlSettingsSource(yaml_file)
                    default_settings.add(yaml_settings_source)

                return tuple(default_settings)

    return SettingsBase
