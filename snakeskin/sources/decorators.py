from functools import wraps

def position_cache(func):
    cache_ = {}
    @wraps(func)
    def wrapped(obj,telescope):
        lmst = telescope.sidereal_time()
        lat = telescope.lat
        key = (obj._ra,obj._dec,lmst,lat)
        if key in cache_:
            return cache_[key]
        else:
            retval = func(obj,telescope)
            cache_[key] = retval
            return retval
    return wrapped

