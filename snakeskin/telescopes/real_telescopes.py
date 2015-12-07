from snakeskin.telescopes import AzAltMountTelescope
from numpy import pi
import ephem as eph

class MeerKAT(AzAltMountTelescope):
    def __init__(self,az=0,alt=pi/2,wrap='north',date=eph.now()):
        super(MeerKAT,self).__init__(
            -0.536182599505178, #lat
             0.37369244614450586, #long
             1000.0, #elv
             0.2617993877991494, #horizon
             1.53588974175501, #zenith limit
             4.799655442984406, #north wrap
             -3.2288591161895095, #south wrap
             0.003490658503988659, #az slew rate 
             0.0017453292519943295, #alt slew rate
             az,
             alt,
             wrap)
        
class Parkes(AzAltMountTelescope):
    def __init__(self,az=0,alt=pi/2,wrap='north',date=eph.now()):
        super(Parkes,self).__init__(
            -0.5759569078288767,
             2.5876652915795892,
             324,
             0.5235987755982988,
             1.53588974175501,
             5.1487212933832724,
             -2.705260340591211,
             0.03490658503988659,
             0.017453292519943295,
             az,
             alt,
             wrap)
