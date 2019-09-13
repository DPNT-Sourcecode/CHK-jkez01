# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    price_data = PriceTable()
    total = 0
    special_item_counter = {}
    try:
        for item in skus:
            if item not in price_data:
                return -1
            if price_data[item][1] is None:
                total += price_data[item][0]
            elif item in special_item_counter:
                special_item_counter[item] += 1
                if price_data[item][1][0]
        return total
    except Exception as e:
        return -1

class SpecialOffer:

    def __init__(self, number, cost):
        self.number = number
        self.cost = cost

class PriceTable:
    """
    Holds a price dictionary:
    skus are the keys, values are a (price, special) tuple
    price is a number, while special is a tuple of (n,y)
    where n is n of that sku costs y pounds
    if there is no special offer, special is None
    """
    def __init__(self):
        special_A = SpecialOffer(3,130)
        special_B = SpecialOffer(2,45)
        self.price_table = {'A': (50, special_A),
                            'B': (30, special_B),
                            'C': (20, None),
                            'D': (15, None)}






