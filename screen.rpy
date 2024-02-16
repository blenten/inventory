init python in inv_screen:

    craft_area = CraftArea()
    drag_pos = PosManager()

    def reset():
        craft_area.clear()
        drag_pos.clear()
        InvUpdBuilder.clear()


    def return_func():
        upd = InvUpdBuilder.build()
        return upd if upd is not None else False


    def item_drugged_func(dragged, dropped_on):
        global drag_pos
        if dropped_on:
            if dropped_on.drag_name == "craft_drop":
                craft_area.add(dragged[0].drag_name)
                return
        dragged[0].snap(*drag_pos.get(dragged[0].drag_name))
        craft_area.remove(dragged[0].drag_name)




screen hud():
    modal False

    showif renpy.get_screen("choice") is None:
        imagebutton auto "inventory/hud_button_%s.png":
            focus_mask True
            action Call("_show_inventory_screen", from_current=True)



label _show_inventory_screen:
    hide screen hud
    $ inv_screen.reset()
    call screen inventory_screen
    show screen hud
    if isinstance(_return, inv.InventoryUpdate):
        $ renpy.suspend_rollback(True)
        jump _craft_occured
        $ renpy.suspend_rollback(False)
    return

label _craft_occured:
    python:
        upd = _return

        if (renpy.in_rollback()
            and isinstance(renpy.roll_forward_info(), inv.InventoryUpdate)):

            upd = renpy.roll_forward_info()

            try:
                for r in upd.remove:
                    renpy.store.inventory.remove_item(r)

            except inv.InventoryDeleteError:    # for rare bug
                del renpy.game.log.forward[-1]
                renpy.return_statement()

            for a in upd.add:
                renpy.store.inventory.add_item(a)

        renpy.checkpoint(upd, hard=False)
    return



screen inventory_screen():
    modal True
    roll_forward True
    style_prefix "inventory"

    add "inventory/bg.png"


    imagebutton auto "inventory/close_button_%s.png":
        focus_mask True
        action Function(inv_screen.return_func)
        # action Return()


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


    draggroup:
        id "items_draggroup"
        style_suffix "items_area"

        for row in inventory.list_items(inv_screen.ITEMS_AREA_ROW_LEN):
            for item in as_items(row):
                drag:
                    drag_name item.id
                    tooltip item.description
                    drag_offscreen True
                    drag_raise True
                    pos inv_screen.drag_pos.get(item.id)
                    xysize (0.25, 0.25)
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


