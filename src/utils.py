def throw(exc):
    raise exc


def find(arr, expr, default=None):
    return next((el for el in arr if expr(el)), default)
