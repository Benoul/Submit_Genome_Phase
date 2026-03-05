import os
import re
import glob
import numpy as np
import csv

def load_dprof(path):
    # columns: z_center, rho_mean, rho_std
    data = np.loadtxt(path)
    z = data[:, 0]
    rho = data[:, 1]
    rho_std = data[:, 2] if data.shape[1] >= 3 else None
    return z, rho, rho_std

def low_high_from_quantiles(rho, rho_std=None, frac=0.2, ignore_zeros=True):
    rho = np.asarray(rho, float)
    if rho_std is not None:
        rho_std = np.asarray(rho_std, float)

    mask = np.isfinite(rho)
    if ignore_zeros:
        mask &= (rho > 0)

    vals = rho[mask]
    k = max(1, int(np.floor(frac * vals.size)))
    order = np.argsort(vals)
    vals_sorted = vals[order]

    low_vals  = vals_sorted[:k]
    high_vals = vals_sorted[-k:]

    rho_low = float(np.mean(low_vals))
    rho_high = float(np.mean(high_vals))

    err_low = err_high = None
    if rho_std is not None:
        std_vals = rho_std[mask]
        std_sorted = std_vals[order]
        low_std = std_sorted[:k]
        high_std = std_sorted[-k:]
        err_low = float(np.sqrt(np.mean(low_std**2)) / np.sqrt(k))
        err_high = float(np.sqrt(np.mean(high_std**2)) / np.sqrt(k))

    return rho_low, rho_high, err_low, err_high, k, vals.size

def parse_csalt_from_name(fname):
    m = re.search(r"dprof[_-]?([0-9]*\.[0-9]+)", fname)
    if not m:
        raise ValueError(f"failed: {fname}")
    return float(m.group(1))

def parse_linker_from_dir(dirname):
    m = re.search(r"(\d+)$", os.path.basename(dirname))
    return int(m.group(1))

def collect_rows(data_dirs=("data25", "data30"), frac=0.2, ignore_zeros=True):
    rows = []
    for ddir in data_dirs:
        L = parse_linker_from_dir(ddir)
        paths = sorted(glob.glob(os.path.join(ddir, "dprof*.txt")))
        if not paths:
            print(f"No matching files found in {ddir}")
            continue

        for path in paths:
            csalt = parse_csalt_from_name(os.path.basename(path))
            z, rho, rho_std = load_dprof(path)
            rho_low, rho_high, err_low, err_high, k_used, n_used = low_high_from_quantiles(
                rho, rho_std=rho_std, frac=frac, ignore_zeros=ignore_zeros
            )

            rows.append({
                "linker": L,
                "csalt": csalt,
                "rho_low": rho_low,
                "rho_high": rho_high,
                "err_low": err_low,
                "err_high": err_high,
                "k_used": k_used,
                "n_bins_used": n_used,
                "file": path,
            })
    rows.sort(key=lambda r: (r["linker"], r["csalt"]))
    return rows

def write_csv(rows, out_path="binodal_quantiles.csv"):
    fieldnames = ["linker","csalt","rho_low","rho_high","err_low","err_high","k_used","n_bins_used","file"]
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"Wrote to {out_path}")

if __name__ == "__main__":
    rows = collect_rows(data_dirs=("data25", "data30"), frac=0.2, ignore_zeros=True)
    write_csv(rows, out_path="binodal_quantiles.csv")
