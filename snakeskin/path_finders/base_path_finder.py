import numpy as np

class BasePathFinder(object):
    def __init__(self,telescope,sources,pheremones,params):
        self.telescope = telescope
        self.sources = sources
        self.pheremones = pheremones
        self.parameters = params

    def __end_condition(self):
        return self.__observed.sum() == self.sources.size

    def __probability(self,pheremones,allure):
        a = self.parameters['pheremone_weight']
        b = self.parameters['allure_weight']
        n = pheremones**a * allure**b
        return n/n.sum()

    def __select(self,probs):
        r,s = np.random.uniform(0, 1),0
        for idx,prob in enumerate(probs):
            s += prob
            if s >= r:
                return idx
        return -1

    def __allure(self,az,alt,sources):
        dt = self.telescope.drive_time(az,alt)
        sky_weight = self.telescope.sky_response(az,alt)
        return sources.value * sky_weight / dt

    def __pheremones(self,current_idx,valid_idxs):
        keys = [(current_idx,idx) for idx in valid_idxs]
        return np.array([self.pheremones[key] for key in keys])

    def recorded_drive(self,source):
        az,alt = source.azalt(self.telescope)
        azpath,altpath = self.telescope.path_to(az,alt)
        self.telescope.drive_to(source,tolerance=0.01)
        return (azpath,altpath)
        
    def recorded_observation(self,source):
        az,alt = source.azalt(self.telescope,dt=source.tobs)
        azpath,altpath = self.telescope.path_to(az,alt)
        self.telescope.observe(source)
        return (azpath,altpath)
        
    def find_path(self):
        self.__observed = np.zeros(self.sources.size).astype('bool')
        up = np.zeros(len(self.sources)).astype('bool')
        current_idx = None        
        path = []
        while not self.__end_condition():
            sources = self.sources[~self.__observed]
            mask = self.telescope.observable(sources)
            sources = sources[mask]
            az,alt = sources.azalt(self.telescope)
            
            if sources.size == 0:
                self.telescope.progress_time(600.0)
                continue
            
            allure = self.__allure(az,alt,sources)
            pheremones = self.__pheremones(current_idx,sources.idx)
            probs = self.__probability(pheremones,allure)
            idx = self.__select(probs)
            current_idx = sources[idx].idx
            new_source = sources[idx].src_obj
            path.append(new_source)
            self.__observed[current_idx] = True
            self.telescope.drive_to(new_source)
            self.telescope.observe(new_source)
        return path
            
            
            
            
            
            
            
            
            
            
            
