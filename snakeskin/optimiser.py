import numpy as np
import ephem as eph
from utils import AttrDict

class Pheremones(dict):
    def __init__(self,default=0.5):
        super(Pheremones,self).__init__()
        self.default = default

    def __missing__(self,key):
        self.__setitem__(key,self.default)
        return self.default

    def all_paths(self,start_node,nodes):
        return [self[(start_node,node)] for node in nodes]

class AntColonyOptimiser(object):
    def __init__(self,sources,telescope_type):
        self.telescope_type = telescope_type
        self.telescopes = []
        self.sources = sources
        self.best_path = []
        self.best_score = 0
        self.model = AttrDict()
        self.model.evaporation_rate = 0.9
        self.model.score_multiplier = 500.0
        self.model.pheremone_weight = 1.0
        self.model.cost_weight = 1.0
        self.model.max_sources = 20
        self.model.max_duration = 18000
        self.model.num_agents = 20
        self.pheremones = Pheremones()
        self.set_nagents(self.model.num_agents)

    def set_nagents(self,n):
        nagents = len(self.telescopes)
        if nagents<n:
            self.telescopes.extend([self.telescope_type() for _ in range(n-nagents)])
    
    def probabilities(self,eta,tau):
        a = self.model.pheremone_weight
        b = self.model.cost_weight
        c = (eta**a + tau**b)
        return c/sum(c)
            
    def evaporate(self):
        for key,item in self.pheremones.items():
            val = item*self.model.evaporation_rate
            self.pheremones[key] = val

    def optimise(self,position,epoch=eph.now()):
        for telescope in self.telescopes:
            telescope.set_position(*position)
            telescope.set_date(epoch)
            telescope.travel(self)
            
        for telescope in self.telescopes:
            cost = telescope.value
            path = telescope.observed
            self.update_pheremones(cost,path)
            
            score = 1./cost
            print score,self.best_score
            if score > self.best_score:
                print "hit"
                self.best_score = score
                self.best_path = path
                print path
        print self.best_path

    def update_pheremones(self,cost,path):
        value = self.model.score_multiplier/cost
        start = path[0]
        for p in path[1:]:
            self.pheremones[(start,p)] += value
            start = p
            
            

            
     
"""        
def evaporate(self):
    for key,item in self.pheremones.items():
        val = max(min(self.max_level,item*self.evaporation_rate),self.min_level)
        self.pheremones[key] = val
"""
