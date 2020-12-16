from item import Item
from errors import ItemNotExistError, ItemAlreadyExistsError
import functools


class ShoppingCart:
    _cart_list = []

    def get_cart_list(self):
        return self._cart_list

    def add_item(self, item: Item):
        """add an item to the shopping cart.
        :argument item: the item we want to add.
        :raise ItemAlreadyExistsError if the item is in the list.
        """
        if self.is_in_cart(item.name):
            raise ItemAlreadyExistsError
        else:
            self._cart_list.append(item)

    def remove_item(self, item_name: str):
        """removes item from a list, if it wasn't there, it raise an exception.
        :argument item_name: the item name as string.
        :raise ItemNotExistError if the item is not in the list.

        """
        length = len(self._cart_list)
        self._cart_list[:] = [x for x in self._cart_list if x.name != item_name]
        if len(self._cart_list) == length:
            raise ItemNotExistError

    def get_subtotal(self) -> int:
        """
        :returns the sum of the item prices as integer.
        :rtype int.
        """
        if len(self._cart_list) == 0:
            return 0
        return functools.reduce(lambda a, b: a + b.price if type(a) == int else a.price + b.price, self._cart_list)

    def is_in_cart(self, item_name: str):
        """ check if an item is in the cart.
        :argument item_name: the item name as string.
        :return if the item is in the cart.
        :rtype bool
        """
        return item_name in (x.name for x in self._cart_list)