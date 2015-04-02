import numpy as np
import ephem as eph
from ConfigParser import ConfigParser


class Telescope(eph.Observer):
    def __init__(self,lat,long,elevation,horizon):
        super(Telescope,self).__init__()
        self.lat = lat
        self.long = long
        self.elevation = elevation
        self.horizon = horizon
        self.dec_limit = lat + (np.pi-horizon)
        self.compute_pressure()

    def set_date(self,date):
        self.date = date
    
    def set_position(self,az,alt):
        self.az = az
        self.alt = alt

    def observe(self,source):
        self.date += source.estimated_tobs * SEC_TO_DAYS


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
        self.az_dist = 0
        self.alt_dist = 0
        self.duration = 0
    
    def reset(self):
        self.az_dist = 0
        self.alt_dist = 0
        self.duration = 0
        
    def set_position(self,az,alt,wrap='north'):
        super(AzAltTelescope,self).set_position(az,alt)
        self.wrap = wrap

    def estimate_drive(self,source):
        source.compute(self)
        az_dist = self._az_distance(source)
        alt_dist = self._alt_distance(source)
        az_time = az_dist / self.az_rate
        alt_time = alt_dist / self.alt_rate
        duration = max(az_time,alt_time)
        return az_dist,alt_dist,duration
    
    def drive_to(self,source):
        az_dist,alt_dist,duration = self.estimate_drive(source)
        self.date += duration * SEC_TO_DAYS
        self.az_dist += az_dist
        self.alt_dist += alt_dist
        self.duration += duration

    def _unwrap(self,az):
        if az > self.wrap_limits["north"]:
            az -= np.pi*2
        elif az > self.wrap_limits["south"]+np.pi*2 and self.wrap == "north":
            if self.wrap == "north":
                az -= np.pi*2
        return az

    def _az_distance(self,source):
        a = self._unwrap(self.az)
        b = self._unwrap(source.az)
        d = b - a
        if a < self.wrap_limits["mid"] < b:
            self.wrap = "south"
        elif a > self.wrap_limits["mid"] > b:
            self.wrap = "north"
        return d
        
    def _alt_distance(self,source):
        return source.alt - self.alt
    
    def travel(self,source_field,colony,max_sources=100,max_duration=36000,date=eph.now()):
        observed = []
        self.reset()
        self.set_date(date)
        
        current_source = None
        while self.duration < max_duration and source_count <= max_sources:
            sources = source_field.get_visible(self,exclude=observed)
            eta = [source.attractiveness(self.date) for source in sources]
            tau = [colony.pheremones[(current_source,source)] for source in sources]
            idx = colony.probability(eta,tau)
            current_source = sources[idx]
            observed.append(current_source)
            self.drive_to(current_source)
            self.observe(current_source)
        return observed
    
def telescope_from_config(config_file,n=1):
    config = ConfigParser()
    config.read(config_file)
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
        return AzAltTelescope(lat,lon,alt,hor,nwrap,swrap,az_rate,alt_rate)
    
