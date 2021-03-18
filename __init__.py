"""Loihi emulator based on Brian2

This package allows an emulation of the Loihi chip in Brian2.

Not all features of Loihi are available in this version. In the following you find a
description of the provided precision and available parameters.

The package provides the following precision:

* The neuron and synapse model result in a perfect match with Loihi
* The learning rule matches Loihi beside small fluctuations due to stochastic rounding

The following parameters can be chosen

* Neuron model: threshold, refactory period, current decay, voltage decay
* Synapse model: delay, weights, traces x1, x2, y1, y2, y3

The module mainly extends Brian2 classes:
* The LoihiNetwork extends the Brian2 Network class
* The LoihiNeuronGroup extends the Brian2 NeuronGroup class
* The LoihiSynapses extends the Brian2 Synapses class
* The LoihiStateMonitor extends the Brian2 StateMonitor class
* The LoihiSpikeGeneratorGroup extends the Brian2 SpikeGeneratorGroup class

Note that the attributes of the extended classes deviate in most cases from
the attributes available in the original Brian2 classes.
"""

"""
TODO Start
"""
# Define learning rule
# Readme
# Create pip package
# Parameter check: warning instead of exception?
# Parameter names according to NxSDK? Pro: consistency, Con: Nobody knows the NxSDK docs
# setter and getter for parameters using python properties? (see https://www.python-kurs.eu/python3_properties.php)
# Create documenation?
"""
TODO End
"""

# Import all necessary modules
from .lib.constants import state, synapse_sign_mode
from .lib.loihi_network import LoihiNetwork
from .lib.loihi_neuron_group import LoihiNeuronGroup
from .lib.loihi_synapses import LoihiSynapses
from .lib.loihi_state_monitor import LoihiStateMonitor
from .lib.loihi_spike_generator_group import LoihiSpikeGeneratorGroup
