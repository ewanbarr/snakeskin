import ephem as eph
from numpy import pi

SEC_TO_DAYS = 1/86400.

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
                
    def set_position(self,az,alt):
        self.az = az
        self.alt = alt
        
    def set_date(self,date):
        self.date = date

    def progress_time(self,seconds):
        self.date += seconds * SEC_TO_DAYS
        
    def drive_time(self,az,alt):
        if hasattr(az,"__iter__"):
            return np.ones(len(sources))
        else:
            return 1
        
    def drive_to(self,source):
        az,alt = source.azalt(self)
        dt = self.drive_time(az,alt)
        self.progress_time(dt)
        self.set_position(az,alt)
                
    def observe(self,source):
        self.progress_time(source.tobs)
        az,alt = source.azalt(self)
        self.set_position(az,alt)
    
    def sky_response(self,az,alt):
        return 1
    
    def observable(self,sources):
        az,alt = sources.azalt(self)
        mask = alt>self.horizon
        return sources[mask],az[mask],alt[mask]

