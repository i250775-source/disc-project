import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_zscores(z_a, z_b, dept_a, dept_b, R, out_path):
    classes = list(range(1, 14))
    width = 0.38
    x_a = [k - width / 2 for k in classes]
    x_b = [k + width / 2 for k in classes]

    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.bar(x_a, z_a, width, label=f"Department A (dept {dept_a})", color="#2a6fdb")
    ax.bar(x_b, z_b, width, label=f"Department B (dept {dept_b})", color="#e8833a")

    ax.axhline(2, color="black", linestyle="--", linewidth=1)
    ax.axhline(-2, color="black", linestyle="--", linewidth=1)
    ax.axhline(0, color="grey", linewidth=0.6)

    ax.set_xticks(classes)
    ax.set_xlabel("Triad class")
    ax.set_ylabel("Z-score")
    ax.set_title(f"Triad Z-scores: dept {dept_a} vs dept {dept_b}  (R = {R})")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
