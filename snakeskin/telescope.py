import ephem as eph
from ConfigParser import ConfigParser


class Telescope(eph.Observer):
    def __init__(self,lat,long,elevation,horizon):
        super(Telescope,self).__init__()
        self.lat = lat
        self.long = long
        self.elevation = elevation
        self.horizon = horizon
        self.compute_pressure()

    def set_epoch(self,epoch):
        self.epoch = epoch
    
    def set_position(self,az,elv):
        self.az = az
        self.elv = elv

        
class AzElvTelescope(Telescope):
    def __init__(self,lat,long,elevation,horizon,az_rate,elv_rate):
        super(AzElvTelescope,self).__init__(lat,long,elevation,horizon)
        self.wrap = 'north'
        self.az = None
        self.elv = None
        self.az_rate = az_rate
        self.elv_rate = elv_rate

    def set_position(self,az,elv,wrap='north'):
        super(AzElvTelescope,self).set_position(az,elv)
        self.wrap = wrap

    # drive_time = path segement cost
    def drive_cost(self,source_list):
        
        
        # convert to az elv
        # calculate rough drive time
        # calculate position at end of rough drive time
        # test if wrap crossed on drive (or wrap will be crossed on observation)
        # if wrap crossed, recalculate drive 
        # drive time is the metric used rather than drive distance
        # unless drive minimization required (a la Molonglo)
        pass
    
    def drive_to(self,source):
        source.compute(self)
        az0,az1 = self.az,source.az
        elv0,elv1 = self.elv,source.elv
        dist = min((az0-az1),(2*np.pi+az0-az1))
        self.total_az_dist += abs(self.az - source.az)
        

def dist(az0,az1,wrap="north"):
    wrap_limits = {
        "north":275.0,
        "south":175.0,
        "mid":50.0
        }
    wrap_switch = 50.0

    az0_ = az0 - 360 if az0 > 180 else az0
    az1_ = az1 - 360 if az1 > 180 else az1
    distance = az1_-az0_
    print distance, az1_, az0_
    print az0 , wrap_limits[wrap] , az0+distance

    if az0_ < wrap_switch < az1_:
        print "Wrap switch"

    if az0 < wrap_limits[wrap] < az0+distance:
        return -1*np.sign(distance) * (360-abs(distance))  
    else:
        return distance
        

    def travel(self,source_field,colony,max_sources=100,max_duration=10,epoch=eph.now()):
        exclusion_list = []
        self.total_az_dist = 0
        self.total_elv_dist = 0

        self.set_epoch(epoch)
        current_source = None
        
        sources = source_field.observable(self)
        sources = [source for source in sources if source not in exclusion_list]
        eta = [source.attractiveness(self.epoch) for source in sources]
        tau = [colony.pheremones[(current_source,source)] for source in sources]
        idx = colony.probability(eta,tau)
        source = sources[idx]
        exclusion_list.append(source)
        
        self.drive_to(source)
        self.observe(source)
        
        
        
        
        
    
        
    
def telescope_from_config(config_file):
    config = ConfigParser()
    pass