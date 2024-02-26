from dataclasses import dataclass
from typing import Optional, Iterable




Position = tuple[int, int]
Size = tuple[int, int]
PrSize = tuple[float, float]




@dataclass(frozen=True)
class CraftCell:
    name: str
    pos: Position




class Craft:

    def __init__(self, cells: Iterable[tuple[str, Position]]) -> None:
        self._cells = {CraftCell(c[0], c[1]) for c in cells}
        self.items = {}
        self.craft_occured = False


    def reset(self) -> None:
        self.items.clear()
        self.craft_occured = False


    @property
    def cell_names(self):
        return self._cells.keys()

    @property
    def cells(self):
        return self._cells.values()


    def get_cell_pos(self, name: str) -> Position:
        return self._cells[name].pos


    def place_item(self, item_id: int, cell_name: str) -> Optional[int]:
        popped = self.items.pop(cell_name, None)
        self.items[cell_name] = item_id
        return popped




class PosManager:

    def __init__(self, positions: tuple[Position]):
        self.positions = positions
        self.assigned = {}


    def get(self, item_id: int) -> Position:
        if not item_id in self.assigned:
            self.assign(item_id)
        return self.positions[self.assigned[item_id]]


    def assign(self, item_id: int) -> None:
        if item_id in self.assigned:
            return
        self.assigned[item_id] = len(self.assigned)


    def remove(self, item_id: int, compress: bool = True) -> None:
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
