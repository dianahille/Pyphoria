import uuid
from dataclasses import Field

from models import StrictBaseModel


class PlanetModel(StrictBaseModel):

    """Planet model."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    description: str
    icon: str
