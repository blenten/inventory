init -1 python early in inventory.screen:

    from renpy.rollback import NoRollback
    from renpy.store import Drag, DragGroup
    from inventory.screen import Position, Size, PrSize, Craft, PosManager


    @renpy.pure
    def get_positions(area_size: Size, row_len: int) -> tuple[Position]:
        delta = area_size[0] / row_len
        result = []
        for dy in range(0, int(area_size[0] / delta)):
            for dx in range(0, row_len):
                result.append((int(dx * delta), int(dy * delta)))
        return tuple(result)


    @renpy.pure
    def get_item_drag_sizes(area_size: Size, row_len: int) -> tuple:
        side_pr = 1.0 / row_len
        side = int(area_size[0] * side_pr)
        return ((side, side), (side_pr, side_pr))


# /* ------------------------------- Screen API ------------------------------- */

    class Screen(NoRollback):

        def __init__(self, name: str, area_size: Size, row_len: int, craft: Craft = None):

            sizes = get_item_drag_sizes(area_size, row_len)

            self.name = name
            self.pos = PosManager(get_positions(area_size, row_len))
            self.cell_size: Size = sizes[0]
            self.cell_pr_size: PrSize = sizes[1]
            self.craft = craft


        @property
        def dg(self) -> DragGroup:
            return renpy.get_displayable(self.name, f'{self.name}_items_draggroup')


        def drag(self, drag_name) -> Drag:
            return self.dg.get_child_by_name(drag_name)


        def return_(self) -> bool:
            if self.craft is not None:
                return self.craft.craft_occured
            return False


        def reset(self) -> None:
            self.pos.clear()
            if self.craft is not None:
                self.craft.reset()


        def on_dragged(self, dragged, dropped_on):
            item_id = dragged[0].drag_name

            if dropped_on is None:
                dragged[0].snap(*self.pos.get(item_id))
                return

            cell_name = dropped_on.drag_name
            self.pos.remove(item_id)

            # if dropped not on craft cell but random droparea
            if not (self.craft and cell_name in self.craft.cell_names):
                return

            popped_id = self.craft.place_item(item_id, cell_name)
            if popped_id:
                # sc.pos.remove(popped_id) # not needed cause it would be removed when first placed in craft cell
                self.drag(popped_id).snap(*self.pos.get(popped_id))
            dragged[0].snap(*self.craft.get_cell_pos(dropped_on.drag_name))




# /* ---------------------------------- SHOW ---------------------------------- */

screen hud(btn_img, sc):
    modal False
    showif renpy.get_screen("choice") is None:
        imagebutton auto btn_img:
            focus_mask True
            action Function(inventory.screen.show, sc)




init -1 python early in inventory.screen:

    from inventory import InventoryState

    def show(sc: Screen) -> None:
        if renpy.call_in_new_context("_show_inventory_screen", sc):
            renpy.call(
                "_inventory_update",
                InventoryState(renpy.store.inventory.current),
                from_current=True
                )




label _show_inventory_screen(sc):
    $ sc.reset()
    window hide
    python:
        With(Dissolve(0.15))()
        renpy.call_screen(sc.name, _layer='screens')
        With(Dissolve(0.25))()
    window auto
    $ renpy.return_statement(_return)



#  For rollback
label _inventory_update(upd):
    $ upd.apply_to(inventory.active)



# /* ------------------------------- ITEMS AREA ------------------------------- */

screen inventory_items_area(sc, inv):
    draggroup:
        id (f"{sc.name}_items_draggroup")
        style (f"{sc.name}_items_area")

        for item in inventory.as_items(inv.list_items()):
            drag:
                drag_name item.id
                tooltip item.description
                # drag_offscreen True
                drag_raise True
                droppable False
                pos sc.pos.get(item.id)
                xysize sc.cell_pr_size
                dragged sc.on_dragged

                frame:
                    style (f"{sc.name}_item_cell")
                    add "[item.pic]":
                        align (0.5, 0.5)
                        fit "contain"
                    text "[item.name]" style (f"{sc.name}_item_cell_text")
