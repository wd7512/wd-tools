import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_ridgeline_with_base(data, y_col, x1_col, x2_col, base_array,
                             n_points=200, overlap=0.7,
                             color1='C0', color2='C1', base_color='C2',
                             ax=None):
    levels = sorted(data[y_col].unique())
    n = len(levels)

    hists, max_d = {}, 0
    for lvl in levels:
        for col in (x1_col, x2_col):
            vals = data.loc[data[y_col]==lvl, col].values
            hist, edges = np.histogram(vals, bins=n_points, density=True)
            centers = 0.5 * (edges[:-1] + edges[1:])
            hists[(lvl, col)] = (centers, hist)
            max_d = max(max_d, hist.max())
    sep = max_d * overlap

    base_hist, base_edges = np.histogram(base_array, bins=n_points, density=True)
    base_centers = 0.5 * (base_edges[:-1] + base_edges[1:])
    base_off = n * sep

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 20))

    ax.fill_between(base_centers, base_off, base_hist + base_off, alpha=0.6, color=base_color)
    ax.plot(base_centers, base_hist + base_off, lw=1.2, color=base_color)
    ax.text(base_centers[0], base_off + 0.001, 'Historical', va='center', ha='left', fontsize=9)

    for idx, lvl in enumerate(levels):
        off = (n - 1 - idx) * sep
        x1_centers, h1 = hists[(lvl, x1_col)]
        ax.fill_between(x1_centers, off, h1 + off, alpha=0.6, color=color1)
        ax.plot(x1_centers, h1 + off, lw=1.2, color=color1)

        x2_centers, h2 = hists[(lvl, x2_col)]
        ax.plot(x2_centers, h2 + off, lw=1.2, linestyle='--', color=color2)
        ax.text(x1_centers[0], off + 0.001, str(lvl), va='center', ha='left', fontsize=9)

    ax.set_yticks([])
    ax.set_xlabel('Value')
    ax.legend(['Historical (2024/2025)', x1_col, x2_col],
              loc='upper right', frameon=False, title=y_col)
    ax.grid()


fig, axs = plt.subplots(1, 2, figsize=(20, 20))

plot_ridgeline_with_base(
    aeres_data, "year", "niv_MFC_25", "niv_DEC_24", historical_data["NIV"],
    color1='C0', color2='C1', base_color='C2', ax=axs[0]
)

plot_ridgeline_with_base(
    aeres_data, "year", "niv_MFC_25", "niv_MFC_25", historical_data["NIV"],
    color1='C0', color2='C1', base_color='C2', ax=axs[1]
)

plt.tight_layout()
plt.show()
