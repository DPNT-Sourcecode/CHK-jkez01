from enum import Enum

class OfferType(Enum):
    DISCOUNT = 1
    COMBO = 2

def raise_value_error(message):
    raise ValueError(message)

class SpecialOffer:
    """
    Describes a special offer for an SKU
    Types can be any of OfferType, discount describes what the offer is
    """
    def __get_discount_cost__(price):
        return self.number * price - self.cost 

    def __get_combo_cost__(price_table):
        return price_table[self.discounted_sku][0] * self.ammount_free 

    def __get_cost_savings__(self, price_table):
        if self.sku not in price_table:
            raise ValueError("Price_table is missing sku for cost calculation")
        return {
            OfferType.DISCOUNT : lambda: self.__get_discount_cost__(price_table[self.sku][0]),
            OfferType.COMBO : lambda: self.__get_combo_cost__(price_table) 
        }.get(self.type, lambda: raise_value_error("Invalid SpecialOffer OfferType"))()

    def __set_discount__(self, discount):
        if len(discount) < 2:
            raise ValueError("Invalid DISCOUNT type")
        self.number = discount[0]
        self.cost = discount[1]

    def __set_combo__(self, discount):
        if len(discount) < 3:
            raise ValueError("Invalid COMBO type")
        self.ammount_needed = discount[0]
        self.discounted_sku = discount[1]
        self.ammount_free = discount[2]

    def __set_type__(self, discount):
        return {
            OfferType.DISCOUNT : lambda: self.__set_discount__(discount),
            OfferType.COMBO : lambda: self.__set_combo__(discount) 
        }.get(self.type, lambda: raise_value_error("Invalid SpecialOffer OfferType"))()

    def __init__(self, sku, type, discount):
        self.sku = sku
        self.type = type
        self.discount = self.__set_type__(discount)


class PriceTable:

    def __sorter_method__(self, offer, price_table):
        return offer.__get_cost_savings__(price_table)
        

    """
    Holds a price dictionary, and a special offer list:
    skus are the keys, values are a (price, boolean) tuple
    price is a number, while boolean denotes if the item has a special offer

    the special offer list is built and then sorted by favourability to the customer
    """
    def __init__(self):
        self.price_table = {'C': (20, False), 'D': (15, False), 'B':(30, True),
        'E': (40, True), 'A': (50, True)}
        self.special_offers = []
        self.special_offers.append((SpecialOffer('B', OfferType.DISCOUNT, (2, 45))))
        self.special_offers.append((SpecialOffer('E', OfferType.COMBO, (2, 'B', 1))))
        self.special_offers.append((SpecialOffer('A', OfferType.DISCOUNT, (3, 130))))
        self.special_offers.append((SpecialOffer('A', OfferType.DISCOUNT, (5, 200))))
        self.special_offers.sort(key=self.__sorter_method__(self.price_table), reverse=True)
        

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    price_data = PriceTable()
    total = 0
    special_item_counter = {}
    try:
        for item in skus:
            if item not in price_data.price_table:
                return -1
            if price_data.price_table[item][1] is None:
                total += price_data.price_table[item][0]
            elif item in special_item_counter:
                special_item_counter[item] += 1
                if price_data.price_table[item][1].number == special_item_counter[item]:
                    special_item_counter[item] = 0
                    total += price_data.price_table[item][1].cost
            else:
                special_item_counter[item] = 1
        for item in special_item_counter:
            if special_item_counter[item] != 0:
                total += special_item_counter[item] * price_data.price_table[item][0]
        return total
    except Exception as e:
        return -1
