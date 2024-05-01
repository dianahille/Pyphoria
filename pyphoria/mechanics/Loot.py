import uuid  # noqa: N999, D100
from typing import Self

import pyphoria


class Loot:
    def __init__(self: Self) -> None:
        """Loot should be considered temporary and should be bound short term to a specific character.
        It will not be stored in the database. The loot will be none to many items.
        Planet and Monster type will be used to determine the possible implicit of the base as well as well as possible stats of the items.
        Character level will be used to determine the minimum item level. While the monster level will be used to determine the maximum item level.
        The item level will be used to determine the tier of stats that can be rolled on the item.
        A stat tier will be used to determine the range of the stat that can be rolled on the item.
        Weighting of stat tier will slide to favor the higher tier stats, but will still allow for lower tier stats to be rolled.
        The monster level may prevent some items from dropping.
        Unique items will not be affected by the character level but only the monster level.
        """
        pass

    def generate(
        self: Self,
        character_id: uuid.UUID,
        planet_id: uuid.UUID,
        monster_type: str,
        monster_level: int,
    ) -> None:
        """Generate loot for the character."""
        pass
