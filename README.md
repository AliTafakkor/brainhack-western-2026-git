# 🧠 LIF Neuron Simulator — Git Tutorial Project

This is the example project for a hands-on git tutorial. The code simulates a
**Leaky Integrate-and-Fire (LIF) neuron** — one of the simplest models of how
a neuron integrates input and fires a spike.

## Start here

👉 Open [`GIT_TUTORIAL.md`](./GIT_TUTORIAL.md) and follow along from Step 1.

## Project files

| File | What it does |
|------|-------------|
| `neuron.py` | The `LIFNeuron` class — membrane dynamics, spiking, reset |
| `simulate.py` | Runs simulations with constant or noisy input |
| `plot.py` | Plots the voltage trace, spike raster, and ISI histogram |

## Requirements

```bash
pip install numpy matplotlib
```

Then run:

```bash
python simulate.py
python plot.py
```
