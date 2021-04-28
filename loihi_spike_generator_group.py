from brian2 import SpikeGeneratorGroup, second, ms

class LoihiSpikeGeneratorGroup(SpikeGeneratorGroup):
    """
    The LoihiSpikeGeneratorGroup extends the SpikeGeneratorGroup class from Brian2.

    This class creates a spike generator which gets times as integer (without time
    units). In addition the schedule of the generator is updated to meet Loihi.
    The period parameter from the parent initialization method is complemented
    with a unit inside of the function (as the times parameter).

    Methods
    -------
    __init__(N, indices, times, period=0, order=0, sorted=False)
        Initializes the LoihiSpikeGeneratorGroup and the SpikeGeneratorGroup
    """
    def __init__(self, N, indices, times, period=0, order=0, sorted=False, name='loihi_spikegeneratorgroup*'):
        """ Initializes the SpikeGeneratorGroupLoihi and the SpikeGeneratorGroup

        The init method adds time units to the times and period parameters.
        In addition the when property of the SpikeGeneratorGroup is changed to 'start'.
        All parameters are already part of the init method of the SpikeGeneratorGroup
        class and are just modified.

        Parameters
        ----------
        N : int
            The number of "neurons" in this group
        indices : array of integers
            The indices of the spiking cells
        times : list (int)
            The spike times for the cells given in ``indices``. Has to have the
            same length as ``indices`` and has to be integer (without time units)
        period : int, optional
            If this is specified, it will repeat spikes with this period. A
            period of 0 means not repeating spikes.
        order : int, optional
            The priority of of this group for operations occurring at the same time
            step and in the same scheduling slot. Defaults to 0.
        sorted : bool, optional
            Whether the given indices and times are already sorted. Set to ``True``
            if your events are already sorted (first by spike time, then by index),
            this can save significant time at construction if your arrays contain
            large numbers of spikes. Defaults to ``False``.
        name : str, optional
            A unique name for the object, otherwise will use
            ``loihi_spikegeneratorgroup_0'``, etc.
        """

        # Define Brian spike generator group
        super().__init__(
            N,
            indices,
            times*ms,
            period=period*second,
            order=order,
            sorted=sorted,
            when='start',  # Update schedule
            name=name
        )
