import numpy as np
import ephem as eph

class PheremoneLevels(dict):
    def __init__(self,default=0.5):
        super(PheremoneLevels,self).__init__()
        self.default = default

    def __missing__(self,key):
        self.__setitem__(key,self.default)
        return self.default

    def all_paths(self,start_node,nodes):
        return [self[(start_node,node)] for node in nodes]


class AntColonyOptimiser(object):
    def __init__(self,telescope,sources):
        self.telescopes = []
        self.sources = sources
        self.best_path = []
        self.best_score = 0
        self.evaporation_rate = 0.9
        self.score_multiplier = 500.0
        self.pheremone_weight = 1.0
        self.cost_weight = 1.0
        self.max_sources = 20
        self.max_duration = 18000
        self.pheremones = PheremoneLevels()
        
    def add_telescopes(self,telescopes):
        if hasattr(telescopes,"__iter__"):
            self.telescopes.extend(telescopes)
        else:
            self.telescopes.append(telescope)
    
    def probabilities(self,eta,tau):
        a = self.pheremone_weight
        b = self.cost_weight
        c = (eta**a + tau**b)
        return c/sum(c)
            
    def evaporate(self):
        for key,item in self.pheremones.items():
            val = item*self.evaporation_rate
            self.pheremones[key] = val

    def source_selector(self,current_source,sources,epoch):
        eta = np.array([source.attractiveness(epoch) for source in sources])
        tau = np.array([self.pheremones[(current_source,source)] for source in sources])
        probabilies = optimiser.probability(eta,tau)
        r,s = random.uniform(0, 1),0
        for idx,prob in enumerate(probabilies):
            s += prob
            if s >= r:
                return sources[idx]
        return sources[-1]

    def optimise(self,position,epoch=eph.now()):
        for telescope in self.telescopes:
            telescope.set_position(*position)
            telescope.travel(self,date=epoch)
            
        for telescope in telescopes:
            cost = self.calculate_cost(telescope)
            path = telescope.path
            self.update_pheremones(cost,path)
            
    def update_pheremones(self,cost,path):
        value = self.score_multiplier/cost
        start = path.pop()
        while path:
            next = path.pop()
            self.pheremones[(start,next)] += value
            start = next
            
        
        
        
        
        
        
        
        
def evaporate(self):
    for key,item in self.pheremones.items():
        val = max(min(self.max_level,item*self.evaporation_rate),self.min_level)
        self.pheremones[key] = val
