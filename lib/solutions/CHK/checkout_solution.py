from enum import enum

@unique
class OfferType(Enum):
    DISCOUNT = 1
    COMBO = 2

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


class SpecialOffer:
    """
    An object that holds (n,y)
    where n is number of that sku, and y is the cost in pounds
    """
    def __init__(self, type, discount):
        if number == 1:
            raise ValueError("Number must be an integer greater than 1")
        self.number = number
        self.cost = cost


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

