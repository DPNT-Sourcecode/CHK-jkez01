from enum import Enum


class OfferType(Enum):
    DISCOUNT = 1
    COMBO = 2
    ANYPACK = 3


def raise_value_error(message):
    raise ValueError(message)


class SpecialOffer:
    """
    Describes a special offer for an SKU
    Types can be any of OfferType, discount describes what the offer is
    """

    def apply_special(self, counters):
        return {
            OfferType.DISCOUNT: lambda: self.__apply_discount__(counters),
            OfferType.COMBO: lambda: self.__apply_combo__(counters),
            OfferType.ANYPACK: lambda: self.__apply_anypack__(counters),
        }.get(self.type, lambda: raise_value_error("Invalid SpecialOffer OfferType"))()

    def __apply_combo__(self, counters):
        print(self.sku, self.ammount_needed,
              self.discounted_sku, self.ammount_free)
        counters[self.sku] -= self.ammount_needed
        counters[self.discounted_sku] -= self.ammount_free
        return counters

    def __apply_anypack__(self, counters):
        print("apply anypack not implemented")
        return counters = {}

    def __apply_discount__(self, counters):
        counters[self.sku] -= self.number
        return counters

    def is_applicable(self, counters):
        return {
            OfferType.DISCOUNT: lambda: self.__is_applicable_discount__(counters),
            OfferType.COMBO: lambda: self.__is_applicable_combo__(counters),
            OfferType.ANYPACK: lambda: self.__is_applicable_anypack__(counters)
        }.get(self.type, lambda: raise_value_error("Invalid SpecialOffer OfferType"))()

    def __is_applicable_combo__(self, counters):
        if self.sku not in counters:
            return False
        if counters[self.sku] < self.ammount_needed:
            return False
        if self.sku == self.discounted_sku:
            if counters[self.sku] < self.ammount_needed + 1:
                return False
            return True
        if self.discounted_sku not in counters:
            return False
        if counters[self.discounted_sku] < self.ammount_free:
            return False
        return True

    def __is_applicable_anypack__(self, counters):
        counter = 0
        for i in self.skus:
            if i in counters:
                print(i, counters[i])  # counter += counters[i]
        print(counter)
        return counter >= self.ammount

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

    def __get_anypack_cost__(self, skus):
        print("anypack cost not implemented")
        return 0

    def get_cost(self, skus):
        if self.sku not in skus and self.type != OfferType.ANYPACK:
            raise ValueError("Price_table is missing sku for cost calculation")
        return {
            OfferType.DISCOUNT: lambda: self.__get_discount_cost__(skus[self.sku].price),
            OfferType.COMBO: lambda: self.__get_combo_cost__(skus),
            OfferType.ANYPACK: lambda: self.__get_anypack_cost__(skus)
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

    def __set_anypack__(self, discount):
        if len(discount) < 7:
            raise ValueError("Invalid ANYPACK type")
        discount = discount.split(' ')
        self.ammount = int(discount[2])
        self.price = int(discount[6])
        discount_skus = discount[4][1:len(discount[4])-1].split(',')
        self.skus = discount_skus

    def __set_type__(self, discount):
        return {
            OfferType.DISCOUNT: lambda: self.__set_discount__(discount),
            OfferType.COMBO: lambda: self.__set_combo__(discount),
            OfferType.ANYPACK: lambda: self.__set_anypack__(discount)
        }.get(self.type, lambda: raise_value_error("Invalid SpecialOffer OfferType"))()

    def __get_discount_savings__(self, price):
        return self.number * price - self.cost

    def __get_combo_savings__(self, skus):
        if self.sku == self.discounted_sku:
            return skus[self.sku].price
        return skus[self.discounted_sku].price * self.ammount_needed

    def __get_anypack_savings__(self, skus):
        max_value = 0
        for i in self.skus:
            if skus[i].price > max_value:
                max_value = skus[i].price
        return max_value * self.ammount

    def get_savings(self, skus):
        if self.sku not in skus and self.type != OfferType.ANYPACK:
            raise ValueError(
                "Price_table is missing sku for savings calculation")
        return {
            OfferType.DISCOUNT: lambda: self.__get_discount_savings__(skus[self.sku].price),
            OfferType.COMBO: lambda: self.__get_combo_savings__(skus),
            OfferType.ANYPACK: lambda: self.__get_anypack_savings__(skus)
        }.get(self.type, lambda: raise_value_error("Invalid SpecialOffer OfferType"))()

    def __init__(self, sku, type, discount):
        self.sku = sku
        self.type = type
        self.discount = self.__set_type__(discount)


class Item:

    def __init__(self, name, price, offers, is_special):
        self.name = name
        self.price = price
        self.offers = offers
        self.is_special = is_special


class PriceTable:
    """
    Holds a price dictionary, and a special offer list:
    skus are the keys, values are a (price, boolean) tuple
    price is a number, while boolean denotes if the item has a special offer

    the special offer list is built and then sorted by favourability to the customer
    """

    def __sorting_helper__(self, offer):
        return offer.get_savings(self.skus)

    def __init__(self):
        self.skus = {}
        self.special_offers = []
        self.special_offer_duplicates = {}
        with open('lib/solutions/CHK/input.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().split('|')
                temp_offers = []
                offer = line[3].strip()
                if 'buy' in offer:
                    temp_offers.append(SpecialOffer(
                        offer, OfferType.ANYPACK, offer))
                elif 'for' in offer:
                    offers = line[3].strip().split(',')
                    for offer in offers:
                        offer = offer.strip().split(' ')
                        position = 0
                        while offer[0][position].isnumeric():
                            position += 1
                        temp_offers.append(SpecialOffer(
                            offer[0][position:], OfferType.DISCOUNT, (int(offer[0][:position]), int(offer[2]))))
                elif 'free' in offer and 'get' in offer:
                    offer = offer.split(' ')
                    position = 0
                    while offer[0][position].isnumeric():
                        position += 1
                    temp_offers.append(SpecialOffer(
                        offer[0][position:], OfferType.COMBO, (int(offer[0][:position]), offer[3], 1)))
                    if offer[3] in self.skus:
                        self.skus[offer[3]].is_special = True
                is_special = False
                if len(temp_offers) > 0:
                    is_special = True
                temp_item = Item(line[1].strip(), int(
                    line[2].strip()), temp_offers, is_special)
                self.skus[line[1].strip()] = temp_item
                for offer in temp_offers:
                    if offer.sku not in self.special_offer_duplicates:
                        self.special_offers.append(offer)
                    if offer.type == OfferType.ANYPACK:
                        self.special_offer_duplicates[offer] = True
        self.special_offers = sorted(
            self.special_offers, key=self.__sorting_helper__, reverse=True)


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
            if not table.skus[item].is_special:
                total += table.skus[item].price
            elif item in special_sku_counter:
                special_sku_counter[item] += 1
            else:
                special_sku_counter[item] = 1
        for offer in table.special_offers:
            while offer.is_applicable(special_sku_counter):
                print('yes')
                total += offer.get_cost(table.skus)
                special_sku_counter = offer.apply_special(special_sku_counter)
        for item in special_sku_counter:
            if special_sku_counter[item] != 0:
                total += special_sku_counter[item] * table.skus[item].price
        return total
    except Exception as e:
        return -1







