from snakeskin.pheremones import BasePheremoneModel

DEFAULT_MAXMIN_PHEREMONE_MODEL = {
    "max_value": 30.0,
    "min_value": 0.5
}

class MaxMinPheremoneModel(BasePheremoneModel):
    def __init__(self,**params):
        super(MaxMinPheremoneModel,self).__init__(**DEFAULT_MAXMIN_PHEREMONE_MODEL)
        self.parameters.update(params)
        
    def __setitem__(self,key,val):
        max_val = self.parameters['max_value']
        min_val = self.parameters['min_value']
        val = min(max(min_val,val),max_val)
        super(MaxMinPheremoneModel,self).__setitem__(key,val)
