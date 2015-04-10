import numpy as np
import ephem as eph
from ConfigParser import ConfigParser
from functools import partial
from utils import *
from pprint import pformat
import logging
logging.basicConfig(level=logging.INFO)

#3.9425754969908628

SIDEREAL_SECONDS_PER_SECOND = 0.9972621011166376

@observable
class Telescope(eph.Observer):
    def __init__(self,lat,long,elevation,horizon):
        super(Telescope,self).__init__()
        self.lat = lat
        self.long = long
        self.elevation = elevation
        self.horizon = horizon
        self.dec_limit = lat + (np.pi-horizon)
        self.compute_pressure()

    def set_date(self,date=eph.now()):
        self.date = date
    
    def progress_time(self,seconds):
        self.date += seconds * SEC_TO_DAYS

    def set_position(self,az,alt):
        self.az = az
        self.alt = alt

    def observe(self,source):
        self.progress_time(source.maximum_tobs)

class AzAltTelescope(Telescope):
    def __init__(self,lat,long,elevation,horizon,north_wrap,south_wrap,az_rate,alt_rate,az_cost,alt_cost):
        super(AzAltTelescope,self).__init__(lat,long,elevation,horizon)
        self.log = logging.getLogger(self.__class__.__name__)
        self.az_rate = az_rate
        self.alt_rate = alt_rate
        self.az_drive_cost = az_cost
        self.alt_drive_cost = alt_cost
        midwrap = ((south_wrap+np.pi*2)+north_wrap)/2. - np.pi
        self.wrap_limits = {
            "north":north_wrap,
            "south":south_wrap,
            "mid":midwrap
            }
        self.wrap = 'north'
        self.az = None
        self.alt = None
        self.last_tour = None

    def set_position(self,az,alt,wrap):
        super(AzAltTelescope,self).set_position(az,alt)
        self.wrap = wrap

    def get_maintenance_cost(self,az_dist,alt_dist):
        a = az_dist * self.az_drive_cost
        b = alt_dist * self.alt_drive_cost
        return a+b

    def drive_to(self,source,simulate=False):
        source.compute(self)
        az_dist,wrap = self._az_distance(source,self.wrap)
        alt_dist = self._alt_distance(source)
        az_time = az_dist / self.az_rate
        alt_time = alt_dist / self.alt_rate
        duration = max(az_time,alt_time)
        if not simulate:
            self.progress_time(duration)
            source.compute(self)
            self.wrap = wrap
            self.az = source.az
            self.alt = source.alt
        return az_dist,alt_dist,duration

    def observe(self,source):
        self.progress_time(source.maximum_tobs)
        source.compute(self)
        self.az = source.az
        self.alt = source.alt

    def _unwrap(self,az,start_wrap):
        if az > self.wrap_limits["north"]:
            az -= np.pi*2
        elif az > self.wrap_limits["south"]+np.pi*2 and start_wrap == "north":
            if start_wrap == "north":
                az -= np.pi*2
        return az
    
    def _az_distance(self,source,start_wrap):
        a = self._unwrap(self.az,start_wrap)
        b = self._unwrap(source.az,start_wrap)
        d = b - a
        if a < self.wrap_limits["mid"] < b:
            end_wrap = "south"
        elif a > self.wrap_limits["mid"] > b:
            end_wrap = "north"
        else:
            end_wrap = start_wrap
        return abs(d),end_wrap
        
    def _alt_distance(self,source):
        return abs(source.alt - self.alt)
    
    def travel(self,start_pos,start_date,optimiser):
        self.az,self.alt,self.wrap = start_pos
        observed = []
        tour = []
        field = optimiser.sources
        model = optimiser.model
        end_date = self.date + model.max_duration * SEC_TO_DAYS
        current_source = None

        self.log.debug("Starting travel")
        self.log.debug("Start position: %s"%(repr(start_pos)))
        self.log.debug("Start date: %s"%(self.date))
        self.log.debug("End date: %s"%(eph.date(end_date)))
        self.log.debug("Model: %s"%(repr(model)))

        while self.date < end_date and len(observed) <= model.max_sources:
            self.log.debug("Calculating possible paths")
            self.date = start_date
            start_pos = self.az,self.alt,self.wrap
            sources = field.get_visible(self,exclude=observed)
            
            self.log.debug("Number of available targets: %d"%len(sources))
            self.log.debug("Targets: %s"%(",".join([i.name for i in sources])))
            
            if not sources:
                break

            possible_paths = []
            for source in sources:
                
                self.log.debug("Calculating parameters of path to %s"%source.name)
                path = AttrDict()
                path.origin = current_source
                path.target = source
                path.start_date= self.date
                path.pre_drive_pos = self.az,self.alt,self.wrap
                
                self.az,self.alt,self.wrap = start_pos
                az_dist,alt_dist,duration = self.drive_to(source,simulate=True)
                path.pre_obs_pos = source.az,source.alt,self.wrap
                
                self.log.debug("Az, Alt distances: %s"%(str((az_dist,alt_dist))))
                self.log.debug("Drive time: %f"%duration)

                path.drive_time = duration
                path.maintenance_cost = self.get_maintenance_cost(az_dist,alt_dist)

                self.log.debug("Maintenance cost: %f"%path.maintenance_cost)

                obs_djd = self.date + duration * SEC_TO_DAYS
                
                self.log.debug("Obs date: %s"%obs_djd)
                
                path.obs_start_date = obs_djd
                
                self.log.debug("Path stats: %s"%pformat(path))
                
                possible_paths.append(path)
                
            path = optimiser.select_path(possible_paths)
            current_source = path.target
            self.drive_to(current_source)
            path.pre_obs_pos = self.az,self.alt,self.wrap
            self.observe(current_source)
            path.post_obs_pos = self.az,self.alt,self.wrap
            path.obs_end_date = self.date
            start_date = self.date
            tour.append(path)
            observed.append(current_source)
        self.last_tour = tour

    

def create_telescope(config):
    lat = config.getfloat("location","latitude")
    lon = config.getfloat("location","longitude")
    alt = config.getfloat("location","elevation")
    hor = config.getfloat("location","horizon")
    
    mount = config.get("type","mount")
    
    if mount == "azel":
        nwrap = config.getfloat("parameters","north_wrap")
        swrap = config.getfloat("parameters","south_wrap")
        az_rate = config.getfloat("parameters","az_drive_rate")
        alt_rate = config.getfloat("parameters","alt_drive_rate")
        max_alt = config.getfloat("parameters","max_alt")
        min_alt = config.getfloat("parameters","min_alt")
        az_cost = config.getfloat("parameters","az_drive_cost")
        alt_cost = config.getfloat("parameters","alt_drive_cost")
        return AzAltTelescope(lat,lon,alt,hor,nwrap,swrap,az_rate,alt_rate,az_cost,alt_cost)
    else:
        raise NotImplemented(mount)

