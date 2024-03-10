from pydantic import ConfigDict
from sqlmodel import SQLModel


class StrictBaseModel(SQLModel):
    class Config(ConfigDict):
        strict = True
