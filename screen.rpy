init -1 python early in inventory.screen:

    from renpy.rollback import NoRollback
    from renpy.store import Drag, DragGroup

    from inventory import InventoryState
    from inventory.screen import Position, Size, CraftArea, CraftCell, PosManager, Screen as ScreenData

    from dataclasses import dataclass


    @renpy.pure
    def get_positions(area_pos: Position, area_size: Size, row_len: int) -> tuple[Position]:
        delta = area_size[0] / row_len
        result = []
        for dy in range(0, int(area_size[0] / delta)):
            for dx in range(0, row_len):
                result.append((int(area_pos[0] + dx * delta), int(area_pos[1] + dy * delta)))
        return tuple(result)


    @renpy.pure
    def get_item_drag_size(area_size: Size, row_len: int) -> Size:
        side = int(area_size[0] / row_len)
        return (side, side)


# /* ------------------------------- Screen API ------------------------------- */

    class Screen(ScreenData):

        def __init__(self, *args):
            super().__init__(*args)
            self.inventory_update = None


        @property
        def dg(self) -> DragGroup:
            return renpy.get_displayable(self.name, f'{self.name}_items_draggroup')


        def drag(self, drag_name) -> Drag:
            return self.dg.get_child_by_name(drag_name)


        def return_(self):
            if self.inventory_update:
                return self.inventory_update
            return False


        def reset(self) -> None:
            self.inventory_update = None
            if self.pos:
                self.pos.clear()
            if self.craft_area :
                self.craft_area.clear()


        def on_dragged(self, dragged, dropped_on):
            item_id = dragged[0].drag_name
            start_cell = self.craft_area.get_cell(item_id)
            self.craft_area.remove(item_id)

            if dropped_on is None:
                dragged[0].snap(*self.pos.get(item_id))
                return

            cell_name = dropped_on.drag_name

            # if dropped not on craft cell but random droparea
            if not (self.craft_area and cell_name in self.craft_area.cell_names):
                return

            popped_id = self.craft_area.place(item_id, cell_name)
            dragged[0].snap(*self.craft_area.get_cell_pos(cell_name))

            if popped_id:
                popped = self.drag(popped_id)
                if start_cell:
                    self.craft_area.place(popped_id, start_cell.name)
                    popped.snap(*start_cell.pos)
                    return
                popped.snap(*self.pos.get(popped_id))


        def craft(self, inv):

            recipe = self.craft_area.get_recipe()
            res_item_id = renpy.store.inventory.Items.recipe(recipe)
            if res_item_id is None:
                return

            dg = self.dg
            self.reset()
            for iid in recipe:
                inv.remove_item(iid)
                dg.remove(dg.get_child_by_name(iid))

            inv.add_item(res_item_id)
            self.inventory_update = InventoryState(inv)





# /* --------------------------------- Builder -------------------------------- */

    class ScreenBuilder(NoRollback):

        def __getstate__(self):
            return None

        def __init__(self):
            self.reset()


        def reset(self) -> None:
            self.pos = None
            self.craft = None
            self.cell_size = (100, 100)


        def build(self, name) -> Screen:
            if self.craft is not None:
                cells = (CraftCell(*c) for c in self.craft)
                self.craft = CraftArea(cells)
            result = Screen(name, self.pos, self.cell_size, self.craft)
            return result


        def items_grid(self, area_pos: Position, area_size: Size, row_len: int) -> None:
            self.pos = PosManager(get_positions(area_pos, area_size, row_len))
            self.cell_size = get_item_drag_size(area_size, row_len)

        def cell_size(self, size: Size) -> None:
            self.cell_size = size

        def craft_cell(self, name: str, pos: Position, size: Size = None, recipe_pos: int = 0) -> None:
            if self.craft is None or isinstance(self.craft, CraftArea):
                self.craft = []
            self.craft.append((name, pos, size or self.cell_size, recipe_pos))





# /* ---------------------------------- SHOW ---------------------------------- */

screen hud(btn_img, sc):
    modal False
    showif renpy.get_screen("choice") is None:
        imagebutton auto btn_img:
            focus_mask True
            action Function(inventory.screen.show, sc)




init -1 python early in inventory.screen:

    def show(sc: Screen) -> None:
        if res := renpy.call_in_new_context("_show_inventory_screen", sc):
            renpy.call("_inventory_update", res, from_current=True)




label _show_inventory_screen(sc):
    $ sc.reset()
    window hide
    python:
        With(Dissolve(0.15))()
        result = renpy.call_screen(sc.name, _layer='screens')
        With(Dissolve(0.25))()
    window auto
    $ renpy.return_statement(result)



#  For rollback
label _inventory_update(upd_state):
    $ upd_state.restore()



# /* ------------------------------- ITEMS AREA ------------------------------- */

screen inventory_items(sc, inv, craft=False):
    draggroup:
        id (f"{sc.name}_items_draggroup")
        style (f"{sc.name}_items_area")

        if craft:
            use inventory_craft_cells(sc)

        for item in [i for i in inventory.as_items(inv.list_items()) if not i.hidden]:
            drag:
                drag_name item.id
                tooltip item.description
                # drag_offscreen True
                drag_raise True
                droppable False
                pos sc.pos.get(item.id)
                xysize sc.cell_size
                dragged sc.on_dragged

                frame:
                    style (f"{sc.name}_item_cell")
                    add "[item.pic]":
                        align (0.5, 0.5)
                        fit "contain"
                    text "[item.name]" style (f"{sc.name}_item_cell_text")




screen inventory_craft_cells(sc):

    for cell in sc.craft_area.cells:
        drag:
            drag_name cell.name
            droppable True
            draggable False
            drag_offscreen True
            xysize cell.size
            pos cell.pos

            frame:
                style (f"{sc.name}_craft_cell")
