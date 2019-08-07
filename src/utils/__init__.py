def throw(exc):
    raise exc


def find(arr: list, expr, default=None):
    return next((el for el in arr if expr(el)), default)
