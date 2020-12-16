import yaml

from item import Item
from shopping_cart import ShoppingCart
from errors import ItemNotExistError, TooManyMatchesError


class Store:
    def __init__(self, path):
        with open(path) as inventory:
            items_raw = yaml.load(inventory, Loader=yaml.FullLoader)['items']
        self._items = self._convert_to_item_objects(items_raw)
        self._shopping_cart = ShoppingCart()

    @staticmethod
    def _convert_to_item_objects(items_raw):
        return [Item(item['name'],
                     int(item['price']),
                     item['hashtags'],
                     item['description'])
                for item in items_raw]

    def get_items(self) -> list:
        return self._items

    def search_by_name(self, item_name: str) -> list:
        """search an item by name.
        :argument item_name: the item name.
        :return a sorted list of all the items that match the search term.
        :rtype list
        """

        return self.__order_search_list([x for x in self.get_items() if
                                         item_name in x.name and not self._shopping_cart.is_in_cart(x.name)])

    def search_by_hashtag(self, hashtag: str) -> list:
        """search an item by hashtag.
        :argument hashtag: an hashtag to search.
        :return a sorted list of all the items that match the search term.
        :rtype list
        """
        return self.__order_search_list([x for x in self.get_items() if
                                         hashtag in x.hashtags and not self._shopping_cart.is_in_cart(x.name)])

    def __order_search_list(self, search_list: list):
        """reorder search list by the following rules.
         An item i1 would be before item i2 in the result list if i1 has more common
         hashtags with Tags than i2.
         future note: you should improve the running time.

         If both i1 and i2 have the same number of common hashtags with Tags,
         than i1 would appear before i2 if i1.name appears
         before i2.name in the lexicographic order.
        :argument search_list: the list to order.
        :return a sorted list.
        :rtype list
        """
        hashtags_collides = []
        search_list.sort(key=lambda x: x.name)
        # create another list, that count the number of hashtags collides according to the rules
        for j in search_list:
            temp_count = 0
            for i in (hashtag for item in self._shopping_cart.get_cart_list() for hashtag in item.hashtags):
                for h in j.hashtags:
                    if h == i:
                        temp_count += 1
            hashtags_collides.append(temp_count)

        #  short the original list based on the second list
        search_list[:] = [x for _, x in sorted(zip(hashtags_collides, search_list), key=lambda x: x[0], reverse=True)]
        return search_list

    def add_item(self, item_name: str):
        """add an item to the shopping cart.
        :argument item_name: the name of the item we want to add.
        :raise ItemNotExistError if the item isn't exists in the list.
        :raise TooManyMatchesError if two or more item correspond to the name.
        :raise ItemAlreadyExistsError if the item exists in the cart, handheld by the cart.
        """
        count, index = self._check_one(self.get_items(), item_name)
        if count == 0:
            raise ItemNotExistError
        elif count > 1:
            raise TooManyMatchesError
        else:
            self._shopping_cart.add_item(self.get_items()[index])

    def remove_item(self, item_name: str):
        """remove an item to the shopping cart.
                :argument item_name: the name of the item we want to add.
                :raise ItemNotExistError if the item isn't exists in the list.
                :raise TooManyMatchesError if two or more item correspond to the name.
                :raise ItemAlreadyExistsError if the item exists in the cart, handheld by the cart.
                """
        count, index = self._check_one(self._shopping_cart.get_cart_list(), item_name)
        if count == 0:
            raise ItemNotExistError
        elif count > 1:
            raise TooManyMatchesError
        else:
            self._shopping_cart.remove_item(self._shopping_cart.get_cart_list()[index].name)

    def _check_one(self, list_to_check, item_name):
        """
        :param list_to_check: item list
        :param item_name:
        :return count: how many times the name appear in the item list
        :return index: the index of the last corresponding item
        """
        count = 0
        index = -1
        for i in range(len(list_to_check)):
            if item_name in list_to_check[i].name:
                count += 1
                index = i
        return count, index

    def checkout(self) -> int:
        return self._shopping_cart.get_subtotal()
