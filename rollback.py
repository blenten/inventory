from collections import defaultdict, namedtuple
from typing import Union

from .inventory import Inventory
from .exception import InventoryUpdateError



InventoryUpdate = namedtuple('InventoryUpdate', 'add remove')


class UpdateBuilder:

    def __init__(self) -> None:
        self.transaction = defaultdict(int)


    def add(self, item_id: int) -> None:
        self.transaction[item_id] += 1

    def remove(self, item_id: int) -> None:
        self.transaction[item_id] -= 1


    def build(self) -> Union[tuple, None]:
        if len(self.transaction) == 0:
            return None

        add = []
        remove = []
        for iid, mod in self.transaction.items():
            if mod > 0:
                add.append(iid)
            elif mod < 0:
                remove.append(iid)

        self.transaction.clear()
        return InventoryUpdate(add, remove)


    def clear(self) -> None:
        self.transaction.clear()
