import uuid

from models import StrictBaseModel


class PlanetModel(StrictBaseModel):

    """Planet model."""

    id: uuid.UUID
    name: str
    description: str
    icon: str
