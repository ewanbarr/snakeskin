import numpy as np
import ephem as eph
from ConfigParser import ConfigParser
from functools import partial
from utils import *

DTYPE = [ ("source","object"),
          ("maintenance_cost","float32"),
          ("drive_time","float32"),
          ("obs_date","float32"),
          ("value","float32"),
          ("attractiveness","float32"),
          ("pheremone_level","float32"),
          ("start_az","float32"),
          ("end_az","float32"),
          ("start_alt","float32"),
          ("end_alt","float32")]


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
    def __init__(self,lat,long,elevation,horizon,north_wrap,south_wrap,az_rate,alt_rate):
        super(AzAltTelescope,self).__init__(lat,long,elevation,horizon)
        self.az_rate = az_rate
        self.alt_rate = alt_rate
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
    
    def travel(self,start_pos,epoch,optimiser):
        self.az,self.alt,self.wrap = start_pos
        self.date = epoch

        observed = []
        tour = []
        field = optimiser.sources
        model = optimiser.model
        current_source = None

        while self.duration < model.max_duration and len(observed) <= model.max_sources:
            
            start_date = self.date
            start_pos = self.az,self.alt,self.wrap
            sources = field.get_visible(self,exclude=observed)
            possible_paths = []
            
            for source in sources:
                path = AttrDict(origin=current_source,target=source,start_date=self.date)
                self.az,self.alt,self.wrap = start_pos
                az_dist,alt_dist,duration = self.drive_to(source,simulate=True)
                path.drive_time = duration
                path.maintenance_cost = self.get_maintenance_cost(az_dist,alt_dist)
                obs_djd = self.date + duration * SEC_TO_DAYS
                path.obs_start_date = obs_djd
                possible_paths.append(path)
                
            path = optimiser.select_path(possible_paths)
            current_source = path.target
            path.start_wrap = self.wrap
            self.drive_to(current_source)
            self.observe(current_source)
            path.end_wrap = self.wrap
            path.obs_end_date = self.date
            tour.append(path)
            observed.append(current_source)
        self.last_tour = tour

    
def telescope_params_from_config(config_file):
    config = ConfigParser()
    config.read(config_file)
    return config

def create_telescope(config)
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
        return partial(AzAltTelescope,lat,lon,alt,hor,nwrap,swrap,az_rate,alt_rate)
    else:
        raise NotImplemented(mount)

    def telescope_from_config(config_file):
        return telescope_type_from_config(config_file)()
    
