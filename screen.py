from dataclasses import dataclass




class PosManager:

    def __init__(self, positions: tuple):
        self.positions = positions
        self.assigned = {}

    def get(self, item_id):
        if not item_id in self.assigned:
            self.assign(item_id)
        return self.positions[self.assigned[item_id]]

    def assign(self, item_id):
        if item_id in self.assigned:
            return
        self.assigned[item_id] = len(self.assigned)

    def remove(self, item_id, compress=True):
        if not item_id in self.assigned:
            return
        del self.assigned[item_id]
        if compress:
            self.sort_and_compress()

    def sort_and_compress(self):
        for pos_idx, iid in enumerate(sorted(self.assigned.keys())):
            self.assigned[iid] = pos_idx

    def clear(self):
        self.assigned.clear()




@dataclass
class Screen:
    name: str
    drag_pos: PosManager
    drag_size: tuple


    def reset(self) -> None:
        self.drag_pos.clear()

    def return_(self) -> bool:
        return False

    def drugged_func(self, dragged, dropped_on) -> None:
        dragged[0].snap(*(self.drag_pos.get(dragged[0].drag_name)))
