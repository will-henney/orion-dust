
import numpy as np
import matplotlib.pyplot as plt
pixscale = {"acs": 0.0500016812098, "wfpc2": 0.0455214603946}
yscale = {"acs": 34.0, "wfpc2": 0.49}

ao_data_radius = np.linspace(0.01, 1.04, 20)
ao_data_major = np.array([
    0.06, 0.24, 0.39, 0.47, 0.56, 0.63, 0.67, 0.71, 0.74, 0.78, 0.83, 0.88, 0.91, 0.94, 0.98, 0.97, 0.98, 0.99, 1.00, 1.01
])
ao_std_major = np.array([
    0.0, 0.145, 0.12, 0.09, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00
])
ao_data_minor = np.array([
    0.075, 0.26, 0.42, 0.52, 0.65, 0.73, 0.82, 0.88, 0.92, 0.97, 0.97, 0.98, 0.985, 0.985, 1.00, 1.02, 1.01, 1.00, 1.00, 1.01
])

def get_xydata(s):
    x, y = np.loadtxt("{}-wcs.dat".format(s), unpack=True)
    return pixscale[camera]*(x - x0), y/yscale[camera]

NR = 41
rgrid = pixscale["acs"]*np.arange(NR) 
ymajor_list_grid = []
for i in range(NR):
    ymajor_list_grid.append(list())
yminor_list_grid = []
for i in range(NR):
    yminor_list_grid.append(list())

fig = plt.figure(figsize=(8,8))
fig.add_subplot(211)
camera = "acs"
for id_, x0 in [
        ["major-B06",  41.0], 
        ["major-R00L", 41.0], 
        ["major-R05L", 41.5], 
]:
    x, y = get_xydata(id_)
    print
    print camera, id_

    plt.bar(x, y, width=pixscale[camera], lw=0.0, color="k", align="center", alpha=0.1)
    plt.bar(x, 0.05*y, width=pixscale[camera], lw=0.0, color="k", align="center", alpha=0.2)
    if "B06" in id_:
        # Fit polynomial to BG sections
        m = (x < -1.0) | (x > 0.8)
        fit_major = np.poly1d(np.polyfit(x[m], y[m], 3))
        plt.plot(x, fit_major(x), color="k", alpha=0.5, lw=1)
    # Add into radial grid (always using ACS pixel size)
    for i, j in enumerate(abs(x/pixscale["acs"]).astype(int)):
        # save normalized brightness in a box according to the radius
        bright = y[i]/fit_major(x[i])
        print j, bright
        if j < NR:
            ymajor_list_grid[j].append(bright)

# Calculate statistics for major axis
ymajor_mean_grid = np.empty((NR,))
ymajor_std_grid = np.empty((NR,))
for j, ylist in enumerate(ymajor_list_grid):
    ymajor_mean_grid[j] = np.mean(ylist)
    ymajor_std_grid[j] = np.std(ylist)


camera = "wfpc2"
for id_, x0 in [
        ["major-wfpc2-R39", 44.0], 
]:
    x, y = get_xydata(id_)
    plt.plot(x, y, color="r", alpha=0.3)
    plt.plot(x, 0.05*y, color="r", alpha=0.6)

# Don't plot the flanking major profiles any more
# camera = "acs"
# for id_, x0 in [
#         ["major-top-R05L",  41.5], 
#         ["major-bot-R05L",  41.5], 
# ]:
#     x, y = get_xydata(id_)
#     plt.plot(x, y, color="k", alpha=0.3)

plt.text(-1.9, 1.25, "M42 218-354: major axis cuts")
plt.text(1.5, 0.1, "x 0.05")
plt.text(1.5, 1.1, "x 1.00")
plt.xlim(-2.0, 2.0)
plt.ylim(0.0, 1.4)
plt.grid(ls="-", alpha=0.3)
plt.ylabel("Surface brightness")

