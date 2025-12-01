import numpy as np
import matplotlib.pyplot as plt

# Load data
rmsf_protein = np.loadtxt("rmsd_protein.dat")
rmsd_protein_CA = np.loadtxt("rmsd_protein_CA.dat")
rmsd_efz = np.loadtxt("rmsd_efz.dat")

# Extract columns (frame, value)
x1, y1 = rmsf_protein[:, 0], rmsf_protein[:, 1]
x2, y2 = rmsd_protein_CA[:, 0], rmsd_protein_CA[:, 1]
x3, y3 = rmsd_efz[:, 0], rmsd_efz[:, 1]

# --- Convert frame → time (ns) ---
dt_ps = 0.002     # 2 fs
ntwx = 5000       # trajectory write frequency
time_per_frame_ns = (dt_ps * ntwx) / 1000.0   # = 0.01 ns

time1 = x1 * time_per_frame_ns
time2 = x2 * time_per_frame_ns
time3 = x3 * time_per_frame_ns

# Means
mean1 = np.mean(y1)
mean2 = np.mean(y2)
mean3 = np.mean(y3)

# Colors
c1, c2, c3 = "blue", "orange", "green"

# --- FIGURE ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 9))

# -------------------------
# Subplot 1: RMSD vs Time
# -------------------------
ax1.plot(time1, y1, label="RMSD Protein", linewidth=1, color=c1)
ax1.plot(time2, y2, label="RMSD Protein_CA", linewidth=1, color=c2)
ax1.plot(time3, y3, label="RMSD EFZ (Ligand)", linewidth=1, color=c3)

ax1.set_xlabel("Time (ns)", fontsize=12)
ax1.set_ylabel("RMSD (Å)", fontsize=12)
ax1.set_title("RMSD vs Time", fontsize=14)
ax1.legend()
ax1.grid(True, linestyle="--", alpha=0.4)

# -------------------------
# Subplot 2: Histogram + Mean Values
# -------------------------
ax2.hist(y1, bins=40, alpha=0.4, label="RMSD Protein", color=c1)
ax2.hist(y2, bins=40, alpha=0.4, label="RMSD Protein_CA", color=c2)
ax2.hist(y3, bins=40, alpha=0.4, label="RMSD EFZ (Ligand)", color=c3)

# Mean lines
ax2.axvline(mean1, color=c1, linestyle="--", linewidth=1)
ax2.axvline(mean2, color=c2, linestyle="--", linewidth=1)
ax2.axvline(mean3, color=c3, linestyle="--", linewidth=1)

# Mean labels (non-rotated)
ymax = ax2.get_ylim()[1]
ax2.text(mean1, ymax * 0.95, f"{mean1:.2f} Å", color=c1, fontsize=11, ha="center")
ax2.text(mean2, ymax * 0.95, f"{mean2:.2f} Å", color=c2, fontsize=11, ha="center")
ax2.text(mean3, ymax * 0.95, f"{mean3:.2f} Å", color=c3, fontsize=11, ha="center")

ax2.set_xlabel("RMSD (Å)", fontsize=12)
ax2.set_ylabel("Frequency", fontsize=12)
ax2.set_title("RMSD Distribution with Mean Values", fontsize=14)
ax2.legend()
ax2.grid(True, linestyle="--", alpha=0.4)

plt.tight_layout()

# Save HD
plt.savefig("rmsd_time_distribution_plot.png", dpi=300)

plt.show()

