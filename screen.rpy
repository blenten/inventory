init python in inv_screen:

    drag_start = {}
    craft_area = CraftArea()

    def return_func():
        drag_start.clear()
        craft_area.clear()
        return True

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
            action Call("_show_inventory_screen", from_current=True)


label _show_inventory_screen:
    hide screen hud
    call screen inventory_screen
    show screen hud
    $ renpy.block_rollback()


screen inventory_screen():
    modal True
    roll_forward True
    style_prefix "inventory"

    add "inventory/bg.png"

    imagebutton auto "inventory/close_button_%s.png":
        focus_mask True
        action Function(inv_screen.return_func)
        # action Return()

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

