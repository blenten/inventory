init python early:

    import inventory as inv
    from inventory import Inventory


    with renpy.file("inventory/items.json") as items_file:
        Items = inv.ItemGlossary.from_file(items_file)
    renpy.const(Items)


    InvUpdBuilder = inv.UpdateBuilder()
    renpy.const(InvUpdBuilder)



    @renpy.pure
    def as_items(iid_list) -> list:
        return [Items.get(iid) for iid in iid_list]




label after_load:
    python:
        renpy.block_rollback()