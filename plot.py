"""
plot.py — Visualize LIF simulation results
Run simulate.py first to generate simulation_results.npz
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def _plot_isi_hist(ax, spike_times, label):
    isi = np.diff(np.asarray(spike_times, dtype=float)) if len(spike_times) > 1 else np.array([])
    isi = isi[np.isfinite(isi)]

    if len(isi) == 0:
        ax.text(0.5, 0.5, "Not enough spikes for ISI", ha="center", va="center", transform=ax.transAxes)
        ax.set_title(f"{label} ISI", fontsize=10)
        ax.set_xlabel("Inter-spike interval (ms)")
        ax.set_ylabel("Count")
        return

    if np.isclose(np.ptp(isi), 0.0):
        ax.bar([isi[0]], [len(isi)], width=0.5, color="#4CAF50", edgecolor="white")
    else:
        bins = max(5, min(20, int(np.sqrt(len(isi)))))
        try:
            ax.hist(isi, bins=bins, color="#4CAF50", edgecolor="white")
        except ValueError:
            ax.hist(isi, bins="auto", color="#4CAF50", edgecolor="white")

    cv = np.std(isi) / np.mean(isi) if np.mean(isi) > 0 else np.nan
    cv_text = f"CV={cv:.3f}" if np.isfinite(cv) else "CV=n/a"
    ax.set_title(f"{label} ISI ({cv_text})", fontsize=10)
    ax.set_xlabel("Inter-spike interval (ms)")
    ax.set_ylabel("Count")


def plot_results(results_file="simulation_results.npz"):
    data = np.load(results_file)

    fig = plt.figure(figsize=(10, 7))
    fig.suptitle("LIF Neuron Simulator", fontsize=14, fontweight="bold")
    gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.55, wspace=0.35)

    labels = ["Constant input", "Noisy input"]
    ts     = [data["t"],  data["t2"]]
    vs     = [data["v"],  data["v2"]]
    spks   = [data["spikes"], data["spikes2"]]

    for col, (label, t, v, spike_times) in enumerate(zip(labels, ts, vs, spks)):
        # Membrane potential trace
        ax_v = fig.add_subplot(gs[0, col])
        ax_v.plot(t, v, color="#2196F3", lw=0.8)
        ax_v.axhline(-50, color="tomato", lw=0.8, ls="--", label="threshold")
        ax_v.set_title(label, fontsize=10)
        ax_v.set_ylabel("V (mV)")
        ax_v.set_xlabel("Time (ms)")
        ax_v.legend(fontsize=7)

        # Spike raster
        ax_r = fig.add_subplot(gs[1, col])
        ax_r.eventplot(spike_times, color="black", linewidths=1.5)
        ax_r.set_title(f"Spike raster  ({len(spike_times)} spikes)", fontsize=9)
        ax_r.set_xlabel("Time (ms)")
        ax_r.set_yticks([])

    # ISI histograms for both conditions
    ax_isi_const = fig.add_subplot(gs[2, 0])
    ax_isi_noise = fig.add_subplot(gs[2, 1])
    _plot_isi_hist(ax_isi_const, spks[0], "Constant")
    _plot_isi_hist(ax_isi_noise, spks[1], "Noisy")

    plt.savefig("lif_results.png", dpi=150, bbox_inches="tight")
    print("Plot saved to lif_results.png")
    plt.show()


if __name__ == "__main__":
    plot_results()
