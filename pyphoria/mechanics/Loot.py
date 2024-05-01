import uuid  # noqa: N999, D100
from typing import Self

import pyphoria
import random


class Loot:
    def __init__(
        self: Self,
        planet_id: uuid.UUID,
        area_id: uuid.UUID,
    ) -> None:
        """Loot should be considered temporary and should be bound short term to a specific character.
        It will not be stored in the database. The loot will be none to many items.
        Planet, Area and Monster type will be used to determine the possible implicit of the base as well as well as possible stats of the items.
        Character level will be used to determine the minimum item level. While the monster level will be used to determine the maximum item level.
        The item level will be used to determine the tier of stats that can be rolled on the item.
        A stat tier will be used to determine the range of the stat that can be rolled on the item.
        Weighting of stat tier will slide to favor the higher tier stats, but will still allow for lower tier stats to be rolled.
        The monster level may prevent some items from dropping.
        Unique items will not be affected by the character level but only the monster level.
        """
        self._load_loot_pool(planet_id, area_id)

    def _load_loot_pool(self: Self, planet_id: uuid.UUID, area_id: uuid.UUID) -> None:
        """Load the loot pool for the area."""
        # load the area loot pool list
        self.area_loot_pool = pyphoria.models.AreaLootPool.load(planet_id, area_id)
        pass

    def generate(
        self: Self,
        character_id: uuid.UUID,
        monster_id: uuid.UUID,
        monster_level: int,
    ) -> None:
        """Generate loot for the character."""
        # TODO: save the loot temporarily in some way
        # load the character and character specific modifiers
        character = pyphoria.models.Character.load(character_id)
        character_level = character["level"]
        # character specific percentage modifiers
        character_loot_chance_modifier = character.get("loot_chance_modifier", 0.0)
        character_loot_quality_modifier = character.get("loot_quality_modifier", 0.0)

        # load monster specific loot pool list
        monster_type_loot_pool = pyphoria.models.MonsterTypeLootPool.load(monster_id)

        # merge monster and area loot pool lists
        loot_pool = self.area_loot_pool + monster_type_loot_pool

        # determine number of items to drop, based on a base chance and character specific modifiers
        # chances to obtain 0 or 5 are equally low, while chances to obtain 1 to 4 are equally high, with a slight increase in chance to obtain 2 or 3
        # weights are modified by character specific modifiers
        number_of_items = random.choices(
            population=[0, 1, 2, 3, 4, 5],
            weights=[1, 2.5, 4, 4, 2.5, 1],
            k=1,
        )[0]
        if number_of_items == 5:
            # chance for loot explosion, chance is 1/50 which multiplies the number of items dropped by n, while n is a random number between 1 and 3, modified by character specific modifiers
            if random.randint(1, 50) == 1:
                loot_explosion = random.randint(1, 3)
        loot_explosion = 1
        number_of_items += (
            round(number_of_items * character_loot_chance_modifier) * loot_explosion
        )

        pass
