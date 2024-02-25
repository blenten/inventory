init -1 python early in inventory.screen:

    import inventory as inv
    from inventory.screen import Screen, PosManager


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


    def create(name: str, area_size: tuple, row_len: int) -> Screen:
        res = Screen(
            name,
            PosManager(get_positions(area_size, row_len)),
            get_item_drag_size(row_len)
            )
        return res



# /* ---------------------------------- SHOW ---------------------------------- */

screen hud(btn_img, sc):
    modal False
    showif renpy.get_screen("choice") is None:
        imagebutton auto btn_img:
            focus_mask True
            action Function(inventory.screen.show, sc)




init -1 python early in inventory.screen:
    def show(sc: Screen) -> None:
        if renpy.call_in_new_context("_show_inventory_screen", sc):
            renpy.call(
                "_inventory_update",
                inv.InventoryState(renpy.store.inventory.current),
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
                drag_offscreen True
                drag_raise True
                pos sc.drag_pos.get(item.id)
                xysize sc.drag_size
                dragged sc.drugged_func

                frame:
                    style (f"{sc.name}_item_cell")
                    add "[item.pic]":
                        align (0.5, 0.5)
                        fit "contain"
                    text "[item.name]" style (f"{sc.name}_item_cell_text")
