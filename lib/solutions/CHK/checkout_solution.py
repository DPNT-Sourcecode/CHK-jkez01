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
        return discount

    def __set_combo__(self, discount):
        return discount

    def __set_type__(self, type, discount):
        return {
            OfferType.DISCOUNT : lambda: self.__set_discount__(discount),
            OfferType.COMBO : lambda: self.__set_combo__(discount) 
        }.get(type, lambda: raise_value_error("Invalid SpecialOffer OfferType"))()

    def __init__(self, type, discount):
        self.offer = self.__set_type__(type, discount)
        

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


class PriceTable:
    """
    Holds a price dictionary:
    skus are the keys, values are a (price, [SpecialOffer]) tuple
    price is a number, while [SpecialOffer] is a list of objects
    """
    def __init__(self):
        self.price_table = {'C': (20, []), 'D': (15, [])}
        self.price_table['B'] = (30, [SpecialOffer(OfferType.DISCOUNT, (2, 45))])
        self.price_table['E'] = (40, [SpecialOffer(OfferType.COMBO, ('B', 1))])
        a_list = []
        a_list.append(SpecialOffer(OfferType.DISCOUNT, (3, 130)))
        a_list.append(SpecialOffer(OfferType.DISCOUNT, (5, 200)))
        self.price_table['A'] = (50, a_list)
