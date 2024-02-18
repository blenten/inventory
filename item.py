from dataclasses import dataclass
import json
from typing import Optional

from .exception import ItemIdError


@dataclass(frozen=True)
class Item:
    id: int
    name: str
    description: str
    pic: str

    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id


class ItemGlossary:

    def __init__(self) -> None:
        self._items = {}
        self._craft_recipies = {}

    @classmethod
    def from_file(cls, item_file):
        res = cls()
        res.load(item_file)
        return res

    def load(self, items_file) -> None:
        item_data = json.load(items_file)
        self._items = {i['id']:Item(**i) for i in item_data['items']}
        for key, res_id in item_data['craft_recepies'].items():
            self._craft_recipies[key] = self.get(res_id)

    def get(self, iid: int) -> Item:
        try:
            return self._items[iid]
        except KeyError:
            raise ItemIdError(f'No item with id: {iid}')

    def get_list(self) -> list[Item]:
        return self._items.values()

    def craft(self, *item_ids: list[int]) -> Optional[Item]:
        key = '+'.join(map(str, sorted(item_ids)))
        return self._craft_recipies.get(key, None)

