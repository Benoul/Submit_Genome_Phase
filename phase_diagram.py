import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_binodal(csv_path="binodal_quantiles.csv",
                  out_png="binodal_overlay.png",
                  show=True):

    df = pd.read_csv(csv_path)

    plt.figure(figsize=(7, 5))

    for L in sorted(df["linker"].unique()):
        sub = df[df["linker"] == L].sort_values("csalt")

        cs = sub["csalt"].values
        low = sub["rho_low"].values
        high = sub["rho_high"].values

        has_err = sub["err_low"].notna().all() and sub["err_high"].notna().all()

        if has_err:
            plt.errorbar(cs, low,
                         yerr=sub["err_low"].values,
                         fmt="o-",
                         capsize=3,
                         label=f"L={L} (low)")

            plt.errorbar(cs, high,
                         yerr=sub["err_high"].values,
                         fmt="s-",
                         capsize=3,
                         label=f"L={L} (high)")
        else:
            plt.plot(cs, low,  "o-", label=f"L={L} (low)")
            plt.plot(cs, high, "s-", label=f"L={L} (high)")

    plt.xlabel(r"$c_{\mathrm{salt}}$")
    plt.ylabel(r"$\rho$")
    plt.title("Binodal estimate from dprof quantiles")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)

    print(f"Saved plot -> {out_png}")

    if show:
        plt.show()
    else:
        plt.close()


if __name__ == "__main__":
    plot_binodal()
