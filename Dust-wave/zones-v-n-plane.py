import sys
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from vec_root import chandrupatla

figname = sys.argv[0].replace('.py', '.pdf')

sns.set_style('ticks')
sns.set_color_codes('dark')
fig, axes = plt.subplots(1, 3, sharex=True, sharey=True, figsize=(8, 4))
stardata = [
    [10.0, 0.63, 0.0026, 1e-4, axes[0]],
    [20.0, 5.5, 0.0446, 0.1, axes[1]],
    [40.0, 22.0, 0.1682, 1.0, axes[2]],
]

# Velocities in units of km/s (10 km/s -> 100 km/s)
vgrid = np.linspace(10.0, 100.0, 800)
# Densities in units of 1 pcc  (0.01 -> 1e5)
logngrid = np.linspace(-3.3, 6.3, 800)
# 2d versions of velocity and density grids
vv, nn = np.meshgrid(vgrid, 10**logngrid)

def rstar(v10, n, L4):
    """Characteristic radius in pc"""
    return 2.21*np.sqrt(L4/n)/v10

def taustar(v10, n, L4, kappa600=1.0):
    """Characteristic optical depth"""
    return 0.0089*kappa600*np.sqrt(L4*n)/v10

def xfunc(x, ts, eta):
    """Function to be zeroed to find x"""
    return x**2 - (1.0 - np.exp(-2*ts*x)) - eta

R0s = (0.0003, 0.001, 0.003, 0.01, 0.03,
       0.1, 0.3, 1.0, 3.0, 10.0, 30.0)
lws = np.linspace(0.3, 2.5, len(R0s))
cformats = { 0.0001: "0.0001 pc", 0.001: "0.001 pc", 0.01: "0.01 pc", 0.1:
             "0.1 pc", 1.0: "1 pc", 10.0: "10 pc", }
clevs_to_label = list(cformats.keys())

box_params = dict(fc='w', ec='0.8', lw=0.4, pad=2)
RBW_label = r"Radiation bow wave, $\eta < \tau < 1$"
RBS_label = r"Radiation bow shock, $\tau > 1$"
WBS_label = r"Wind bow shock, $\tau < \eta$"

# Miscellaneous panel-dependent plot params
d = {
    "trapped y": {10.0: 1.6e4, 20.0: 4.0e4, 40.0: 3.0e4},
    "trapped bg": {10.0: '0.85', 20.0: 'w', 40.0: 'w'},
}

