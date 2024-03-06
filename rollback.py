from .inventory import Inventory




class InventoryState(tuple):

    def __new__(cls, inv: Inventory):
        return super().__new__(cls, (inv, tuple(inv._data.keys())))

    def __reduce__(self):
        return (super().__new__, (InventoryState, (self[0], self[1])))



    @property
    def inv(self) -> Inventory:
        return self[0]

    @property
    def items(self) -> tuple[int]:
        return self[1]


    def restore(self) -> None:
        self.inv.clear()
        for iid in self.items:
            self.inv.add_item(iid)
