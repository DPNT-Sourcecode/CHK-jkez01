# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    price_data = get_price_table_and_offers()
    total = 0
    special_item_counter = {}
    try:
        for item in skus:
            if item not in price_data:
                return -1
            if price_data[item][1] is None:
                total += price_data[item][0]
            else:
                pass
        return total
    except Exception as e:
        return -1

def get_price_table_and_offers():
    """
    Return a price dictionary:
    skus are the keys, values are a (price, special) tuple
    price is a number, while special is a tuple of (n,y)
    where n is n of that sku costs y pounds
    if there is no special offer, special is None
    """
    prices = {'A': (50, (3,130)),
              'B': (30, (2,45)),
              'C': (20, None),
              'D': (15, None)}
    return prices




