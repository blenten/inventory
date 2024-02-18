init -1 python early:
    from typing import Iterable

    import inventory as inv
    from inventory import Inventory


    with renpy.file("inventory/items.json") as items_file:
        Items = inv.ItemGlossary.from_file(items_file)
    renpy.const(Items)




    @renpy.pure
    def as_items(iid_list: Iterable) -> list:
        return [Items.get(iid) for iid in iid_list]


    @renpy.pure
    def inventory_after_load():
        """
        Must ba called in the `after_load` label for correct work
        """
        renpy.block_rollback()




# /* ---------------------------- SCREEN DISPLAYING --------------------------- */

init python in inv_screen:

    from renpy.store import inv

    def show():
        if renpy.call_in_new_context("_show_inventory_screen"):
            renpy.call(
                "_inventory_update",
                inv.InventoryState(renpy.store.inventory),
                from_current=True
                )


label _show_inventory_screen:
    $ inv_screen.reset()
    call screen inventory_screen
    $ renpy.return_statement(_return)

#  For rollback
label _inventory_update(upd):
    $ upd.apply_to(inventory)
