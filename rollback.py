from typing import NewType

from .inventory import Inventory


_UpdID = NewType('_UpdID', int)
_UPD_ID = 0


def _upd_id() -> _UpdID:
    global _UPD_ID
    _UPD_ID += 1
    return _UpdID(_UPD_ID)




class InventoryState(tuple):

    def __new__(cls, inv: Inventory):
        global _UPD_STORE
        return super().__new__(cls, (_upd_id(), tuple(inv._data.keys())))


    @property
    def upd_id(self) -> _UpdID:
        return self[0]

    @property
    def items(self) -> tuple[int]:
        return self[1]


    def apply_to(self, inv: Inventory) -> None:
        inv.clear()
        for iid in self.items:
            inv.add_item(iid)
