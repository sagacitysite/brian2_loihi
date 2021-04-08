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
* The LoihiSpikeMonitor extends the Brian2 SpikeMonitor class
* The LoihiSpikeGeneratorGroup extends the Brian2 SpikeGeneratorGroup class

Note that the attributes of the extended classes deviate in most cases from
the attributes available in the original Brian2 classes.
"""

"""
TODO Start
"""
# print(LoihiSynapses), print(LoihiNeuronGroup)
# Parameter check: warning instead of exception?
# Parameter names according to NxSDK? Pro: consistency, Con: Nobody knows the NxSDK docs
# setter and getter for parameters using python properties? (see https://www.python-kurs.eu/python3_properties.php)
# Create documenation?
"""
TODO End
"""

# Import all necessary modules
#from brian2_loihi.constants import state, synapse_sign_mode
#from brian2_loihi.loihi_network import LoihiNetwork
#from brian2_loihi.loihi_neuron_group import LoihiNeuronGroup
#from brian2_loihi.loihi_synapses import LoihiSynapses
#from brian2_loihi.loihi_state_monitor import LoihiStateMonitor
#from brian2_loihi.loihi_spike_generator_group import LoihiSpikeGeneratorGroup

from .constants import state, synapse_sign_mode
from .loihi_network import LoihiNetwork
from .loihi_neuron_group import LoihiNeuronGroup
from .loihi_synapses import LoihiSynapses
from .loihi_state_monitor import LoihiStateMonitor
from .loihi_spike_monitor import LoihiSpikeMonitor
from .loihi_spike_generator_group import LoihiSpikeGeneratorGroup
