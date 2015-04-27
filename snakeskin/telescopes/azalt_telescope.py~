from snakeskin.telescopes import BaseTelescope
import ephem as eph
import numpy as np
pi = np.pi

class AzAltMountTelescope(BaseTelescope):
    def __init__(self,
                 lat,
                 long,
                 elevation,
                 horizon,
                 zenith_limit,
                 north_wrap,
                 south_wrap,
                 az_rate,
                 alt_rate,
                 az=0.,
                 alt=0.,
                 wrap='north',
                 date=eph.now()):
        super(AzAltMountTelescope,self).__init__(lat,long,elevation,horizon,az,alt,date)
        self.zenith_limit = zenith_limit
        self.az_rate = az_rate
        self.alt_rate = alt_rate
        self.wrap_limits = {
            "north":north_wrap,
            "south":south_wrap,
            "mid": (south_wrap+pi*2+north_wrap)/2. - pi
            }
        self.wrap = 'north'

    def set_position(self,az,alt,wrap='north'):
        self.az = az
        self.alt = alt
        self.wrap = wrap
        
    def __unwrap_vector(self,az):
        az[(az>self.wrap_limits['north'])
           | ((az>self.wrap_limits['south']+pi*2)
              & (self.wrap=='north'))] -= pi
        return az
        
    def __unwrap(self,az):
        if az > self.wrap_limits["north"]:
            az -= pi*2
        elif az > self.wrap_limits["south"]+pi*2 and self.wrap == "north":
            az -= pi*2
        return az

    def __switch_wrap(self):
        if self.wrap == "north":
            self.wrap = "south"
        elif self.wrap == "south":
            self.wrap = "north"
        
    def __az_drive(self,az):
        if hasattr(az,"__iter__"):
            az = self.__unwrap_vector(az)
        else:
            az = self.__unwrap(az)
        unwrapped_az = self.__unwrap(self.az)
        return unwrapped_az,az

    def path_to(self,az,alt,npts=100):
        az0,az1= self.__az_drive(az)
        alt0,alt1 = self.alt,alt
        az_path = np.linspace(az0,az1,npts)
        alt_path = np.linspace(alt0,alt1,npts)
        return az_path,alt_path

    def drive_time(self,az,alt):
        az0,az1 = self.__az_drive(az)
        az_drive_time = abs((az0 - az1) / self.az_rate)
        alt_drive_time = abs((self.alt-alt) / self.alt_rate)
        return np.vstack((az_drive_time,alt_drive_time)).max(axis=0)
    
    def drive_to(self,source,tolerance=0.01):
        az0 = self.az
        super(AzAltMountTelescope,self).drive_to(source,tolerance)
        az1 = self.az
        mid = self.wrap_limits["mid"]
        if (az0 < mid < az1) or (az0 > mid > az1):
            self.__switch_wrap()
            
        
    
        
    
        
    
        
        
        
