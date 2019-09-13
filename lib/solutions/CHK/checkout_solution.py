from enum import Enum

@unique
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
    def __process_discount__(discount):
        return discount

    def __process_combo__(discount):
        return -discount

    def __process_type__(type, discount):
        return {
            OfferType.DICOUNT : lambda: __process_discount__(discount),
            OfferType.COMBO : lambda: __process_combo__(discount) 
        }.get(type, lambda: raise_value_error("Invalid SpecialOffer OfferType"))()

    def __init__(self, type, discount):
        self.offer = __process_type__(type,discount)
        

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
    skus are the keys, values are a (price, SpecialOffer) tuple
    price is a number, while SpecialOffer is an object
    if there is no special offer, the value is None
    """
    def __init__(self):
        special_A = SpecialOffer(3,130)
        special_B = SpecialOffer(2,45)
        self.price_table = {'A': (50, special_A),
                            'B': (30, special_B),
                            'C': (20, None),
                            'D': (15, None)}

