#type:ignore
"""renpy
init python early:
"""

from itertools import islice

from inventory import ItemGlossary, Item
from inventory.exception import InventoryOverflowError, InventoryDeleteError



with renpy.file("inventory/items.json") as items_file:
    Items = ItemGlossary.from_file(items_file)
# TMP
# it = {}
# for i in Items._items.values():
#     it[i.id + 3] = Item(i.id + 3, i.name, i.description, i.pic)
# Items._items.update(it)
# del it
# /TMP
renpy.const(Items)



class Inventory(renpy.store.object):
    def __init__(self, size: int) -> None:
        self.testflag = True
        self._size: int = size
        self._data: dict[int, int] = {}
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
    
    def add_item(self, item_id: int) -> None:
        if item_id in self._data:
            return
        if self._items_qty >= self._size:
            raise InventoryOverflowError(f'Cant add item. Id: {item_id}') 
        self._data[item_id] = 1
        self._items_qty += 1
        return
    
    def remove_item(self, item_id: int) -> None:
        # placeholder for qty management later
        self.del_item(item_id)
    
    def del_item(self, item_id: int) -> None:
        if not item_id in self._data:
            raise InventoryDeleteError(f'No such item in inventory. Id: {item_id}')
        del self._data[item_id]
        self._items_qty -= 1
        return

    def list_items(self, chunk_size: int = 1) -> list:
        items = (Items.get(iid) for iid in self._data.keys())
        if chunk_size == 1:
            return list(items)
        result = []
        while chunk := list(islice(items, chunk_size)):
            result.append(chunk)
        return result
