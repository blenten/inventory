from dataclasses import dataclass
from typing import Optional, Iterable

from .exception import ItemIdError




ItemId = int


NULL_ID = -1


ITEMS_KEY = 'items'
RECIPES_KEY = 'craft_recipes'




@dataclass(frozen=True)
class Item:
    id: ItemId
    name: str
    description: str = ''
    hidden: bool = False
    pic: Optional[str] = None
    shadow_pic: Optional[str] = None

    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id




class ItemGlossary:

    def __init__(self, data: dict) -> None:
        self._items = {i['id']:Item(**i) for i in data[ITEMS_KEY]}
        self.recipes = data[RECIPES_KEY]

        if NULL_ID not in self._items:
            self._items[NULL_ID] = Item(NULL_ID, '', hidden=True)


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


    def name(self, item_id: ItemId) -> str:
        return self.get(item_id).name


    def description(self, item_id: ItemId) -> str:
        return self.get(item_id).description
