"""
plot.py — Visualize LIF simulation results
Run simulate.py first to generate simulation_results.npz
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


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

    # ISI histogram (constant input only)
    ax_isi = fig.add_subplot(gs[2, :])
    isi = np.diff(spks[0]) if len(spks[0]) > 1 else []
    if len(isi):
        ax_isi.hist(isi, bins=20, color="#4CAF50", edgecolor="white")
        ax_isi.set_xlabel("Inter-spike interval (ms)")
        ax_isi.set_ylabel("Count")
        ax_isi.set_title("ISI distribution (constant input)", fontsize=10)
    else:
        ax_isi.text(0.5, 0.5, "Not enough spikes for ISI",
                    ha="center", transform=ax_isi.transAxes)

    plt.savefig("lif_results.png", dpi=150, bbox_inches="tight")
    print("Plot saved to lif_results.png")
    plt.show()


if __name__ == "__main__":
    plot_results()
