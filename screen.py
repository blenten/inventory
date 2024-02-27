from dataclasses import dataclass
from typing import Optional, Iterable

from .item import ItemId




Position = tuple[int, int]
Size = tuple[int, int]




@dataclass(frozen=True)
class CraftCell:
    name: str
    pos: Position
    size: Size
    recipe_pos: int = 0




class CraftArea:

    def __init__(self, cells: Iterable[CraftCell]) -> None:
        self._cells = {c.name : c for c in cells}
        self.cell_item = {}
        self.item_cell = {}


    def __reduce__(self):
        return (CraftArea, (tuple(self._cells.values()),))


    def clear(self) -> None:
        self.cell_item.clear()
        self.item_cell.clear()


    @property
    def cell_names(self):
        return self._cells.keys()

    @property
    def cells(self):
        return self._cells.values()

    def get_cell(self, item_id: ItemId) -> Optional[CraftCell]:
        if cname := self.item_cell.get(item_id, False):
            return self._cells[cname]
        return None

    def get_cell_pos(self, name: str) -> Position:
        return self._cells[name].pos


    def place(self, item_id: ItemId, cell_name: str) -> Optional[ItemId]:
        popped = self.cell_item.pop(cell_name, None)
        if popped is not None:
            del self.item_cell[popped]
        self.cell_item[cell_name] = item_id
        self.item_cell[item_id] = cell_name
        return popped


    def remove(self, item_id: ItemId) -> None:
        if not item_id in self.item_cell:
            return
        del self.cell_item[self.item_cell[item_id]]
        del self.item_cell[item_id]


    def get_recipe(self) -> tuple[ItemId]:
        ids = (iid for iid, _ in sorted(self.item_cell.items(), key=lambda it: self._cells[it[1]].recipe_pos))
        return tuple(ids)




class PosManager:

    def __init__(self, positions: tuple[Position]):
        self.positions = positions
        self.assigned = {}
        self.arbitrary = {}


    def __reduce__(self):
        return (PosManager, (self.positions,))


    def get(self, item_id: ItemId) -> Position:
        if item_id in self.arbitrary:
            return self.arbitrary[item_id]
        if not item_id in self.assigned:
            self.assign(item_id)
        return self.positions[self.assigned[item_id]]


    def assign(self, item_id: ItemId, pos: Position = None) -> None:

        if pos is not None:
            if self.assigned.pop(item_id, None) is not None:
                self.sort_and_compress()
            self.arbitrary[item_id] = pos
            return

        if item_id in self.assigned:
            return
        self.assigned[item_id] = len(self.assigned)


    def remove(self, item_id: ItemId, compress: bool = True) -> None:
        if item_id in self.arbitrary:
            del self.arbitrary[item_id]
            return
        if not item_id in self.assigned:
            return
        del self.assigned[item_id]
        if compress:
            self.sort_and_compress()


    def sort_and_compress(self) -> None:
        for pos_idx, iid in enumerate(sorted(self.assigned.keys())):
            self.assigned[iid] = pos_idx


    def clear(self) -> None:
        self.assigned.clear()
        self.arbitrary.clear()





@dataclass(frozen=True)
class Screen:
    name: str
    pos: PosManager = None
    cell_size: Size = (100,100)
    craft_area: CraftArea = None

