init -2 python early in inventory:

    from typing import Iterable
    import json
    import inventory as inv
    from inventory import Inventory


    with renpy.file("items.json") as items_file:
        item_data = json.load(items_file)

    Items = inv.ItemGlossary(item_data)


    @renpy.pure
    def as_items(iid_list: Iterable) -> list:
        return [Items.get(iid) for iid in iid_list]
