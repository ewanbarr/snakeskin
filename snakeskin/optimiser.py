import numpy as np
import ephem as eph
from utils import AttrDict

DEFAULT_MODEL = {
    "evaporation_rate":0.9,
    "pheremone_multiplier":500.0,
    "pheremone_weight":1.0,
    "attractiveness_weight":1.0,
    "max_sources":20,
    "max_duration":18000,
    "num_agents":20,
    }

class Pheremones(dict):
    def __init__(self,model_params={}):
        super(Pheremones,self).__init__()
        self.update_params(model_params)

    def update_params(self,model_params)
        self.default = model_params.get("pheremone_init_value",0.5)
        self.min = model_params.get("pheremone_min_value",0.0)
        self.max = model_params.get("pheremone_max_value",np.inf)
        self.rho = model_params.get("evaporation_rate",0.9)
        self.Q = model_params.get("pheremone_multiplier",500.0) 

    def update_trail(self,path,cost):
        val = self.Q / cost
        for a,b in zip(path[:-1],path[1:]):
            self.pheremones[(a,b)] += val

    def evaporate(self):
        for key in self.iterkeys():
            self[key]*=self.rho

    def __missing__(self,key):
        self.__setitem__(key,self.default)
        return self.default
    
    def __setitem__(self,key,val):
        val = min(max(self.min,val),self.max)
        super(Pheremones,self).__setitem__(self,key,val)

    def all_paths(self,start_node,nodes):
        return [self[(start_node,node)] for node in nodes]


class AntColonyOptimiser(object):
    def __init__(self, sources, evaluator, 
                 telescope_config, 
                 model_params = DEFAULT_MODEL):
        self.telescope_config = telescope_config
        self.model = AttrDict(model_params)
        self.pheremones = Pheremones(self.model)
        self.telescopes = []
        self.sources = sources
        self.evaluator = evaluator
        self.pheremones = Pheremones(self.model)
        self.best_path = []
        self.best_score = 0
        
    def update(self,params):
        self.model.update(params):
        self.pheremones.update_params(params)

    def set_nagents(self,n):
        nagents = len(self.telescopes)
        self.telescopes.extend(create_telescopes(self.telescope_config,n=n-nagents))
    
    def probabilities(self,eta,tau):
        a = self.model.pheremone_weight
        b = self.model.attractiveness_weight
        c = (eta**a + tau**b)
        return c/sum(c)

    def _calcualate_attractivenes(self,maintenance_cost,drive_time,source_value):
        m,dt,v = maintenance_cost, drive_time, source_value
        return v/(m*dt)
    
    def select_path(self,paths):
        eta = np.empty(len(paths))
        tau = np.empty(len(paths))
        for ii,path in evaluate(paths):
            value = self.evaluator.evaluate(path.source,path.obs_start_epoch)
            path.value = value
            eta[ii] = self._calcualate_attractivenes(path.maintenace_cost,path.drive_time,value)
            tau[ii] = self.pheremones[(path.origin,path.target)]
        probs = self.probabilities(eta,tau)
        idx = select_from(probs)
        return paths[idx]
            
    def optimise(self,position,epoch=eph.now()):
        self.set_nagents(self.model.num_agents)
        
        for telescope in self.telescopes[:self.model.num_agents]:
            telescope.travel(position,epoch,self)
        
        self.pheremones.evaporate()
        for telescope in self.telescopes[:self.model.num_agents]:
            cost = telescope.value
            path = telescope.observed
            self.pheremones.update_trail(path,cost)
            
            score = 1./cost
            if score > self.best_score:
                self.best_score = score
                self.best_path = path
                

        
            


