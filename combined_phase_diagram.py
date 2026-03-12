import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

normalisation = 0.065
beta = 3.06

colour1 = 'b'
colour2 = 'r'

def binodal_function(c, ccrit, a):
    return np.where(c >= ccrit, a * (c - ccrit)**(1/beta), 0)

def diameter_function(c, rcrit, s, ccrit):
    return rcrit + s * (c - ccrit)

def fit_and_plot(ax, filename, label, linker, colour):
    data = np.genfromtxt(filename, delimiter=',', names=True, dtype=None, encoding=None)
    mask = (data['linker'] == linker)

    c_val = data['csalt'][mask].astype(float)
    rho_l = data['rho_low'][mask].astype(float)
    rho_l_err = data['err_low'][mask].astype(float)
    rho_h = data['rho_high'][mask].astype(float)
    rho_h_err = data['err_high'][mask].astype(float)

    popt_b, _ = curve_fit(binodal_function, c_val, rho_h - rho_l, p0=[0.065, 1000], bounds=([0.01, 0], [0.0729, 1e7]))
    cc_fit, a_fit = popt_b

    popt_d, _ = curve_fit(lambda c, rc, s: diameter_function(c, rc, s, cc_fit), c_val, (rho_l + rho_h) / 2)
    rho_c_fit, s_fit = popt_d

    c_plot = np.linspace(cc_fit, max(c_val) * 1.1, 200)
    diff   = binodal_function(c_plot, cc_fit, a_fit)
    mean   = diameter_function(c_plot, rho_c_fit, s_fit, cc_fit)
    rho_low  = mean - diff / 2
    rho_high = mean + diff / 2
    y_norm = c_plot / normalisation

    ax.errorbar(rho_l, c_val / normalisation, xerr=rho_l_err, fmt='o', markersize=6, capsize=3, zorder=5, color=colour)
    ax.errorbar(rho_h, c_val / normalisation, xerr=rho_h_err, fmt='o', markersize=6, capsize=3, zorder=5, label=label, color=colour)

    ax.fill_betweenx(y_norm, rho_low, rho_high, alpha=0.20)
    ax.plot(rho_low,  y_norm, '--', lw=1.5, color=colour)
    ax.plot(rho_high, y_norm, '--', lw=1.5, color=colour)

    crit_legend_label = (
    f"{label}: cc={cc_fit:.5f} M, \n"
    f"critical point=({rho_c_fit:.1f} g/L, {cc_fit/normalisation:.2f})")
    
    ax.scatter([rho_c_fit], [cc_fit / normalisation], marker='x', s=140, linewidth=2, zorder=10, label = crit_legend_label)

fig, ax = plt.subplots(figsize=(6, 5.5))
fit_and_plot(ax, "binodal_quantiles.csv", "25 bp", linker=25, colour=colour1)
fit_and_plot(ax, "binodal_quantiles.csv", "30 bp", linker=30, colour=colour2)

ax.legend(loc='lower right', fontsize=12)
ax.set_title("Simulation Phase Diagram", fontsize=16)
ax.set_ylabel("Normalised salt concentration", fontsize=14)
ax.set_xlabel("Density (g/L)", fontsize=14)
ax.set_ylim(1.00, 1.25)
ax.set_yticks([1.05, 1.10, 1.15, 1.20, 1.25])
ax.set_xlim(-2, 100)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()
