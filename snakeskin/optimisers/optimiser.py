import numpy as np

class PheremoneLevels(dict):
    def __init__(self,default=0.5):
        super(PheremoneLevels,self).__init__()
        self.default = default

    def __missing__(self,key):
        self.__setitem__(key,self.default)
        return self.default

    def all_paths(self,start_node,nodes):
        return [self[(start_node,node)] for node in nodes]


class Optimiser(object):
    def __init__(self,telescope,sources):
        self.telescope = telescope
        self.sources = sources
        self.best_path = []
        self.best_score = 0


class AntColonySystem(object):
    def __init__(self,sources,telescope):
        super(Optimiser,self).__init__(sources,telescope)
        self.evaporation_rate = 0.9
        self.score_multiplier = 500.0
        self.pheremone_weight = 1.0
        self.cost_weight = 1.0
        self.min_level = 0.1
        self.max_level = 2.0
        self.pheremones = PheremoneLevels()

    def probabilities(self,phe,attr):
        a = self.pheremone_weight
        b = self.cost_weight
        c = (phe**a + attr**b)
        return c/sum(c)
            
    def evaporate(self):
        for key,item in self.pheremones.items():
            val = max(min(self.max_level,item*self.evaporation_rate),self.min_level)
            self.pheremones[key] = val

    def travel(self,nagents,max_epoch):
        # telescope agent at current epoch
        agent = self.telescope.create_agent(self.sources,self.pheremones)
        while epoch < max_epoch:
            epoch = agent.step()
        agent.update_pheremones()
            
            
        
    def optimise(self):
        # current epoch
        # this will be simulated from here on 
        simulator = self.telescope.get_simulator()
        sources = self.sources.visible(simulator)
        costs = simulator.costs(sources)
        self.init_pheremones(simulator,sources)

        


        
        
        
        
        
        
        
