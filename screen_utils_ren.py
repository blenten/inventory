#type:ignore
"""renpy
init 1 python early in inv_screen:
"""

from renpy.store import Items, InvUpdBuilder



@renpy.pure
def square(side):
    if isinstance(side, float):
        ratio = renpy.config.screen_height / renpy.config.screen_width
        return (side * ratio, side)
    return (side, side)


@renpy.pure
def init_positions() -> list:
    delta = ITEMS_AREA_SIZE[0] / ITEMS_AREA_ROW_LEN
    result = []
    for dy in range(0, int(ITEMS_AREA_SIZE[0] / delta)):
        for dx in range(0, ITEMS_AREA_ROW_LEN):
            result.append((int(dx * delta), int(dy * delta)))
    return result



class CraftArea:

    def __init__(self):
        self.data = {}


    def clear(self):
        self.data.clear()


    def return_drags(self):
        idg = renpy.get_displayable("inventory_screen", "items_draggroup")
        for dname in self.data.keys():
            if d := idg.get_child_by_name(dname):
                d.snap(*drag_pos.get(dname))
        self.clear()


    def add(self, item_id):
        if item_id in self.data:
            self.data[item_id] += 1
            return
        self.data[item_id] = 1


    def remove(self, item_id):
        if not item_id in self.data:
            return
        if self.data[item_id] < 2:
            self.data.pop(item_id, None)
            return
        self.data[item_id] -= 1


    def craft(self):
        res_item = Items.craft(*self.data.keys())
        if res_item is None:
            self.return_drags()
            return None

        for r in self.data.keys():
            renpy.store.inventory.remove_item(r)
            InvUpdBuilder.remove(r)
            drag_pos.remove(r, False)
        self.clear()

        renpy.store.inventory.add_item(res_item.id)
        InvUpdBuilder.add(res_item.id)

        drag_pos.assign(res_item.id)
        drag_pos.sort_and_compress()



class PosManager:
    def __init__(self):
        self.positions = tuple(init_positions())
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
