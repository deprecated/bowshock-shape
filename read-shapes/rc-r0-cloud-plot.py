import json
import glob
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as colors

shelldata = json.load(open("../rc-r0.json"))

params = {
    "font.family": "serif",
    "text.usetex": True,
    "text.latex.preamble": [r"\usepackage[varg]{txfonts}"],
    "figure.figsize": (5, 5),
}
matplotlib.rcParams.update(params)

lw = dict(isotropic=1, proplyd=2)
opacity = dict(isotropic=0.3, proplyd=0.7)

#colors = "bgrmkcy"

#sort beta in ascending order
beta_keys = shelldata["proplyd"].keys()
beta =[]
for b in beta_keys:
    beta.append(float(b))
#******************
# Counting the number of curves for obtaining the color of the curves
beta = sorted(beta,reverse=True)
Ncurves = len(beta)
values = range(Ncurves)
#********************
# Setting colormap
colmap = plt.get_cmap("Purples")
cNorm = colors.Normalize(vmin=-1,vmax = values[-1])
scalarMap = cmx.ScalarMappable(norm=cNorm,cmap=colmap)
#**********************
#plot model data
for inn in shelldata.keys():
    for b in beta:
        inclinations = np.array(shelldata[inn][str(b)]["inc"])
        R0 = np.array(shelldata[inn][str(b)]["R0'"])
        Rc = np.array(shelldata[inn][str(b)]["Rc"])
        colorVal = scalarMap.to_rgba(values[beta.index(b)]) # assign color to each beta value
        
        # Mask to select inclinations close to multiples of 15 degrees
        every15 = np.zeros(R0.shape, dtype=bool)
        for thisinc in 0.0, 15.0, 30.0, 45.0, 60.0, 75.0:
            iclosest = np.argmin(np.abs(np.degrees(inclinations) - thisinc))
            every15[iclosest] = True

        label = r'\(\beta={:.3f}\)'.format(b) if inn == "proplyd" else ""
        Y = Rc/R0
        # First, plot a line with all the inclinations
        plt.plot(R0, Y, '-', linewidth=lw[inn], c=colorVal, 
                 label=label, alpha=opacity[inn])
        # Second, add symbols every 15 degrees
        plt.plot(R0[every15], Y[every15], '.', c=colorVal, alpha=opacity[inn])



# Add the observations to the plot
#Collection of hex colors
dark_blue = "#1e25b6"
pearl_turquoise ="#32c6a6"
mexican_pink = "#e4007c"
crimson = "#dc143c"
leaf_green = "#15ae26"
brown = "#b6451e"
gray = "#515952"
guinda = "#aa1c47"
gold = "#FFD700"
orange = "#E08000"
#Create a dictionary with hex colors for the objects
colordict = {"LV2":dark_blue,"LV2b":pearl_turquoise,"LV3":mexican_pink,"LV4":crimson,"LV5":brown,
             "168-328":leaf_green,"169-338":gray,"177-341":guinda,"180-331":orange}

# # get all the savefiles of samples
# savefiles = glob.glob("./Multi-Fit/samp*/*.save")
# for savefile in savefiles:
#     data = json.load(open(savefile))
#     plt.plot(data["R0"],data["Rc"]/data["R0"],color=colordict[data["proplyd"]],marker="*")

#plot the main poins (without removing points in the shell in the *.reg files)

m_savefiles = glob.glob("LV-bowshocks-xyfancy-positionswill-*.save")
dict_xtext = {"LV2":10,"LV2b":-10,"LV3":10,"LV4":10,"LV5":10,"168-328":-10,"169-338":-10,"177-341":10,"180-331":-20}
dict_ytext = {"LV2":10,"LV2b":10,"LV3":-10,"LV4":10,"LV5":10,"168-328":10,"169-338":10,"177-341":-10,"180-331":-20}
for savefile in m_savefiles:
    data = json.load(open(savefile))
    combined_file = savefile.replace('positionswill', 'variations')
    vardata = json.load(open(combined_file))
    plt.plot(data["R0"],data["Rc"]/data["R0"],
             # color=colordict[data["proplyd"]],
             color='k',
             marker="o")
    plt.annotate(data["proplyd"], xy=(data["R0"],data["Rc"]/data["R0"]),
                 xytext=(dict_xtext[data["proplyd"]], dict_ytext[data["proplyd"]]),
                 textcoords="offset points", fontsize="xx-small",
                 bbox=dict(boxstyle='round,pad=0.5',
                           fc=colordict[data["proplyd"]],
                           alpha=0.5))
    # Plot the variations of the fits with points removed
    R0 = data["R0"]
    A = data["Rc"]/data["R0"]
    var_R0 = vardata["R0"]
    var_A = np.array(vardata["Rc"])/np.array(vardata["R0"])
    for vR0, vA in zip(var_R0, var_A):
        # Scale gives fractional deviation from typical value
        scale = np.hypot((vR0 - R0)/0.25, (vA - A)/1.5)
        alpha = 1./(1 + 20.0*scale)
        plt.plot([R0, vR0], [A, vA], '-',
                  lw=2, alpha=alpha, color=colordict[data["proplyd"]])
    # plt.plot(vardata["R0"], np.array(vardata["Rc"])/np.array(vardata["R0"]),
    #          '*', 
    #          color=colordict[data["proplyd"]])

#for pset, color,colorbox in [
 #       ["best", 'ko','yellow'],
 #       ["best45", 'ro','blue']
#]:
 #   pdata = np.genfromtxt(pset + "-proplyds.dat", names=True, dtype=None)
 #   plt.errorbar(pdata["R0D"], pdata["RcR0"],
 #                xerr=pdata["ER0D"], yerr=pdata["ERcR0"],
 #                fmt=color, label="", alpha=1.0)
 #   for label, x, y, dx, dy in zip(
 #           pdata["Proplyd"], pdata["R0D"], pdata["RcR0"],
 #           pdata["dx"], pdata["dy"]):
 #       ha = "right" if dx < 0 else "left"
 #       va = "top" if dy < 0 else "bottom"
 #       plt.annotate(
 #           "{}".format(label),
 #           xy=(x, y), xytext=(dx, dy), fontsize="xx-small", alpha=1.0,
 #           textcoords = 'offset points', ha = ha, va = va,
 #           bbox=dict(boxstyle='round,pad=0.5', fc=colorbox, alpha=0.5),
 #           arrowprops = dict(arrowstyle='->', connectionstyle='arc3,rad=0')
 #       )


plt.xlabel(r"\(R'_0 / D'\)")
# avoid numbering the origin
epsilon = 1.e-6
plt.xlim(0.0 + epsilon, 0.5)
plt.ylim(0.0 - epsilon, 4 + epsilon)
plt.ylabel(r"\(R'_{c} / R'_0\)")
plt.legend(loc="best", ncol=2, prop=dict(size="x-small"))

plt.title("Curvature radii versus parallel bowshock radii")
plt.savefig("proplyd-shell-R0-Rc-cloud.pdf")
