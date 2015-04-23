from snakeskin.telescopes import AzAltMountTelescope
from numpy import pi
import ephem as eph

LATITUDE      = -0.5759569078288767
LONGITUDE     = 2.5876652915795892
ELEVATION     = 324
HORIZON       = 0.5235987755982988
ZENITH_LIMIT  = 1.53588974175501
NORTH_WRAP    = 5.1487212933832724
SOUTH_WRAP    = -2.705260340591211
AZ_SLEW_RATE  = 0.03490658503988659
ALT_SLEW_RATE = 0.017453292519943295

class Parkes(AzAltMountTelescope):
    def __init__(self,az=0,alt=pi/2,wrap='north',date=eph.now()):
        super(Parkes,self).__init__(
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
        
