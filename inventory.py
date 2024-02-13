from dataclasses import dataclass
from itertools import islice
from .item import Item


class InventoryError(Exception):
    pass

class InventoryOverflowError(InventoryError):
    pass

class InventoryDeleteError(InventoryError):
    pass


@dataclass
class InventoryCell:
    item: Item
    qty: int
    # position: int


class Inventory:
    def __init__(self, size: int) -> None:
        self._size: int = size
        self._data: dict[int, InventoryCell] = {}
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
    
    def clear(self):
        self._data.clear()
        self._items_qty = 0
    
    def has_item(self, item_id: int) -> bool:
        return item_id in self._data
    
    def add_item(self, item: Item, qty: int = 1) -> None:
        if item.id in self._data:
            # self.update_qty(item, qty)
            return
        if self._items_qty >= self._size:
            raise InventoryOverflowError(f'Cant add item. Id: {item.id}') 
        self._data[item.id] = InventoryCell(item, qty)
        self._items_qty += 1
        return
    
    def remove_item(self, item_id: int) -> None:
        # placeholder for qty management later
        self.del_item(item_id)
    
    def del_item(self, item_id: int) -> None:
        if not item_id in self._data:
            raise InventoryDeleteError(f'No such item in inventory. Id: {item_id}')
        self._data.pop(item_id)
        self._items_qty -= 1
        return

    def list_items(self, chunk_size: int = 1) -> list:
        items = (c.item for c in self._data.values())
        if chunk_size == 1:
            return list(items)
        result = []
        while chunk := list(islice(items, chunk_size)):
            result.append(chunk)
        return result