fig.add_subplot(212)
camera = "acs"
for id_, x0 in [
        ["minor-star-B06",  42.0], 
        ["minor-star-R00L", 41.0], 
        ["minor-star-R05L",  41.5], 
]:
    x, y = get_xydata(id_)
    # plt.plot(x, y, label=id_, drawstyle="steps-mid")
    plt.bar(x, y, width=pixscale[camera], lw=0.0, color="k", align="center", alpha=0.1)
    plt.bar(x, 0.05*y, width=pixscale[camera], lw=0.0, color="k", align="center", alpha=0.2)
    if "B06" in id_:
        # Fit polynomial to BG sections
        m = (x < -0.5) | (x > 0.5)
        fit_minor = np.poly1d(np.polyfit(x[m], y[m], 3))
        plt.plot(x, fit_minor(x), color="k", alpha=0.5, lw=1.5)
      # Add into radial grid (always using ACS pixel size)
    for i, j in enumerate(abs(x/pixscale["acs"]).astype(int)):
        # save normalized brightness in a box according to the radius
        bright = y[i]/fit_minor(x[i])
        print j, bright
        if j < NR:
            yminor_list_grid[j].append(bright)

# Calculate statistics for minor axis
yminor_mean_grid = np.empty((NR,))
yminor_std_grid = np.empty((NR,))
for j, ylist in enumerate(yminor_list_grid):
    yminor_mean_grid[j] = np.mean(ylist)
    yminor_std_grid[j] = np.std(ylist)

camera = "wfpc2"
for id_, x0 in [
        ["minor-wfpc2-R39", 45.5], 
]:
    x, y = get_xydata(id_)
    plt.plot(x, y, color="r", alpha=0.3)
    plt.plot(x, 0.05*y, color="r", alpha=0.6)

plt.text(-1.9, 1.25, "M42 218-354: minor axis cuts")
plt.text(1.5, 0.1, "x 0.05")
plt.text(1.5, 1.1, "x 1.00")
plt.xlim(-2.0, 2.0)
plt.ylim(0.0, 1.4)
plt.grid(ls="-", alpha=0.3)
plt.ylabel("Surface brightness")


figfile = "profiles-acs-218-354.pdf"
plt.xlabel("Offset, arcsec")
plt.legend()
fig.tight_layout()
plt.savefig(figfile)

figfile = "rprofiles-acs-218-354.pdf"
rfig = plt.figure(figsize=(8,8))
ymax = 1.4  

rfig.add_subplot(211)
plt.fill_betweenx([0.0, ymax], [0.32, 0.32], color="k", alpha=0.1) 
m = ymajor_std_grid < 0.5
plt.errorbar(ao_data_radius, ao_data_major, ao_std_major, fmt='bo', label="Magellan AO", zorder=3)
plt.errorbar(rgrid[m], ymajor_mean_grid[m], ymajor_std_grid[m], fmt='ro', label="HST-ACS", zorder=1)
# Add in WFPC2 as function of radius
camera = "wfpc2"
for id_, x0 in [
        ["major-wfpc2-R39", 44.0], 
]:
    x, y = get_xydata(id_)
    plt.plot(np.abs(x), y/fit_major(x), color="g", alpha=0.3, label="HST-WFPC2", zorder=2)
# finish WFPC2
plt.xlim(0.0, 1.4)
plt.ylim(0.0, ymax)
plt.grid(ls="-", alpha=0.3)
plt.legend(loc="center right", title="Major axis", fancybox=True, shadow=True)
plt.ylabel("Mean brightness profile")

rfig.add_subplot(212)
plt.fill_betweenx([0.0, ymax], [0.18, 0.18], color="k", alpha=0.1) 
m = yminor_std_grid < 10.0
p3, = plt.plot(ao_data_radius, ao_data_minor, 'bo')
p1, = plt.errorbar(rgrid[m], yminor_mean_grid[m], yminor_std_grid[m], fmt='ro')
# Add in WFPC2 as function of radius
camera = "wfpc2"
for id_, x0 in [
        ["minor-wfpc2-R39", 45.5], 
]:
    x, y = get_xydata(id_)
    p2, = plt.plot(np.abs(x), y/fit_minor(x), color="g", alpha=0.3)
# finish WFPC2
plt.xlim(0.0, 1.4)
plt.ylim(0.0, ymax)
plt.grid(ls="-", alpha=0.3)
plt.legend([p1, p2, p3], ["HST-ACS", "HST-WFPC2", "Magellan AO"], loc="center right", title="Minor axis", fancybox=True, shadow=True)
plt.xlabel("Radius, arcsec")
plt.ylabel("Mean brightness profile")

rfig.tight_layout()
plt.savefig(figfile)

# return figfile
