"""
neuron.py — Leaky Integrate-and-Fire (LIF) neuron model

The membrane potential V evolves as:
    τ_m · dV/dt = -(V - V_rest) + R_m · I(t)

When V crosses v_thresh, a spike is recorded and V resets to v_reset.
"""


class LIFNeuron:
    def __init__(
        self,
        tau_m=20.0,     # membrane time constant (ms)
        v_rest=-65.0,   # resting potential (mV)
        v_thresh=-50.0, # spike threshold (mV)
        v_reset=-65.0,  # reset potential after spike (mV)
        r_m=10.0,       # membrane resistance (MΩ)
        t_ref=2.0,      # refractory period (ms)
    ):
        self.tau_m = tau_m
        self.v_rest = v_rest
        self.v_thresh = v_thresh
        self.v_reset = v_reset
        self.r_m = r_m
        self.t_ref = t_ref

        # State variables
        self.v = v_rest
        self.t_since_spike = float("inf")  # ms since last spike

    def step(self, i_ext, dt=0.1):
        """
        Advance the neuron by one timestep dt (ms).
        Returns True if a spike occurred this step.
        """
        spiked = False

        if self.t_since_spike < self.t_ref:
            # Refractory period — clamp voltage, skip integration
            self.v = self.v_reset
            self.t_since_spike += dt
            return spiked

        # Euler integration of the LIF equation
        dv = (dt / self.tau_m) * (
            -(self.v - self.v_rest) + self.r_m * i_ext
        )
        self.v += dv

        if self.v >= self.v_thresh:
            self.v = self.v_reset
            self.t_since_spike = 0.0
            spiked = True
        else:
            self.t_since_spike += dt

        return spiked

    def reset(self):
        """Reset neuron to resting state."""
        self.v = self.v_rest
        self.t_since_spike = float("inf")
