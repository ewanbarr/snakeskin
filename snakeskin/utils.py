import numpy as np

SEC_TO_DAYS = 1/86400.

def notify(func):
    def wrapper(obj,*args,**kwargs):
        retval = func(obj,*args,**kwargs)
        obj.notify_observers(func.__name__,retval)
        return retval
    return wrapper

def observable(cls):
    orig_init = cls.__init__
    def __init__(self,*args,**kwargs):
        self.__observers = []
        orig_init(self,*args,**kwargs)

    def register_observer(self,observer):
        self.__observers.append(observer)
        
    def notify_observers(self,func_name,*args,**kwargs):
        for observer in self.__observers:
            observer.notify(func_name,*args,**kwargs)

    cls.__init__ = __init__
    cls.register_observer = register_observer
    cls.notify_observers = notify_observers
    return cls


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Observer(object):
    def __init__(self,observable):
        observable.register_observer(self)

    def notify(self,func_name,*args,**kwargs):
        print func_name,args,kwargs


def select_from(probs):
    r,s = np.random.uniform(0, 1),0
    for idx,prob in enumerate(probs):
        s += prob
        if s >= r:
            return idx
    return idx
