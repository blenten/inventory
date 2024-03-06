from dataclasses import dataclass
from typing import Optional, Iterable

from .exception import ItemIdError




ItemId = int


ITEMS_KEY = 'items'
RECIPES_KEY = 'craft_recipes'




@dataclass(frozen=True)
class Item:
    id: ItemId
    name: str
    description: str = ''
    pic: Optional[str] = None
    hidden: bool = False

    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id




class ItemGlossary:

    def __init__(self, data: dict) -> None:
        self._items = {i['id']:Item(**i) for i in data[ITEMS_KEY]}
        self.recipes = data[RECIPES_KEY]


    def get(self, item_id: ItemId) -> Item:
        try:
            return self._items[item_id]
        except KeyError:
            raise ItemIdError(f'No item with id: {item_id}')


    def get_list(self) -> list[Item]:
        return self._items.values()


    def recipe(self, item_ids: Iterable[ItemId]) -> Optional[ItemId]:
        key = '+'.join(str(iid) for iid in item_ids)
        return self.recipes.get(key, None)
