import sys
import numpy as np
import matplotlib.pyplot as plt

def load_dprof(path):
    data = np.loadtxt(path)

    z = data[:, 0]
    rho = data[:, 1]
    rho_std = data[:, 2] if data.shape[1] >= 3 else None
    return z, rho, rho_std

def plot_dprof(path):
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

    plt.show()

if __name__ == "__main__":
    path = sys.argv[1]
    plot_dprof(path)
