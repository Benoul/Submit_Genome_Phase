import sys
import numpy as np
import matplotlib.pyplot as plt

def load_dprof(path):
    data = np.loadtxt(path)
    if data.ndim != 2 or data.shape[1] < 2:
        raise ValueError(f"Must have columns: z, rho, (maybe rho_std...)")

    z = data[:, 0]
    rho = data[:, 1]
    rho_std = data[:, 2] if data.shape[1] >= 3 else None
    return z, rho, rho_std

def plot_dprof(path, out_png=None, show=True):
    z, rho, rho_std = load_dprof(path)

    plt.figure(figsize=(7, 4.5))

    if rho_std is not None and np.all(np.isfinite(rho_std)):
        plt.errorbar(z, rho, yerr=rho_std, fmt="-", capsize=2)
    else:
        plt.plot(z, rho, "-")

    plt.xlabel("z")
    plt.ylabel(r"$\rho(z)$")
    plt.title(path)
    plt.grid(alpha=0.25)
    plt.tight_layout()

    if out_png:
        plt.savefig(out_png, dpi=200)
        print(f"Saved -> {out_png}")

    if show:
        plt.show()
    else:
        plt.close()

if __name__ == "__main__":
    path = sys.argv[1]
    out_png = sys.argv[2] if len(sys.argv) >= 3 else None
    plot_dprof(path, out_png=out_png, show=True)
