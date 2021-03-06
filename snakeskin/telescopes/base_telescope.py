import ephem as eph
import numpy as np
from snakeskin.constants import SEC_TO_DAYS


class BaseTelescope(eph.Observer):
    def __init__(self, 
                 lat,
                 long,
                 elevation,
                 horizon,
                 az=0.,
                 alt=0.,
                 date=eph.now()):
        super(BaseTelescope,self).__init__()
        self.lat = lat
        self.long = long
        self.elevation = elevation
        self.horizon = horizon
        self.az = az
        self.alt = alt
        self.date = date
        self.compute_pressure()
        self.init_params = {
            "date":self.date,
            "az":self.az,
            "alt":self.alt
            }

    def reset(self):
        for key,val in self.init_params.items():
            self.__setattr__(key,val)
        
    def set_position(self,az,alt):
        self.az = az
        self.alt = alt
        
    def set_date(self,date):
        self.date = date

    def progress_time(self,seconds):
        self.date += seconds * SEC_TO_DAYS

    def reverse_time(self,seconds):
        self.date -= seconds * SEC_TO_DAYS
        
    def drive_time(self,az,alt):
        return np.ones(len(az))

    def path_to(self,az,alt,npts=2):
        azpath = np.array([self.az,az])
        altpath = np.array([self.alt,alt])
        return azpath,altpath
    
    def is_close(self,az,alt,tolerance=0.01):
        d = np.sqrt((self.az-az)**2 + (self.alt-alt)**2)
        return d<tolerance
        
    def drive_to(self,source, tolerance=0.01):
        az,alt = source.azalt(self)
        while not self.is_close(az,alt,tolerance):
            dt = self.drive_time(az,alt)
            self.progress_time(dt)
            self.set_position(az,alt)
            az,alt = source.azalt(self)

    def observe(self,source):
        self.progress_time(source.tobs)
        az,alt = source.azalt(self)
        self.set_position(az,alt)
    
    def sky_response(self,az,alt):
        return np.ones(len(az))
    
    def visible(self,az,alt):
        return alt > self.horizon