T0 = 8000
for M, L4, eta, S49, ax in stardata:
    Mlabel = "\n".join([rf"$M = {M:.0f}\, M_\odot$",
                        rf"$L = {1e4*L4:.1e}\, L_\odot$".replace("e+0", r"\times 10^"),
                        rf"$\eta = {eta}$"])
    Rs = rstar(vv/10, nn, L4)
    ts = taustar(vv/10, nn, L4)
    a, b = 0.0, 2*np.sqrt(1.0 + eta)
    x = chandrupatla(xfunc, a, b, args=(ts, eta))
    R0 = x*Rs
    tau = 2*x*ts

    # Ionization parameter - fiducial
    U = 2.789*S49 / (R0**2 * nn)
    # Shell ionization parameter - assume compression by M^2
    Ush = U/(vv/10)**2
    # Ionization fraction in shell
    ysh = 1.0 - 1.0/(3.5e5*Ush)

    # cs = ax.contour(vv, nn, ysh,
    #                 (0.9, 0.99, 0.999, 0.9999, 0.99999),
    #                 linewidths=1.0,
    #                 colors='g', alpha=0.5)
    # ax.clabel(cs,
    #           fontsize=5, colors='g', fmt='$%.5f$', 
    #           inline=True, inline_spacing=1, use_clabeltext=True)
    # ax.text(75, 6e-3, fr"$y_\mathrm{{in}} = {ysh.max():.5f}$",
    #         fontsize=5, color='g', alpha=0.5)
    # ax.text(12, 1.3e6, fr"$y_\mathrm{{in}} = {ysh.min():.5f}$",
    #         fontsize=5, color='g', alpha=0.5)

    # Fraction of ionizing photons absorbed in shell
    absfrac = 2.56e-5 * (vv/10)**2 * nn**2 * R0**3 / S49
    # Equivalent optical depth
    tau_gas = -np.log(1.0 - absfrac)
    #absfrac = 2.76e-4 * (vv/10)**-1 * nn**0.5 * (L4)**1.5 / S49

    # Ionization parameter just outside the shell
    Uout = U*np.exp(-(tau + tau_gas))
    Uout[~np.isfinite(Uout)] = 0.0
    Ushout = Uout/(vv/10)**2

    # y^2 / (1 - y) = CU
    # y = 0.1 => y^2 / (1 - y) = 0.0111111111111
    # y = 0.5 => y^2 / (1 - y) = 0.5
    # y = 0.9 => y^2 / (1 - y) = 8.1
    # y = 0.99 => y^2 / (1 - y) = 98.1

    # cu = 3.5e5*Uout

    # y_out = 0.5*cu * (np.sqrt(1.0 + 4/cu) - 1.0)
    # cs = ax.contour(vv, nn, Uout,
    #                 np.logspace(-7.0, 1.0, 9),
    #                 linewidths=np.linspace(0.2, 1.5, 9),
    #                 colors='r', alpha=0.5)
    # ax.clabel(cs,x
    #           fontsize='xx-small', colors='r', fmt='%.0e', 
    #           inline=True, inline_spacing=1, use_clabeltext=True)

    #ax.contour(vv, nn, 3.5e5*Uout, (0.5, 98.1), colors='r', alpha=0.5)
    cs = ax.contour(vv, nn, 3.5e5*Ushout, (0.5,), linewidths=2, colors='r', alpha=0.5)
    ax.text(60, d["trapped y"][M],
            r'$\uparrow\uparrow$ Trapped i-front $\uparrow\uparrow$',
            ha='center', va='center',
            fontsize='xx-small', color='r', alpha=0.5, rotation=10,
            bbox=dict(fc=d["trapped bg"][M], ec='none', pad=1)
    )
    # ax.clabel(cs, (0.5,),
    #           manual=((60, 1e4),),
    #           fontsize='xx-small', colors='r',
    #           fmt=r'$\uparrow\uparrow$ Trapped i-front $\uparrow\uparrow$', 
    #           inline=True, inline_spacing=10, use_clabeltext=True)

    ax.contourf(vv, nn, tau, (eta, 1.0), colors='k', alpha=0.15)
    # ax.contour(vv, nn, tau, (eta/3, eta, 3*eta), colors='r')
    # ax.contour(vv, nn, tau, (1.0, 3.0), colors='m')
    cs = ax.contour(vv, nn, R0, R0s, linewidths=lws, colors='k')
    clevs = [level for level in clevs_to_label if level in cs.levels]
    ax.clabel(cs, clevs,
              fontsize='x-small', fmt=cformats,
              inline=True, inline_spacing=2, use_clabeltext=True)
    ax.text(18.0, 3e-3, Mlabel, zorder=100, fontsize='x-small', bbox=box_params)
    ax.text(18.0, 2000.0, RBW_label, rotation=15, fontsize='xx-small', bbox={**box_params, **dict(fc='0.85', ec='0.6')})
    ax.text(16.0, 1e6, RBS_label, rotation=15, fontsize='xx-small', bbox=box_params)
    ax.text(20.0, 15.0, WBS_label, rotation=15, fontsize='xx-small', bbox=box_params)


    #
    # Now do the cooling length
    #
    # pre-shock Mach number
    M0 = vv/10.0
    # post-shock Mach number
    M1 = np.sqrt((M0**2 + 3)/(5*M0**2 - 1))
    # post-shock temperature in units of T0
    T1 = (5*M0**2 - 1)*(1 + 3/M0**2) / 16
    # post-shock density
    n1 = nn*4*M0**2 / (M0**2 + 3)
    # post-shock velocity
    v1 = vv*nn/n1
    # Cooling rate
    Lam1 = 3.3e-24 * T1**2.3
    Lam2 = 1e-20 / T1
    k = 3
    Lambda = (Lam1**(-k) + Lam2**(-k))**(-1/k)
    # Cooling length in parsec
    dcool = 3*(1e5*v1)*(1.3806503e-16 * T1*T0) / (n1*Lambda) / 3.085677582e18

    # Ratio with respect to adiabatic shell thickness
    h1 = 0.177*R0
    cool_ratio1 = dcool / R0
    # Ratio with respect to isothermal shell thickness
    h2 = 3*R0/(4*M0**2) * (2 / (1 + np.sqrt(1 + (18/M0**2)) ))
    cool_ratio2 = dcool / h2

    cs = ax.contour(vv, nn, cool_ratio1, (1.0,),
                    linewidths=2, colors='b', alpha=0.5)
    ax.clabel(cs, 
              fontsize='xx-small', fmt=r"$d_\mathrm{cool} = R_0$",
              inline=True, inline_spacing=2, use_clabeltext=True)
    cs = ax.contour(vv, nn, cool_ratio2, (1.0,),
                    linewidths=1, colors='b', alpha=0.5)
    ax.clabel(cs, 
              fontsize='xx-small', fmt=r"$d_\mathrm{cool} = h_0$",
              inline=True, inline_spacing=2, use_clabeltext=True)


    ax.set(yscale='log')

axes[0].set(xlabel=r"$v$, km s$^{-1}$", ylabel=r"$n$, cm$^{-3}$")
sns.despine()
for ax in axes:
    ax.label_outer()
fig.tight_layout()
fig.savefig(figname)

print(figname, end='')
