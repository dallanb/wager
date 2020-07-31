from .. import cache


def get(key):
    return cache.cache.get(key)


def has(key):
    return cache.cache.has(key)


def set(key, val, timeout=30):
    return cache.cache.set(key, val, timeout)


def delete(key):
    return cache.cache.delete(key)


def clear():
    return cache.cache.clear()


def unmemoize(f, **kwargs):
    return cache.delete_memoized(f, **kwargs)
