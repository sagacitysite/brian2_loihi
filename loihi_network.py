from brian2 import Network, ExplicitStateUpdater, StateUpdateMethod, defaultclock, ms
import warnings

class LoihiNetwork(Network):
    """
    The LoihiNetwork extends the Network class from Brian2.

    Note that it is important to use the LoihiNetwork class and not the magic network.

    Methods
    -------
    __init__(*objs, **kwds)
        Initializes the LoihiNetwork and the Network
    run(duration, **kwargs)
        Checks for problems and runs the Brian network simulation
    """

    def __init__(self, *objs, **kwds):
        """ Initializes the LoihiNetwork and the Network

        This method registers two ExplicitStateUpdater as StateUpdateMethod. These update
        methods are used by Loihi to integrate diffeential equations. Further, the dt is
        set to 1, again to match a Loihi simulation. Afterwards the __init__() method from
        the Brian2 Network is called, initializing a default Brian2 network. Finally, the
        default schedule from Brian2 is reordered to match Loihi. All arguments are passed
        to the parent init method.

        Parameters
        ----------
        *objs :
            All arguments defined by the parent class
        **kwds : optional
            All keyword arguments defined by the parent class
        """

        # Define first order forward euler, if not already defined
        if ('forward_euler' not in StateUpdateMethod.stateupdaters):
            eq_forward_euler = '''
            x_new = x + dt * f(x,t)
            '''
            forward_euler = ExplicitStateUpdater(eq_forward_euler, stochastic='none')
            StateUpdateMethod.register('forward_euler', forward_euler)

        # Define exact state updater for the pre/post traces for learning, if not already defined
        if ('exact_synapse' not in StateUpdateMethod.stateupdaters):
            eq_exact_synapse = '''
                x_0 = dt*f(x,t)
                x_new = int(x_0)
            '''
            exact_synapse = ExplicitStateUpdater(eq_exact_synapse, stochastic='none')
            StateUpdateMethod.register('exact_synapse', exact_synapse)

        # Set default clock dt
        defaultclock.dt = 1*ms

        # Call super init
        super().__init__(*objs, **kwds)

        # Reorder schedule to match Loihi
        self.schedule = ['start', 'synapses', 'groups', 'thresholds',  'resets', 'end']

    def run(self, duration, **kwargs):
        """ Checks for problems and runs the Brian network simulation

        The run method overwrites the run method from the Network class. Just before running
        the simulation, it checks if the most important settings are still valid. If not, a
        warning is shown. The user should be able to choose other settings, but should be warned
        that results can then vary from Loihi. Afterwards the parent run() method is called.
        The duration is modified, such that the LoihiNetwork run() method will only take an integer
        without Brian's time information (e.g. ms). All keyword arguments are passed to the
        parent run() method.

        Parameters
        ----------
        duration : int
            Duration of the simulation as an integer value, no time (e.g. ms) should to be added
        **kwargs : optional
            All keyword arguments defined by the parent method

        Raises
        ------
        Warning
            If defautlclock dt value has changed and is not set to 1ms any more
        Warning
            If the schedule has changed and is not in the Loihi-like order any more
        """

        # Check if the user has manually changed defaultclock and print warning
        if (defaultclock.dt != 1*ms):
            warnings.warn("The defaultclock.dt is not set to 1*ms, this may cause results which deviate from Loihi.")

        # Check if the user has manually changed schedule and print warning
        if (self.schedule != ['start', 'synapses', 'groups', 'thresholds',  'resets', 'end']):
            warnings.warn("The schedule has changed, this may cause results which deviate from Loihi.")

        # Call run method from Brian Network
        super().run(duration*ms, **kwargs)
