import sys
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from bow_projection import (omega, paraboloid_R_theta,
                            wilkinoid_R_theta, cantoid_R_theta,
                            Spline_R_theta_from_function)

figfile = sys.argv[0].replace('.py', '.pdf')

sns.set_style('ticks')
fig, ax = plt.subplots()

th = np.linspace(0.0, np.pi, 501)
th_dg = np.degrees(th)

for label, func, pars, ngrid, epsilon in [
        ["paraboloid", paraboloid_R_theta, (), 301, 1e-3],
        ["Wilkinoid", wilkinoid_R_theta, (), 101, 1e-6],
        [r"Cantoid $\beta = 0.001$", cantoid_R_theta, (0.001,), 101, 1e-6],
        [r"Cantoid $\beta = 0.01$", cantoid_R_theta, (0.01,), 101, 1e-6],
        [r"Cantoid $\beta = 0.1$", cantoid_R_theta, (0.1,), 101, 1e-6],
]:
    spline_func = Spline_R_theta_from_function(
        ngrid=ngrid, epsilon=epsilon,
        shape_func=func, shape_func_pars=pars)
    ax.plot(th_dg, omega(th, spline_func), label=label)
    ax.plot(th_dg, omega(th, func, *pars), color='b', alpha=0.2, lw=2, label='_nolabel_')

ax.legend(title=r"Spline approximations")
ax.axhline(1.0, xmin=0.35, xmax=0.65, color='white', lw=4, zorder=100)
ax.axhline(1.0, xmin=0.35, xmax=0.65, color='k', lw=1, ls=':', zorder=101)
ax.axhspan(0.0, 1.0, color='k', alpha=0.05, ec='none')
ax.set_yscale('symlog', linthreshy=1.0, linscaley=0.5)
ax.set(
    xlabel=r"Polar angle: $\theta$, degrees",
    ylabel=r"$\omega \equiv R^{-1} d R / d \theta$",
    xlim=[0, 180],
    ylim=[0.0, 2e2],
    xticks=[0, 30, 60, 90, 120, 150, 180],
)
sns.despine()
fig.tight_layout()
fig.savefig(figfile)
print(figfile, end='')
