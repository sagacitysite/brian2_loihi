from brian2 import SpikeMonitor

class LoihiSpikeMonitor(SpikeMonitor):
    """
    The LoihiSpikeMonitor extends the SpikeMonitor class from Brian2.

    This class creates a Brian2 spike monitor and updates the schedule for
    reading the monitored values. This schedule change is performed to
    produce the same outputs as in Loihi.

    Methods
    -------
    __init__(source, variable, record=True, order=0)
        Initializes the LoihiSpikeMonitor and the SpikeMonitor
    """

    @property
    def t(self):
        """ Property decorator to inclulde a getter for the spike times
        Returns
        -------
        list (int)
            Return spike times as int
        """
        return (self.t_*1000).astype(int)

    def __init__(self, source, variable=None, record=True, order=None, name='loihi_spikemonitor*'):
        """ Initializes the LoihiSpikeMonitor and the SpikeMonitor

        First, a SpikeMonitor is initialized, based on the given parameters.
        Afterwards, the schedule for monitoring the values is updated.
        Parameters
        ----------
        source : `Group`
            Which object to record values from.
        variable : str, optional
            Which variables to record at the time of the spike (in addition to the index of the neuron).
            Can be the name of a variable or a list of names
        record : bool, sequence of ints, optional
            Which indices to record, nothing is recorded for ``False``,
            everything is recorded for ``True`` (warning: may use a great deal of
            memory), or a specified subset of indices.
        order : int, optional
            The priority of of this group for operations occurring at the same time
            step and in the same scheduling slot. Defaults to 0.
        name : str, optional
            A unique name for the object, otherwise will use
            ``source.name+'_loihi_spikemonitor_0'``, etc.
        """

        # Define Brian spike monitor
        super().__init__(
            source,
            variable,
            record=record,
            order=order,
            name=name
        )

        # Update when states should be monitored
        self.when = 'end'
