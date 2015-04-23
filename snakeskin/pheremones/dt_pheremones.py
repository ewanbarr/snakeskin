from snakeskin.pheremones import BasePheremoneModel
from snakeskin.pheremones import Max

# this is incomplete and needs some thought

TRAIL_DTYPE = [
    ("amplitude","float32"),
    ("epoch","float32"),
    ("width","float32")
]

class PheremoneTrail(object):
    def __init__(self):
        self.coefficients = []
        
    def evaluate(self,epoch):
        ar = np.array(self.coefficients,dtype=TRAIL_DTYPE)
        return (ar['amplitude'] * np.e **(-(epoch-ar['epoch'])**2/ar['width'])).sum()
        
    def evaporate(self,rate):
        for coeff in self.coefficients:
            coeff[0]*=rate

    def __add__(self,coeff):
        self.coefficients.append(coeff)
        return self


class TimeDependentMaxMinPheremoneModel(BasePheremoneModel):
    def __init__(self,params):
        super(MaxMinPheremoneModel,self).__init__(DEFAULT_MAXMIN_PHEREMONE_MODEL)
        self.parameters.update(params)

    def __missing__(self,key):
        trail = PheremoneTrail()
        self.__setitem__(key,trail)
        return trail

    def evaporate(self):
        rate = self.parameters['evaporation_rate']
        for key in self.iterkeys():
            self[key].evaporate(rate)

    def deposit(self,tour,cost):
        value = self.parameters['value_multiplier']/cost
        width = self.parameters['temporal_width']
        for path in tour:
            key = path.origin,path.target
            self.pheremones[key]+=(value,epoch,width)
        
    def __setitem__(self,key,val):
        max_val = self.parameters['max_value']
        min_val = self.parameters['min_value']
        val = min(max(min_val,val),max_val)
        super(MaxMinPheremoneModel,self).__setitem__(key,val)
