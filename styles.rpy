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