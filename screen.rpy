init -1 python early in inventory.screen:

    import inventory as inv
    from inventory import PosManager


    @renpy.pure
    def get_positions(area_size: tuple, row_len: int) -> tuple:
        delta = area_size[0] / row_len
        result = []
        for dy in range(0, int(area_size[0] / delta)):
            for dx in range(0, row_len):
                result.append((int(dx * delta), int(dy * delta)))
        return tuple(result)


    @renpy.pure
    def get_item_drag_size(row_len: int) -> tuple:
        side = 1.0 / row_len
        return (side, side)


    def show(sc_name: str) -> None:
        if renpy.call_in_new_context("_show_inventory_screen", sc_name):
            renpy.call(
                "_inventory_update",
                inv.InventoryState(renpy.store.inventory.current),
                from_current=True
                )


    class Screen(renpy.python.StoreModule):

        def __init__(self):
            super().__init__(renpy.python.StoreDict())

        def return_(self):
            return False

        def reset(self):
            pass

        def item_drugged_func(self, dragged, dropped_on) -> None:
            dragged[0].snap(*(self.drag_pos.get(dragged[0].drag_name)))


    def create(name: str, area_size: tuple, row_len: int) -> Screen:
        res = Screen()
        res.drag_pos = PosManager(get_positions(area_size, row_len))
        res.drag_size = get_item_drag_size(row_len)
        renpy.store.inventory.screen.__setattr__(name, res)
        return res




label _show_inventory_screen(sc_name):
    $ inventory.screen.__dict__[sc_name].reset()
    window hide
    python:
        With(Dissolve(0.15))()
        renpy.call_screen(sc_name, _layer='screens')
        With(Dissolve(0.25))()
    window auto
    $ renpy.return_statement(_return)

#  For rollback
label _inventory_update(upd):
    $ upd.apply_to(inventory.active)




screen hud(btn_img, sc_name):
    modal False
    showif renpy.get_screen("choice") is None:
        imagebutton auto btn_img:
            focus_mask True
            action Function(inventory.screen.show, sc_name)




screen inventory_items_area(sc_name, inv):
    $ sc = inventory.screen.__dict__[sc_name]
    draggroup:
        id (f"{sc_name}_items_draggroup")
        style (f"{sc_name}_items_area")

        for item in inventory.as_items(inv.list_items()):
            drag:
                drag_name item.id
                tooltip item.description
                drag_offscreen True
                drag_raise True
                pos sc.drag_pos.get(item.id)
                xysize sc.drag_size
                dragged sc.item_drugged_func

                frame:
                    style (f"{sc_name}_item_cell")
                    add "[item.pic]":
                        align (0.5, 0.5)
                        fit "contain"
                    text "[item.name]" style (f"{sc_name}_item_cell_text")