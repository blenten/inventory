#type:ignore
"""renpy
init python early in inv_screen:
"""

from collections import deque

from renpy.store import Items



@renpy.pure
def square(side):
    if isinstance(side, float):
        ratio = renpy.config.screen_height / renpy.config.screen_width
        return (side * ratio, side)
    return (side, side)

@renpy.pure
def tuple_sort_key(t):
    return t[1] * renpy.config.screen_width + t[0]



class CraftArea:

    def __init__(self):
        self.data = {}
    

    def clear(self):
        self.data.clear()


    def return_drags(self):
        idg = renpy.get_displayable("inventory_screen", "items_draggroup")
        for dname in self.data.keys():
            if d := idg.get_child_by_name(dname):
                d.snap(*pos_stack.get(dname))
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
        
        for r in sorted(self.data.keys(), reverse=True):
            renpy.store.inventory.remove_item(r)
            pos_stack.remove(r)
        self.clear()

        renpy.store.inventory.add_item(res_item.id)
        pos_stack.assign(res_item.id)
        pos_stack.sort()


class PositionStack:
    def __init__(self):
        self.assigned = {}
        self.pos_stack = deque()

    def add_pos(self, pos: tuple):
        self.pos_stack.appendleft(pos)
    
    def assign(self, item_id):
        if item_id in self.assigned:
            return
        self.assigned[item_id] = self.pos_stack.pop()

    def remove(self, item_id):
        if not item_id in self.assigned:
            return
        self.pos_stack.append(self.assigned.pop(item_id))

    def get(self, item_id) -> tuple:
        if item_id in self.assigned:
            return self.assigned[item_id]
        self.assign(item_id)
        return self.assigned[item_id]