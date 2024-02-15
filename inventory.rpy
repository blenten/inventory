init python early:

    from inventory import Inventory, ItemGlossary, Item


    with renpy.file("inventory/items.json") as items_file:
        Items = ItemGlossary.from_file(items_file)
    # TMP
    # it = {}
    # for i in Items._items.values():
    #     it[i.id + 3] = Item(i.id + 3, i.name, i.description, i.pic)
    # Items._items.update(it)
    # del it
    # /TMP
    renpy.const(Items)


    @renpy.pure
    def as_items(iid_list) -> list:
        return [Items.get(iid) for iid in iid_list]


