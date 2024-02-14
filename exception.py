class InventoryError(Exception):
    pass

class InventoryOverflowError(InventoryError):
    pass

class InventoryDeleteError(InventoryError):
    pass


class ItemIdError(Exception):
    pass