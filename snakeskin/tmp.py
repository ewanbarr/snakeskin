import sources as s
import optimiser as opt
import telescope as t

position = (0.1,0.1,"north")

field = s.fake_source_field()
telescopes = [t.telescope_from_config("../config/telescopes/MeerKAT.cfg") for _ in range(20)]
o = opt.AntColonyOptimiser(field)
o.add_telescopes(telescopes)
for _ in range(5):
    o.optimise(position)


import matplotlib.pyplot as plt

ax = plt.subplot(111)

for source in field:
    plt.scatter(source.ra,source.dec)

for a,b in o.pheremones.keys():
    if a is None or b is None:
        continue
    print a,b
    ra = [a.ra,b.ra]
    dec = [a.dec,b.dec]
    plt.plot(ra,dec,lw=o.pheremones[(a,b)]/1000.0,c="b")

plt.show()


