import uuid

from sqlmodel import Field, SQLModel


class PlanetModel(SQLModel, table=True):

    """Planet model."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, unique=True)
    name: str = Field(max_length=50, unique=True, index=True)
    description: str
    icon: str
