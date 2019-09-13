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

    def apply_special(self, counters):
        return {
            OfferType.DISCOUNT : lambda: self.__apply_discount__(counters),
            OfferType.COMBO : lambda: self.__apply_combo__(counters) 
        }.get(self.type, lambda: raise_value_error("Invalid SpecialOffer OfferType"))()

    def __apply_combo__(self, counters):
        counters[self.sku] -= self.ammount_needed
        counters[self.discounted_sku] -= self.ammount_free
        return counters

    def __apply_discount__(self, counters):
        counters[self.sku] -= self.number
        return counters

    def is_applicable(self, counters):
        return {
            OfferType.DISCOUNT : lambda: self.__is_applicable_discount__(counters),
            OfferType.COMBO : lambda: self.__is_applicable_combo__(counters) 
        }.get(self.type, lambda: raise_value_error("Invalid SpecialOffer OfferType"))()

    def __is_applicable_combo__(self, counters):
        if self.sku not in counters:
            return False
        if counters[self.sku] < self.ammount_needed:
            return False
        if self.discounted_sku not in counters:
            return False
        if counters[self.discounted_sku] < self.ammount_free:
            return False
        return True

    def __is_applicable_discount__(self, counters):
        if self.sku not in counters:
            return False
        if counters[self.sku] < self.number:
            return False
        return True

    def __get_discount_cost__(self, price):
        return self.cost 

    def __get_combo_cost__(self, skus):
        return skus[self.sku].price * self.ammount_needed 

    def get_cost(self, skus):
        if self.sku not in skus:
            raise ValueError("Price_table is missing sku for cost calculation")
        return {
            OfferType.DISCOUNT : lambda: self.__get_discount_cost__(skus[self.sku].price),
            OfferType.COMBO : lambda: self.__get_combo_cost__(skus) 
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
        return self.price

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
        f_offers = [SpecialOffer('F', OfferType.COMBO, (3, 'F', 1))]
        f = Item('F', 10, f_offers)
        self.skus = {'A': a, 'B': b, 'C': c, 'D': d, 'E': e, 'F': f}
        self.special_offers = a_offers + e_offers + b_offers + f_offers
        

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
            print(offer.sku)
            while offer.is_applicable(special_sku_counter):
                print('is applicable', total)
                total += offer.get_cost(table.skus)
                print('new total', total)
                print(special_sku_counter)
                special_sku_counter = offer.apply_special(special_sku_counter)
                print(special_sku_counter)
        print(total, special_sku_counter)
        for item in special_sku_counter:
            if special_sku_counter[item] != 0:
                print(item)
                total += special_sku_counter[item] * table.skus[item].get_cost()
        print(total, special_sku_counter)
        return total
    except Exception as e:
        print(e)
        return -1
