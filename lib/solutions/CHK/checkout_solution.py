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
    def is_applicable(self, counters):
        return False

    def get_cost(self):
        return 0

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

class Item:
    def is_special(self):
        return len(self.offers) > 0

    def get_cost(self):
        if not self.is_special():
            return self.price
        else:
            return 0

    def __init__(self, name, price, offers):
        self.name = name
        self.price = price
        self.offers = offers

class PriceTable:
    """
    Holds a price dictionary, and a special offer list:
    skus are the keys, values are a (price, boolean) tuple
    price is a number, while boolean denotes if the item has a special offer

    the special offer list is built and then sorted by favourability to the customer
    """
    def __init__(self):
        a_offers = [SpecialOffer('A', OfferType.DISCOUNT, (5, 200)),
                    SpecialOffer('A', OfferType.DISCOUNT, (3, 130))]
        a = Item('A', 50, a_offers)
        b_offers = [SpecialOffer('B', OfferType.DISCOUNT, (2, 45))]
        b = Item('B', 30, b_offers)
        c = Item('C', 20, [])
        d = Item('D', 15, [])
        e_offers = [SpecialOffer('E', OfferType.COMBO, (2, 'B', 1))]
        e = Item('E', 40, e_offers)
        self.skus = {'A': a, 'B': b, 'C': c, 'D': d, 'E': e}
        self.special_offers = a_offers + e_offers + b_offers
        

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    table = PriceTable()
    total = 0
    special_sku_counter = {}
    try:
        for item in skus:
            if item not in table.skus:
                return -1
            if not table.skus[item].is_special():
                total += table.skus[item].get_cost()
            elif item in special_sku_counter:
                special_sku_counter[item] += 1
            else:
                special_sku_counter[item] = 1
        for offer in table.special_offers:
            while offer.is_applicable(special_sku_counter):
                total += offer.get_cost()
                special_sku_counter = table.apply_special(special_sku_counter, offer)
        for item in special_sku_counter:
            if special_sku_counter[item] != 0:
                total += special_sku_counter[item] * table.skus[item].get_cost()
        return total
    except Exception as e:
        print(e)
        return -1








