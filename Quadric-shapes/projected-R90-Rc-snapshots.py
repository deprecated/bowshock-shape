import sys
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker
import seaborn as sns

plotfile = sys.argv[0].replace('.py', '.pdf')

sns.set_style('ticks')
fig, axes = plt.subplots(3, 3, figsize=(9, 9), sharex=True, sharey=True)

incs_deg = 10.0*np.arange(9)

ny, nx = 55, 55
Rcs = np.linspace(0.5, 7.0, nx)
R90s = np.linspace(0.5, 7.0, ny)[::-1]
Rc_grid = Rcs[None, :]*np.ones_like(R90s[:, None])
R90_grid = R90s[:, None]*np.ones_like(Rcs[None, :])
Tc_grid = 2*Rc_grid - R90_grid**2

cols = sns.color_palette('magma', n_colors=ny)


def Rc_prime(inc, Tc, Rc):
    f = np.sqrt(1.0 + Tc*np.tan(inc)**2)
    return Rc * (1 + np.tan(inc)**2) / f / (1.0 + Rc*(f - 1.0) / Tc)

def Tc_prime(inc, Tc):
    fsquared = 1.0 + Tc*np.tan(inc)**2
    return Tc * (1.0 + np.tan(inc)**2) / fsquared

def R90_prime(inc, Tc, Rc):
    return np.sqrt(2*Rc_prime(inc, Tc, Rc) - Tc_prime(inc, Tc))

def qratio(inc, Tc, Rc):
    f = np.sqrt(1.0 + Tc*np.tan(inc)**2)
    return (1.0 + Rc*(f - 1.0) / Tc)*np.cos(inc)


for ax, inc_deg in zip(axes.flat, incs_deg):

    Rc_grid2 = np.linspace(0.0, 10.0, 2000)
    R90_T0_grid = np.sqrt(2*Rc_grid2)
    R90_T1_grid = np.sqrt(2*Rc_grid2 - 1.0)
    R90_T1_grid[~np.isfinite(R90_T1_grid)] = 0.0 
    ax.fill_between(Rc_grid2, R90_T1_grid, R90_T0_grid, color='k', alpha=0.2)
    ax.fill_between(Rc_grid2, R90_T0_grid, color='k', alpha=0.1)
    ax.plot(Rc_grid2, R90_T0_grid, c='k', lw=0.5)
    ax.axhline(1.0, lw=0.5, alpha=0.5, color='k', zorder=-1)
    ax.axvline(1.0, lw=0.5, alpha=0.5, color='k', zorder=-1)
    ax.plot([0.0, 10.0], [0.0, 10.0], lw=0.5, alpha=0.5, color='k', zorder=-1)

    inc = np.radians(inc_deg)
    Rcp = Rc_prime(inc, Tc_grid, Rc_grid).ravel()
    R90p = R90_prime(inc, Tc_grid, Rc_grid).ravel()
    R0p = qratio(inc, Tc_grid, Rc_grid).ravel()

    ax.scatter(Rcp, R90p, c=Tc_grid.ravel(), s=15*R0p,
	       vmin=Tc_grid.min(), vmax=Tc_grid.max(),
	       edgecolors='none',
	       cmap='magma', marker='.', alpha=0.8)
    # ax.axhspan(0.0, 10.0, alpha=0.1, facecolor='k', zorder=-1)
    # ax.axhline(1.0, ls='--', lw=0.5, c='k', zorder=0)
    # ax.axvline(1.0, ls='--', lw=0.5, c='k', zorder=0)
    ax.plot([1.0], [1.0], 'x', c='k')
    ax.text(5.5, 0.5, rf'$i = {inc_deg:.0f}^\circ$',
            bbox={'facecolor': 'w', 'alpha': 0.8, 'edgecolor': 'none'})

axes[-1, 0].set(
    yscale='linear',
    xlim=[0.0, 8.1],
    ylim=[0.0, 8.1],
    xticks=range(9),
    yticks=range(9),
    xlabel=r"$\Pi'$",
    ylabel=r"$\Lambda'$",
)        

sns.despine()
fig.tight_layout()
fig.savefig(plotfile, dpi=300)
print(plotfile, end='')
