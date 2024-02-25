init -2 python early in inventory:

    from typing import Iterable
    import inventory as inv


    with renpy.file("inventory/items.json") as items_file:
        Items = inv.ItemGlossary.from_file(items_file)
    renpy.const(Items)


    @renpy.pure
    def as_items(iid_list: Iterable) -> list:
        return [Items.get(iid) for iid in iid_list]


    @renpy.pure
    def after_load() -> None:
        """
        Must ba called in the `after_load` label for correct work
        """
        renpy.block_rollback()




    active: inv.Inventory = None

    def create(size: int, set_active: bool = False) -> inv.Inventory:
        global active
        res = inv.Inventory(size)
        if (not active) or set_active:
            active = res
        return res
