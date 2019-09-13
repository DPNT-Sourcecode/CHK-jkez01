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
    def __set_discount__(self, discount):
        if len(discount) < 2:
            raise ValueError("Invalid DISCOUNT type")
        self.number = discount[0]
        self.cost = discount[1]

    def __set_combo__(self, discount):
        if len(discount) < 2:
            raise ValueError("Invalid COMBO type")
        self.sku = discount[0]
        self.ammount_free = discount[1]

    def __set_type__(self, type, discount):
        return {
            OfferType.DISCOUNT : lambda: self.__set_discount__(discount),
            OfferType.COMBO : lambda: self.__set_combo__(discount) 
        }.get(type, lambda: raise_value_error("Invalid SpecialOffer OfferType"))()

    def __init__(self, type, discount):
        self.type = type
        self.discount = self.__set_type__(type, discount)


class PriceTable:
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
        self.special_offers.append((SpecialOffer(OfferType.DISCOUNT, (2, 45)),'B'))
        self.special_offers.append((SpecialOffer(OfferType.COMBO, ('B', 1)),'E'))
        self.special_offers.append((SpecialOffer(OfferType.DISCOUNT, (3, 130)),'A'))
        self.special_offers.append((SpecialOffer(OfferType.DISCOUNT, (5, 200)),'A'))
        

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


