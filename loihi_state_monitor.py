from brian2 import StateMonitor

class LoihiStateMonitor(StateMonitor):
    """
    The LoihiStateMonitor extends the StateMonitor class from Brian2.

    This class creates a Brian2 state monitor and updates the schedule for
    reading the monitored values. This schedule change is performed to
    produce the same outputs as in Loihi.

    Methods
    -------
    __init__(source, variable, record=True, order=0)
        Initializes the LoihiStateMonitor and the StateMonitor
    """

    def __init__(self, source, variable, record=True, order=0, name='loihi_statemonitor*'):
        """ Initializes the LoihiStateMonitor and the StateMonitor

        First, a StateMonitor is initialized, based on the given parameters.
        Afterwards, the schedule for monitoring the values is updated. For
        parameters relating to the neuron, the 'end' has to be chosen. And
        for those telating to the synapse, the 'synapses' has to be chosen.

        Parameters
        ----------
        source : `Group`
            Which object to record values from.
        variable : str
            Which variable to record, check the `state` object for details.
        record : bool, sequence of ints
            Which indices to record, nothing is recorded for ``False``,
            everything is recorded for ``True`` (warning: may use a great deal of
            memory), or a specified subset of indices.
        order : int, optional
            The priority of of this group for operations occurring at the same time
            step and in the same scheduling slot. Defaults to 0.
        name : str, optional
            A unique name for the object, otherwise will use
            ``source.name+'loihi_statemonitor_0'``, etc.
        """

        # Check if only one varibable is given
        if isinstance(variable, list):
            raise Exception('In the Loihi emulator, you can only define one varible in every state monitor. If you need to probe more variables, create another state monitor.')

        # Define Brian state monitor
        super().__init__(
            source,
            variable,
            record=record,
            order=order,
            name=name
        )

        # Update when states should be monitored
        if (variable in ['v', 'w', 'w_act']):
            self.when = 'end'
        #if (variable in ['I', 'x1', 'x2', 'y1', 'y2', 'y3', 'w', 'w_act']):
        if (variable in ['I', 'x1', 'x2', 'y1', 'y2', 'y3']):
            self.when = 'synapses'
    #@property
    #def t(self):
        """
        Returns t as ints without ms
        """
    #    return self._t/ms