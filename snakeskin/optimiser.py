import numpy as np
import ephem as eph
from utils import AttrDict,select_from
from telescope import create_telescope

DEFAULT_MODEL = {
    "evaporation_rate":0.9,
    "pheremone_multiplier":1500.0,
    "pheremone_weight":2.0,
    "attractiveness_weight":1.0,
    "max_sources":20,
    "max_duration":18000,
    "num_agents":20,
    "pheremone_init_value":10,
    "pheremone_min_value":0.0
    }

#z = lambda A,x,mu,sigma : A*np.e**(-1*((x-mu)/sigma)**2)

class Pheremones(dict):
    def __init__(self,model_params={}):
        super(Pheremones,self).__init__()
        self.update_params(model_params)

    def update_params(self,model_params):
        self.default = model_params.get("pheremone_init_value",0.5)
        self.min = model_params.get("pheremone_min_value",0.0)
        self.max = model_params.get("pheremone_max_value",np.inf)
        self.rho = model_params.get("evaporation_rate",0.9)

    def evaporate(self):
        for key in self.iterkeys():
            self[key]*=self.rho

    def __missing__(self,key):
        self.__setitem__(key,self.default)
        return self.default
    
    def __setitem__(self,key,val):
        val = min(max(self.min,val),self.max)
        super(Pheremones,self).__setitem__(key,val)

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
        self.best_tour = []
        self.best_score = 0
        
    def update(self,params):
        self.model.update(params)
        self.pheremones.update_params(params)

    def set_nagents(self,n):
        nagents = int(n - len(self.telescopes))
        self.telescopes.extend([create_telescope(self.telescope_config) 
            for _ in range(nagents)])
    
    def probabilities(self,eta,tau):
        a = self.model.pheremone_weight
        b = self.model.attractiveness_weight
        c = (eta**a + tau**b)
        return c/sum(c)

    def _calcualate_attractivenes(self,path):
        m = path.maintenance_cost
        dt = path.drive_time
        v = path.value
        t = 1./path.target.remaining
        return v/(m*dt)
    
    def select_path(self,paths):
        eta = np.empty(len(paths))
        tau = np.empty(len(paths))
        for ii,path in enumerate(paths):
            value = self.evaluator.evaluate(path.target,path.obs_start_date)
            path.value = value
            eta[ii] = self._calcualate_attractivenes(path)
            tau[ii] = self.pheremones[(path.origin,path.target)]
        probs = self.probabilities(eta,tau)
        for prob,eta_,tau_,path in zip(probs,eta,tau,paths):
            if path.origin == None:
                print path.target,prob
            path.probability = prob
            path.attractiveness = eta_
            path.pheremone = tau_
        idx = select_from(probs)
        return paths[idx]

    def _calculate_cost(self,tour):
        total_value = 0
        for path in tour:
            total_value += 1/(path.value/path.drive_time)        
        return total_value

    def _update_pheremones(self,tour,cost):
        value = self.model.pheremone_multiplier / cost
        for path in tour:
            key = path.origin,path.target
            self.pheremones[key] += value
        

    def optimise(self,position,epoch=eph.now()):
        self.set_nagents(self.model.num_agents)
        nagents = int(self.model.num_agents)
    
        for telescope in self.telescopes[:nagents]:
            print "Telescope travelling"
            telescope.travel(position,epoch,self)
        
        self.pheremones.evaporate()
        
        p = [key for key in self.pheremones.keys() if key[0] is None]
        for key in p:
            print key,self.pheremones[key]
        
        for telescope in self.telescopes[:nagents]:
            
            cost = self._calculate_cost(telescope.last_tour)**2
            self._update_pheremones(telescope.last_tour,cost)
            print "Cost = %f"%(cost)
            score = 1./cost
            if score > self.best_score:
                print "New best tour"
                self.best_score = score
                self.best_tour = telescope.last_tour
                self._update_pheremones(self.best_tour,1./self.best_score)
                

        
            


