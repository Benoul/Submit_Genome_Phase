import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os


NBINS = 100
MINC = 6.5735696879671400261e-02


COLOR25 = '#1565C0'
COLOR30 = '#C62828'


def binodal_func(c, cc, a):
    return np.where(c >= cc, a * (c - cc)**(1/3.06), 0)

def diameter_func(c, rc, s, cc):
    return rc + s * (c - cc)

def fit_and_plot(ax, filename, color, label, linker):
    data = np.genfromtxt(filename, delimiter=',', names=True, dtype=None, encoding=None)
    mask = (data['linker'] == linker)

    c_val = data['csalt'][mask].astype(float)
    rho_l = data['rho_low'][mask].astype(float)
    rho_l_err = data['err_low'][mask].astype(float)
    rho_h = data['rho_high'][mask].astype(float)
    rho_h_err = data['err_high'][mask].astype(float)

    popt_b, _ = curve_fit(binodal_func, c_val, rho_h - rho_l,
                          p0=[0.065, 1000],
                          bounds=([0.01, 0], [0.0729, 1e7]))
    cc_fit, a_fit = popt_b

    popt_d, _ = curve_fit(
        lambda c, rc, s: diameter_func(c, rc, s, cc_fit),
        c_val, (rho_l + rho_h) / 2)
    rho_c_fit, s_fit = popt_d

    c_plot = np.linspace(cc_fit, max(c_val) * 1.1, 200)
    diff   = binodal_func(c_plot, cc_fit, a_fit)
    mean   = diameter_func(c_plot, rho_c_fit, s_fit, cc_fit)
    rho_left  = mean - diff / 2
    rho_right = mean + diff / 2
    y_norm = c_plot / MINC

    ax.fill_betweenx(y_norm, rho_left, rho_right, color=color, alpha=0.20)
    ax.plot(rho_left,  y_norm, '--', color=color, lw=1.5)
    ax.plot(rho_right, y_norm, '--', color=color, lw=1.5)
    ax.errorbar(rho_l, c_val / MINC, xerr=rho_l_err,
            fmt='o', color=color, markersize=6,
            capsize=3, zorder=5)
    ax.errorbar(rho_h, c_val / MINC, xerr=rho_h_err,
                fmt='o', color=color, markersize=6,
                capsize=3, zorder=5, label=label)
    ax.scatter([rho_c_fit], [cc_fit / MINC], marker='x', color=color,
               s=120, linewidth=2, zorder=10)

    print(f"{label}: cc={cc_fit:.5f} M, "
          f"critical point=({rho_c_fit:.1f} g/L, {cc_fit/MINC:.4f})")

fig, ax = plt.subplots(figsize=(6, 5.5))

fit_and_plot(ax, "binodal_quantiles.csv", COLOR25, "25 bp", linker=25)
fit_and_plot(ax, "binodal_quantiles.csv", COLOR30, "30 bp", linker=30)

ax.set_ylabel("Normalised salt concentration", fontsize=14)
ax.set_xlabel("Density (g/L)", fontsize=14)
ax.set_ylim(1.01, 1.26)
ax.set_yticks([1.05, 1.10, 1.15, 1.20, 1.25])
ax.set_xlim(-2, 100)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(loc='lower right', frameon=True, fontsize=12)
ax.set_title("Simulation Phase Diagram", fontsize=16)

plt.tight_layout()
plt.show()
