# noinspection PyShadowingBuiltins,PyUnusedLocal
def compute(x, y):
    try:
        if x < 0 or x > 100 or y < 0 or y > 100:
            raise ValueError("Parameters must be positive integers between 0-100")
        return x + y
    except Exception as e:
        raise(e)

