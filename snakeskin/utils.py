
def observable(cls):
    orig_init = cls.__init__
    def __init__(self,*args,**kwargs):
        self.__observers = []
        orig_init(self,*args,**kwargs)

    def register_observer(self,observer):
        self.__observers.append(observer)
        
    def notify_observers(self,*args,**kwargs):
        for observer in self.__observers:
            observer.notify(*args,**kwargs)

    cls.__init__ = __init__
    cls.register_observer = register_observer
    cls.notify_observers = notify_observers
    return cls
