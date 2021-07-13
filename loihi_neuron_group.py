from brian2 import NeuronGroup, ms
import re
from .parameter_checks import *

class LoihiNeuronGroup(NeuronGroup):
    """
    The LoihiNeuronGroup extends the NeuronGroup class from Brian2.

    This class defines the Loihi neuron model as differential equations,
    which are then defined in Brian2. Finally the Brian2 NeuronGroup is
    initialized with this neuron model.

    Methods
    -------
    __init__(N, refractory=1, threshold_v_mant=100, decay_v=0, decay_I=4096)
        Initializes the LoihiNeuronGroup and the NeuronGroup
    """

    def __init__(self, N, refractory=1, threshold_v_mant=100, decay_v=0, decay_I=4096, name='loihi_neurongroup*'):
        """ Initializes the LoihiStateMonitor and the StateMonitor

        The init method checks if the given parameters are valid. Afterwards the
        equations for the neuron model are defined. Finally, the Brian2 NeuronGroup
        is initialized. Parameters are given as integers, not time units
        (seconds, ms, etc.) should be used. They are added by this method automatically.
        As integration method, forward euler is used.

        Parameters
        ----------
        N : int
            Number of neurons in the group.
        refractory: int (1...64), optional
            The refactory period of the neuron.
        threshold_v_mant: int (0...131071), optional
            The mantissa of the membrane voltage threshold.
        decay_v : int (0...4096), optional
            The membrane voltage decay (note that tau_v = 4096/decay_v)
        decay_I : int (0...4096), optional
            The current decay (note that tau_I = 4096/decay_I)
        name : str, optional
            A unique name for the group, otherwise use ``loihi_neurongroup_0``, etc.
        """

        # Check if tau values are in a range of 0...4096 and integer
        check_range_and_int(decay_v, 'decay_v', low=0, high=4096)
        check_range_and_int(decay_I, 'decay_I', low=0, high=4096)

        # Check if refactory period is in a range of 1...64 and integer
        check_range_and_int(refractory, 'refractory', low=1, high=64)

        # Check if threshold_v_mant is in a range of 0...131071 and integer
        check_range_and_int(threshold_v_mant, 'threshold_v_mant', low=0, high=131071)

        # Define parameters for equation
        # Note: tau is inversed to avoid division by zero
        p = {
            '1_tau_v': decay_v/2**12,  # 1/tau_v
            '1_tau_I': decay_I/2**12,  # 1/tau_I
            'v_th': threshold_v_mant * 2**6
        }

        # Define parameters for printing
        self.loihi_parameters = {
            **p,
            'decay_v': decay_v,
            'decay_I': decay_I,
            'tau_v': 2**12/decay_v,
            'tau_I': 2**12/decay_I,
            'refractory': refractory,
            'threshold_v_mant': threshold_v_mant,
            'reset_v': 0
        }

        # Neuron model
        equations_LIF = '''
            rnd_v = int(sign(v)*ceil(abs(v*{1_tau_v}))) : 1
            rnd_I = int(sign(I)*ceil(abs(I*{1_tau_I}))) : 1
            dv/dt = -rnd_v/ms + I/ms: 1 (unless refractory)
            dI/dt = -rnd_I/ms: 1
        '''.format(**p)

        # Create Brian neuron group

        super().__init__(
            N,
            re.sub('(?<=\\n)[ \t]*', '', equations_LIF),
            threshold='v > {v_th}'.format(**p),
            reset='v = 0',
            refractory=refractory*ms,
            method='forward_euler',
            name=name
        )

        # Set initial voltage
        self.v = 0

    def __str__(self):
        """Creates a user friendly overview over all parameters

        This function makes it easy to get a transparent overview over all neuron group parameters.
        Call: print(LoihiNeuronGroup.__str__())
        """
        print_string = 'Parameters of the neuron group:\n\n'
        for key, value in self.loihi_parameters.items():
            print_string += '{:18} {:}\n'.format(key, value)

        return print_string
