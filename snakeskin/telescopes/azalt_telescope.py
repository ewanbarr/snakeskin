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

    def drive_time(self,az,alt):
        if hasattr(az,"__iter__"):
            az = self.__unwrap_vector(az)
        else:
            az = self.__unwrap(az)
        
        az_drive_time = abs((self.az - az) * self.az_rate)
        alt_drive_time = abs((self.alt-alt) * self.alt_rate)
        return np.vstack((az_drive_time,alt_drive_time)).max(axis=0)

    def allure(self,sources):
        lmst = self.sidereal_time()
        az,alt = sources.azalt(self) #<--- need to cache these calls on source side
        response = self.sky_response(az,alt)
        return sources.value(self.date)*response
    
    
        
    
        
    
        
        
        
