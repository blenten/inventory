# type:ignore
from renpy.revertable import RevertableObject, RevertableDict

from .exception import InventoryOverflowError, InventoryDeleteError
from .item import ItemId



class Inventory(RevertableObject):
    def __init__(self, size: int) -> None:
        self._size: int = size
        self._data: dict[ItemId, int] = RevertableDict()
        self._items_qty: int = 0

    @property
    def items_qty(self) -> int:
        return self._items_qty

    @property
    def size(self) -> int:
        return self._size

    def is_full(self) -> bool:
        return self._items_qty >= self._size

    def is_empty(self) -> bool:
        return self._items_qty == 0

    def clear(self) -> None:
        self._data.clear()
        self._items_qty = 0

    def has_item(self, item_id: ItemId) -> bool:
        return item_id in self._data

    def add_item(self, item_id: ItemId) -> None:
        if item_id in self._data:
            return
        if self._items_qty >= self._size:
            raise InventoryOverflowError(f'Cant add item. Id: {item_id}')
        self._data[item_id] = 1
        self._items_qty += 1

    def remove_item(self, item_id: ItemId) -> None:
        # placeholder for qty management
        self.del_item(item_id)

    def del_item(self, item_id: ItemId) -> None:
        try:
            del self._data[item_id]
            self._items_qty -= 1
        except KeyError:
            raise InventoryDeleteError(f'No item with id: {item_id} in inventory')

    def list_items(self) -> tuple:
        return tuple(self._data.keys())
