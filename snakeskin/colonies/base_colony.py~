from multiprocessing import Process

DEFAULT_MODEL = {"num_agents":20}

class BaseColony(object):
    def __init__(self,sources,telescope,path_finder,pheremones,model=None):
        self.sources = sources
        self.telescope = telescope
        self.path_finder = path_finder
        self.pheremones = pheremones
        self.model = DEFAULT_MODEL.copy()
        if model is not None:
            self.model.update(model)
        self.best_path = None
        self.best_score = 0.0

    def iterate(self):
        path_costs = []
        for ii in range(self.model['num_agents']):
            path_costs.append(self.deploy_ant())
        for path,cost in path_costs:
            self.pheremones.deposit(path,cost)
        self.pheremones.evaporate()

    def deploy_ant(self):
        self.telescope.reset()
        path,cost = self.path_finder.find_path()
        score = 1./cost
        if score > self.best_score:
            self.best_score = score
            self.best_path = path
        return path,cost
        
        

        
        
        
