define inv_screen.INVENTORY_ROW_LEN = 4
define inv_screen.CRAFT_BORDER = 155

style inventory_items_area:
    pos (285, 220)
    xysize inv_screen.square(0.603)

style inventory_item_cell is empty:
    # background "#0000FF"
    xfill True
    yfill True
    padding (5, 5)

style inventory_item_cell_text is text:
    size 18
    align (0.5, 1.0)

style craft_area is empty:
    pos (752 + inv_screen.CRAFT_BORDER, 5 + inv_screen.CRAFT_BORDER)
    xysize (410 - inv_screen.CRAFT_BORDER * 2, 470 - inv_screen.CRAFT_BORDER * 2)


style inventory_craftbutton is frame:
    pos (1040, 713)
    xysize (403, 147)
    background "#d9c89b"

style inventory_craftbutton_text is text:
    align (0.5, 0.5)
    size 45
    kerning 10
    color "#ffefc5"


#  ------------------ indescribable horrors below this line -----------------

init python early:
    from inventory import Inventory, Item, ItemGlossary
    
    with renpy.file("inventory/items.json") as items_file:
        Items = ItemGlossary.from_file(items_file)
    renpy.const(Items)

    def _call_inventory_screen():
        inv_screen.reset()
        renpy.call_in_new_context("_show_inventory_screen")
        print(renpy.game.context().current)
        renpy.checkpoint(hard=False)
        

init python early in inv_screen:
    from renpy.store import Items
    from collections import deque


    class Position:
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


    class CraftArea:
        def __init__(self):
            self.data = {}
        
        def clear(self):
            self.data.clear()

        def return_drags(self):
            idg = renpy.get_displayable("inventory_screen", "items_draggroup")
            for dname in self.data.keys():
                if d := idg.get_child_by_name(dname):
                    d.snap(*drag_start[dname])
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
                return
            for iid in self.data.keys():
                renpy.store.inventory.remove_item(iid)
            renpy.store.inventory.add_item(res_item)
            self.clear()
            drag_start.clear()



init python in inv_screen:

    @renpy.pure
    def square(side):
        ratio = renpy.config.screen_height / renpy.config.screen_width
        return (side * ratio, side)

    drag_start = {}
    craft_area = CraftArea()

    def reset():
        drag_start.clear()
        craft_area.clear()

    def item_activated_func(dragged):
        iid = dragged[0].drag_name
        if iid in drag_start:
            return
        drag_start[iid] = (dragged[0].x, dragged[0].y)

    def item_drugged_func(dragged, dropped_on):
        if dropped_on:
            if dropped_on.drag_name == "craft_drop":
                craft_area.add(dragged[0].drag_name)
                return
        dragged[0].snap(*drag_start[dragged[0].drag_name])
        craft_area.remove(dragged[0].drag_name)




screen hud():
    modal False

    showif renpy.get_screen("choice") is None:
        imagebutton auto "inventory/hud_button_%s.png":
            focus_mask True
            action Function(_call_inventory_screen)



label _show_inventory_screen:
    hide screen hud
    call screen inventory_screen
    show screen hud
    return


screen inventory_screen():
    modal True
    style_prefix "inventory"

    add "inventory/bg.png"

    imagebutton auto "inventory/close_button_%s.png":
        focus_mask True
        action Return()

    draggroup:
        id "items_draggroup"
        style_suffix "items_area"
        for yn, row in enumerate(inventory.list_items(4)):
            for xn, item in enumerate(row):
                drag:
                    drag_name item.id
                    tooltip item.description
                    drag_offscreen True
                    drag_raise True
                    pos (float(xn), float(yn))
                    xysize (0.25, 0.25)
                    activated inv_screen.item_activated_func
                    dragged inv_screen.item_drugged_func

                    frame:
                        style_suffix "item_cell"
                        add "[item.pic]":
                            align (0.5, 0.5)
                            fit "contain"
                        text "[item.name]" style "inventory_item_cell_text"
        
        drag:
            drag_name "craft_drop"
            draggable False
            droppable True
            style "craft_area"

            fixed:
                xfill True
                yfill True
                # background "#00FF00"

    button:
        style "inventory_craftbutton"
        action Function(inv_screen.craft_area.craft)
        hovered SetScreenVariable("craftbutton_hovered", True)
        unhovered SetScreenVariable("craftbutton_hovered", False)
        default craftbutton_hovered = False

        if craftbutton_hovered:
            text "CROooOFT" style "inventory_craftbutton_text":
                outlines [(3, "#ffefc5", 0, 0)]
                color "#000000"
        else:
            text "CROOFT" style "inventory_craftbutton_text"            

