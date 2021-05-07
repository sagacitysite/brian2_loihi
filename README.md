# A Loihi emulator based on Brian2

The package extends *Brian2* classes such that they match Loihi simulations. While the neuron and synapse model results in an exact match to *Loihi*, the pre- and post-synaptic traces have very small variations from the *Loihi* chip due to stochastic rounding.

Further details are explained in a paper coming soon.

## Installation

```
pip install brian2-loihi
```

### Requirements and dependencies

**Python 3.6** or higher is required.

Dependencies are automatically installed by the pip package manager.

If the source code is used directly, the following packages need to be installed:

* [Brian2 (2.4.2 or higher)](https://brian2.readthedocs.io/en/stable/)
* [Numpy](https://numpy.org/)

## Usage

Five *Brian2* classes are extended. Available parameters are reported below. Further down you find example code.

**Note**:

* It is important to use a `LoihiNetwork`. The *Brian2* magic network approach is not supported.
* Don't change the `defaultclock.dt` value. It is set to match *Loihi*.
* Don't reorder the network simulation `schedule`.

First import the package as:

```
from brian2_loihi import *
```

The following classes can be used:

### LoihiNetwork

Extends the `Network` class from *Brian2* and supports the same parameters.

### LoihiNeuronGroup

Extends the `NeuronGroup` class from *Brian2* and supports the following parameters:

* **N** (int): Number of neurons in the group.
* **refractory** (int, 1...64, optional): The refactory period of the neuron.
* **threshold_v_mant** (int, 0...131071, optional): The mantissa of the membrane voltage threshold.
* **decay_v** (int, 0...4096, optional): The membrane voltage decay (note that tau_v = 4096/decay_v)
* **decay_I** (int, 0...4096, optional): The current decay (note that tau_I = 4096/decay_I)
* **name** (str, optional): A unique name for the group, otherwise use `loihi_neurongroup_0`, etc.

### LoihiSynapses

Extends the `Synapses` class from *Brian2* and supports the following parameters:

* **source** (`SpikeSource`): The source of spikes, e.g. a NeuronGroup.
* **target** (`Group`, optional): The target of the spikes, typically a NeuronGroup. If none is given, the same as source().
* **delay** (int, optional): The synaptic delay.
* **dw** (str, optional): Learning rule, using the pre- and post-synaptic traces. Also constant values are allowed. Note that only `*`, `-` and `+` is allowed.
* **w_exp** (int, optional): Weight exponent which scales the weights by 2^(6 + w_exp). The weight exponent can be between -8 and 7.
* **sign_mode** (int, optional): Defines if the synapses are mixed (1), excitatory (2) or inhibitory (3). Excitatory synapses are default. `synapse_sign_mode` can be used for defining the sign mode.
* **num_weight_bits** (int, optional): Defines the precision of the weight, default is 8 bits. `num_weight_bits` is in a range between 0 and 8.
* **imp_x1** (int, optional): The impulse of the first synaptic pre trace x1. The impulse is between 0 and 127.
* **tau_x1** (int, optional): The time constant of the first synaptic pre trace x1. Tau has to be greater or equal to 0.
* **imp_x2** (int, optional): The impulse of the first synaptic pre trace x2. The impulse is between 0 and 127.
* **tau_x2** (int, optional): The time constant of the first synaptic pre trace x2. Tau has to be greater or equal to 0.
* **imp_y1** (int, optional): The impulse of the first synaptic post trace y1. The impulse is between 0 and 127.
* **tau_y1** (int, optional): The time constant of the first synaptic pre trace y1. Tau has to be greater or equal to 0.
* **imp_y2** (int, optional): The impulse of the first synaptic post trace y2. The impulse is between 0 and 127.
* **tau_y2** (int, optional): The time constant of the first synaptic pre trace y2. Tau has to be greater or equal to 0.
* **imp_y3** (int, optional): The impulse of the first synaptic post trace y3. The impulse is between 0 and 127.
* **tau_y3** (int, optional): The time constant of the first synaptic pre trace y3. Tau has to be greater or equal to 0.
* **name** (str, optional):  The name for this object. If none is given, a unique name of the form. `loihi_synapses`, `loihi_synapses_1`, etc. will be automatically chosen.

### LoihiStateMonitor

Extends the `StateMonitor` class from *Brian2* and supports the following parameters:

* **source** (`Group`): Which object to record values from.
* **variable** (str): Which variables to record, check the `state` object for details.
* **record** (bool, sequence of ints): Which indices to record, nothing is recorded for ``False``, everything is recorded for ``True`` (warning: may use a great deal of memory), or a specified subset of indices.
* **order** (int, optional): The priority of of this group for operations occurring at the same time step and in the same scheduling slot. Defaults to 0.
* **name** (str, optional): A unique name for the object, otherwise will use `source.name+'loihi_statemonitor_0'`, etc.

### LoihiSpikeMonitor

Extends the `SpikeMonitor` class from *Brian2* and supports the following parameters:

* **source** (`Group`): Which object to record values from.
* **variable** (str, optional): Which variables to record at the time of the spike (in addition to the index of the neuron). Can be the name of a variable or a list of names
* **record** (bool, sequence of ints, optional): Which indices to record, nothing is recorded for ``False``, everything is recorded for ``True`` (warning: may use a great deal of memory), or a specified subset of indices.
* **order** (int, optional): The priority of of this group for operations occurring at the same time step and in the same scheduling slot. Defaults to 0.
* **name** (str, optional): A unique name for the object, otherwise will use `source.name+'_loihi_spikemonitor_0'`, etc.

### LoihiSpikeGeneratorGroup

Extends the `SpikeGeneratorGroup` class from *Brian2* and supports the following parameters:

* **N** (int): The number of "neurons" in this group
* **indices** (array of integers): The indices of the spiking cells
* **times** (list (int)): The spike times for the cells given in ``indices``. Has to have the same length as ``indices`` and has to be integer (without time units)
* **period** (int, optional): If this is specified, it will repeat spikes with this period. A period of 0 means not repeating spikes.
* **order** (int, optional): The priority of of this group for operations occurring at the same time step and in the same scheduling slot. Defaults to 0.
* **sorted** (bool, optional):  Whether the given indices and times are already sorted. Set to ``True`` if your events are already sorted (first by spike time, then by index), this can save significant time at construction if your arrays contain large numbers of spikes. Defaults to ``False``.
* **name** (str, optional): A unique name for the object, otherwise will use `loihi_spikegeneratorgroup_0'`, etc.

## Example

More examples and further details are provided in this repository:

https://github.com/sagacitysite/brian2_loihi_utils

Here we just provide a simple example.

### Single neuron

```
import matplotlib.pyplot as plt
from brian2_loihi import *

# Define a single neuron
loihi_group = LoihiNeuronGroup(
    1,
    refractory=2,
    threshold_v_mant=400,
    decay_v=1024,
    decay_I=1024
)

# Excitatory input spikes
ex_neuron_indices = [0, 0, 0, 0]
ex_spike_times = [12, 14, 40, 80]

# Inhibitory input spikes
in_neuron_indices = [0, 0, 0]
in_spike_times = [50, 60, 90]

# Define spike generators
generator_ex = LoihiSpikeGeneratorGroup(1, ex_neuron_indices, ex_spike_times)
generator_in = LoihiSpikeGeneratorGroup(1, in_neuron_indices, in_spike_times)

# Connect excitatory generator with neuron
syn_ex = LoihiSynapses(generator_ex, loihi_group, sign_mode=synapse_sign_mode.EXCITATORY)
syn_ex.connect()
syn_ex.w = 124

# Connect inhibitory generator with neuron
syn_in = LoihiSynapses(generator_in, loihi_group, sign_mode=synapse_sign_mode.INHIBITORY)
syn_in.connect()
syn_in.w = -124

# Probe synaptic input using a state monitor
mon_I = LoihiStateMonitor(loihi_group, 'I')
# Probe voltage using a state monitor
mon_v = LoihiStateMonitor(loihi_group, 'v')

# NOTE: It is important to use the LoihiNetwork,
#       using Brian's magic network is not provided
net = LoihiNetwork(
    loihi_group,
    generator_in,
    generator_ex,
    syn_ex,
    syn_in,
    mon_I,
    mon_v
)

# Run the simulation
net.run(100, report='text')

# Plot synaptic input (current)
plt.plot(mon_I.I[0])
plt.title('Synaptic input / Current')
pl = plt.show()

# Plot voltage
plt.plot(mon_v.v[0])
plt.title('Voltage')
pl = plt.show()
```

## References

### Emulator

The emulator is described in

... coming soon ...

### Loihi

The Loihi chip was developed by Intel and is introduced in

[M. Davies et al., "Loihi: A Neuromorphic Manycore Processor with On-Chip Learning," in IEEE Micro, vol. 38, no. 1, pp. 82-99, January/February 2018, doi: 10.1109/MM.2018.112130359.](https://doi.org/10.1109/MM.2018.112130359)

Some further details are given in

[C. Lin et al., "Programming Spiking Neural Networks on Intel’s Loihi," in Computer, vol. 51, no. 3, pp. 52-61, March 2018, doi: 10.1109/MC.2018.157113521.](https://doi.org/10.1109/MC.2018.157113521)
