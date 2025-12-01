#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

# -------------------------------
# Load RMSF data
# -------------------------------
data = np.loadtxt("rmsf_protein.dat")

residues = data[:, 0]
rmsf = data[:, 1]

# Filter residues 1–243 only
mask = (residues >= 1) & (residues <= 243)
residues = residues[mask]
rmsf = rmsf[mask]

# Compute statistics
mean_rmsf = np.mean(rmsf)

# -------------------------------
# Plotting
# -------------------------------
fig, ax = plt.subplots(2, 1, figsize=(10, 7), sharex=False)

# =============================
# 1️⃣ Line plot RMSF vs residue
# =============================
ax[0].plot(residues, rmsf, linewidth=1, label="RMSF (Residue-wise)")

ax[0].axhline(mean_rmsf, color="r", linestyle="--", linewidth=1)
ax[0].text(residues[-1], mean_rmsf + 0.02,
           f"Mean = {mean_rmsf:.3f} Å",
           color="r", fontsize=11, ha="right", va="bottom")

ax[0].set_xlabel("Residue Index")
ax[0].set_ylabel("RMSF (Å)")
ax[0].set_title("RMSF Per Residue (1–243)")
ax[0].grid(True, linestyle="--", alpha=0.4)

# =============================
# 2️⃣ RMSF Distribution
# =============================
ax[1].hist(rmsf, bins=25, density=True, alpha=0.5)

# Smooth KDE-like curve without seaborn
density_x = np.linspace(min(rmsf), max(rmsf), 200)
hist, bin_edges = np.histogram(rmsf, bins=25, density=True)
hist_smooth = gaussian_filter1d(hist, sigma=2)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
ax[1].plot(bin_centers, hist_smooth, linewidth=1)

# Highlight mean on distribution
ax[1].axvline(mean_rmsf, color="r", linestyle="--", linewidth=1)
ax[1].text(mean_rmsf, max(hist_smooth) * 0.9,
           f"{mean_rmsf:.3f} Å",
           color="r", fontsize=11, ha="center")

ax[1].set_xlabel("RMSF (Å)")
ax[1].set_ylabel("Density")
ax[1].set_title("RMSF Distribution (Residues 1–243)")
ax[1].grid(True, linestyle="--", alpha=0.4)

plt.tight_layout()

# Save HD figure
plt.savefig("rmsf_plot.png", dpi=600)

plt.show()
