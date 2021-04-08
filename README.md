# A Loihi emulator based on Brian2

The package extends *Brian2* classes such that they match Loihi simulations. While the neuron and synapse model results in an exact match to *Loihi*, the pre- and post-synaptic traces have very small variations from the *Loihi* chip due to stochastic rounding.

Further details are explained in a paper coming soon.

## Installation

```
pip install brian2-loihi
```

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

### LoihiSynapses

Extends the `Synapses` class from *Brian2* and supports the following parameters:

* **source** (`SpikeSource`): The source of spikes, e.g. a NeuronGroup.
* **target** (`Group`, optional): The target of the spikes, typically a NeuronGroup. If none is given, the same as source().
* **delay** (int, optional): The synaptic delay.
* **dw** (str, optional): Learning rule, using the pre- and post-synaptic traces. Also constant values are allowed. Note that only `*`, `-` and `+` is allowed.
* **w_exp** (int, optional): Weight exponent which scales the weights by 2^(6 + w_exp). The weight exponent can be between -8 and 7.
* **sign_mode** (int, optional): Defines if the synapses are mixed (1), excitatory (2) or inhibitory (3). Excitatory synapses are default. `synapse_sign_mode` can be used for defining the sign mode.
* **num_weight_bits** (int, optional): Defines the precision of the weight, default is 8 bits. `num_weight_bits` is in a range between 0 and 8.
* **imp_x1** (int, optional): The impulse of the first synaptic pre trace x1.
* **tau_x1** (int, optional): The time constant of the first synaptic pre trace x1.
* **imp_x2** (int, optional): The impulse of the first synaptic pre trace x2.
* **tau_x2** (int, optional): The time constant of the first synaptic pre trace x2.
* **imp_y1** (int, optional): The impulse of the first synaptic post trace y1.
* **tau_y1** (int, optional): The time constant of the first synaptic pre trace y1.
* **imp_y2** (int, optional): The impulse of the first synaptic post trace y2.
* **tau_y2** (int, optional): The time constant of the first synaptic pre trace y2.
* **imp_y3** (int, optional): The impulse of the first synaptic post trace y3.
* **tau_y3** (int, optional): The time constant of the first synaptic pre trace y3.

### LoihiStateMonitor

Extends the `StateMonitor` class from *Brian2* and supports the following parameters:

* **source** (`Group`): Which object to record values from.
* **variable** (str): Which variables to record, check the `state` object for details.
* **record** (bool, sequence of ints): Which indices to record, nothing is recorded for ``False``, everything is recorded for ``True`` (warning: may use a great deal of memory), or a specified subset of indices.
* **order** (int, optional): The priority of of this group for operations occurring at the same time step and in the same scheduling slot. Defaults to 0.

### LoihiSpikeMonitor

Extends the `SpikeMonitor` class from *Brian2* and supports the following parameters:

* **source** (`Group`): Which object to record values from.
* **variable** (str): Which variables to record at the time of the spike (in addition to the index of the neuron). Can be the name of a variable or a list of names
* **record** (bool, sequence of ints): Which indices to record, nothing is recorded for ``False``, everything is recorded for ``True`` (warning: may use a great deal of memory), or a specified subset of indices.
* **order** (int, optional): The priority of of this group for operations occurring at the same time step and in the same scheduling slot. Defaults to 0.

### LoihiSpikeGeneratorGroup

Extends the `SpikeGeneratorGroup` class from *Brian2* and supports the following parameters:

* **N** (int): The number of "neurons" in this group
* **indices** (array of integers): The indices of the spiking cells
* **times** (list (int)): The spike times for the cells given in ``indices``. Has to have the same length as ``indices`` and has to be integer (without time units)
* **period** (int, optional): If this is specified, it will repeat spikes with this period. A period of 0 means not repeating spikes.
* **order** (int, optional): The priority of of this group for operations occurring at the same time step and in the same scheduling slot. Defaults to 0.
* **sorted** (bool, optional):  Whether the given indices and times are already sorted. Set to ``True`` if your events are already sorted (first by spike time, then by index), this can save significant time at construction if your arrays contain large numbers of spikes. Defaults to ``False``.

## Example

Follows soon
