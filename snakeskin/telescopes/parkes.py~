from snakeskin.telescopes import AzAltMountTelescope
from numpy import pi
import ephem as eph

LATITUDE      = -0.536182599505178
LONGITUDE     = 0.37369244614450586
ELEVATION     = 1000.0
HORIZON       = 0.2617993877991494
ZENITH_LIMIT  = 1.53588974175501
NORTH_WRAP    = 4.799655442984406
SOUTH_WRAP    = -3.2288591161895095
AZ_SLEW_RATE  = 0.003490658503988659
ALT_SLEW_RATE = 0.0017453292519943295

class MeerKAT(AzAltMountTelescope):
    def __init__(self,az=0,alt=pi/2,wrap='north',date=eph.now()):
        super(MeerKAT,self).__init__(
            LATITUDE,
            LONGITUDE,
            ELEVATION,
            HORIZON,
            ZENITH_LIMIT,
            NORTH_WRAP,
            SOUTH_WRAP,
            AZ_SLEW_RATE,
            ALT_SLEW_RATE,
            az,
            alt,
            wrap)
        
