# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
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
              'C': (30, None),
              'D': (30, None)}
    return prices


