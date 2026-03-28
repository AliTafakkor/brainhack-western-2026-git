"""
simulate.py — Run LIF neuron simulations and save results
"""

import numpy as np
from neuron import LIFNeuron


def run_simulation(i_ext_fn, duration=500.0, dt=0.1, seed=42):
    """
    Simulate a LIF neuron.

    Parameters
    ----------
    i_ext_fn : callable
        Function of time t (ms) → input current (nA)
    duration : float
        Total simulation time (ms)
    dt : float
        Timestep (ms)
    seed : int
        Random seed for reproducibility

    Returns
    -------
    t       : np.ndarray  — time vector (ms)
    v       : np.ndarray  — membrane potential trace (mV)
    spikes  : list        — spike times (ms)
    """
    np.random.seed(seed)
    neuron = LIFNeuron()

    t = np.arange(0, duration, dt)
    v = np.zeros(len(t))
    spikes = []

    for i, ti in enumerate(t):
        spiked = neuron.step(i_ext_fn(ti), dt=dt)
        v[i] = neuron.v
        if spiked:
            spikes.append(ti)

    return t, v, spikes


if __name__ == "__main__":
    # --- Experiment 1: constant input ---
    def constant_input(t):
        return 1.6  # nA (near threshold for more interpretable baseline)

    t, v, spikes = run_simulation(constant_input, duration=500)
    print(f"Constant input → {len(spikes)} spikes")
    print(f"  Mean firing rate: {len(spikes) / 0.5:.1f} Hz")

    # --- Experiment 2: noisy input ---
    def noisy_input(t):
        return 1.6 + np.random.normal(0, 2.0)

    t2, v2, spikes2 = run_simulation(noisy_input, duration=500)
    print(f"\nNoisy input → {len(spikes2)} spikes")
    print(f"  Mean firing rate: {len(spikes2) / 0.5:.1f} Hz")

    # Save results for plot.py
    np.savez(
        "simulation_results.npz",
        t=t, v=v, spikes=np.array(spikes),
        t2=t2, v2=v2, spikes2=np.array(spikes2),
    )
    print("\nResults saved to simulation_results.npz — run plot.py to visualize.")
