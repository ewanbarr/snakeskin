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

    # DJD epoch
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
    def drive_time(self,ra,dec,epoch,tobs=600.0):
        # convert to az elv
        # calculate rough drive time
        # calculate position at end of rough drive time
        # test if wrap crossed on drive (or wrap will be crossed on observation)
        # if wrap crossed, recalculate drive 
        # drive time is the metric used rather than drive distance
        # unless drive minimization required (a la Molonglo)
        pass
        
    
def telescope_from_config(config_file):
    config = ConfigParser()
    pass
