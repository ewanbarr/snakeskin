
DEFAULT_PHEREMONE_MODEL = {
    "initial_level":1,
    "evaporation_rate":0.95,
    "value_multiplier":1.0
}

class BasePheremoneModel(dict):
    def __init__(self,**params):
        self.parameters = DEFAULT_PHEREMONE_MODEL
        self.parameters.update(params)
        super(BasePheremoneModel,self).__init__()

    def __missing__(self,key):
        default = self.parameters['initial_level']
        self.__setitem__(key,default)
        return default

    def evaporate(self):
        rate = self.parameters['evaporation_rate']
        for key in self.iterkeys():
            self[key]*=rate
        
    def deposit(self,tour,cost):
        value = self.parameters['value_multiplier']/cost
        for path in tour:
            key = path.origin,path.target
            self.pheremones[key]+=value
        
