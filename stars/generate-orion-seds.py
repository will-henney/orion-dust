
"""
Generate Cloudy input files for some OB stars in Orion
"""

stars = dict(
    th1C = dict(T=39000., g=4.1, L=5.31),
    th1A = dict(T=30000., g=4.0, L=4.45),
    th1D = dict(T=32000., g=4.2, L=4.47),
    th1B = dict(T=18000., g=4.1, L=3.25),
    th1C2 = dict(T=25000., g=3.86, L=4.2),
    )

stars.update(
    iota = dict(T=32000., g=3.21, L=5.72),
    iotaB = dict(T=24000., g=3.52, L=4.57),
    HR1886 = dict(T=25400., g=3.62, L=4.57),
    HR1887 = dict(T=27700., g=3.78, L=4.58),
)

template = """\
title Spectrum of Orion star %(id)s using Tlusty
table star tlusty OBstar 3-dim %(T)i g=%(g).2f z=-0.1
luminosity total solar %(L).2f 
hden 4
radius 17
stop zone 1
save continuum file="%(id)s.cont"
"""

for star in stars:
    stars[star].update(id=star)
    with open(star + ".in", "w") as f:
        f.write(template % stars[star])
