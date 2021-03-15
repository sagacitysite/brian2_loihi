from brian2 import Synapses, ms
import re
import numpy as np
from .parameter_checks import *
from .constants import synapse_sign_mode

class LoihiSynapses(Synapses):
    """
    The LoihiSynapses extends the Synapses class from Brian2.

    This class provides Loihi parameters for delay and pre- and post-synaptic
    traces. Note that all parameters are given just as a pure integer without
    a Brain2 time unit (like e.g. ms or seconds). If parameters for one of the
    traces are not given, the trace equations are not created for this trace.

    Methods
    -------
    __init__(source, target=None, parameters ...)
        Initializes the LoihiSynapses and the Synapses
    """

    def __defineTraceEquation(self, name, imp, tau):
        """ Checks and defines trace equations from impulse and tau parameters

        This functions helps to define the trace equations for the LoihiSynapses.
        Every trace equation is optional. If parameters are empty, empty equations
        will be returned.

        Parameters
        ----------
        name : str
            The name of the trace (x1, x2, y1, etc.)
        imp : int
            The impulse of a synaptic pre or post trace
        tau : int
            The time constant of a synaptic pre or post trace

        Returns
        -------
        tuple
            a tuple containing the model equations and the on-pre/on-post equation
            each as a string
        """
        model = ''
        on = ''

        if (imp and tau):
            p = { 'v': name, 'imp': imp, 'tau': tau }

            # Check if impulse value is in a range of 0...127 and integer
            check_range_and_int(imp, 'imp_'+name, low=0, high=127)
            # Check if tau value is in a range of 0...127 and integer
            check_lower_and_int(tau, 'tau_'+name, low=0)

            model = '''
                {v}_new = {v} * exp(-1.0/{tau}) : 1
                {v}_int = int({v}_new) : 1
                {v}_frac = {v}_new - {v}_int : 1
                {v}_add_or_not = int({v}_frac > rand()) : 1 (constant over dt)
                {v}_rnd = {v}_int + {v}_add_or_not : 1
                d{v}/dt = {v}_rnd / ms : 1 (clock-driven)
            '''.format(**p)

            on = '''{v} = int(clip({v} + {imp}, 0, 127))\n'''.format(**p)

        # Remove preceding spaces and tabs from model and return model and on as tuple
        return re.sub('(?<=\\n)[ \t]*', '', model), on

    def __buildLearningRule(self, dw_raw):
        """ Takes a learning rule and returns Brian2 compatible equations

        First, the formula equation string is tested for several different problems.
        If problems are found, an exception is raised.
        Second, the equations for updating the weight and the actual weight are defined.

        Parameters
        ----------
        dw_raw : str
            The learning rule as a string, given from the user.

        Returns
        -------
        str
            The Brian2 equations to update the weight
        """

        # Trim learning rule string: remove all tabs and whitespaces
        dw = re.sub('[ \t]+', '', dw_raw)

        # First, check for division
        if (re.search('/+', dw) is not None):
            raise Exception("Division is not allowed.")

        # Check if variables are used which are not support by this package in the current version
        # This is: r0, r1, d, t
        if (re.search('(r0)+', dw) is not None):
            raise Exception("The variable 'r0' is currently not supported by this package.")
        if (re.search('(r1)+', dw) is not None):
            raise Exception("The variable 'r1' is currently not supported by this package.")
        if (re.search('d+', dw) is not None):
            raise Exception("The variable 'd' is currently not supported by this package.")
        if (re.search('t+', dw) is not None):
            raise Exception("The variable 't' is currently not supported by this package.")

        # Check if any not-allowed variable is used
        # Allowed are x0, x1, x2, y0, y1, y2, y3, u, w, 0-9, +, -, *, ^, (, )
        match = re.findall('x0|x1|x2|y0|y1|y2|y3|u[0-9]+|w|sign\(|[0-9]+|\+|-|\*|\^|\(|\)', dw)
        # Construct string again from found parts and check if it can reproduce the learning rule string
        if (''.join(match) != dw):
            raise Exception("The learing rule contains some unsupported symbols. Allowed are: x0, x1, x2, y0, y1, y2, y3, u[0-9]+, w, sign, 0-9, +, -, *, ^, (, )")

        # Check if any math symbol (+,-,*) is used in the end or if * is used in the beginning
        if (re.search('^\*', dw) is not None):
            raise Exception("'*' is not allowed as the first symbol in the equation.")
        if (re.search('[\+\*-]$', dw) is not None):
            raise Exception("'*', '+' and '-' is not allowed as the last symbol in the equation.")

        # Check if every variable has a math symbol around it
        # Predefine a symbols to search for
        group = '(x0|x1|x2|y0|y1|y2|y3|u[0-9]+|w|sign\([^)]*\))'
        match_variables_all = re.findall(group, dw)
        match_variables_correct = re.findall('(?<=[+*(-])'+group+'(?=[+*)-])', '+'+dw+'+')  # Small '+' hack to simplify regexp
        if (not np.array_equal(match_variables_all, match_variables_correct)):
            raise Exception("Some variables are not included correctly.")

        # Check if all occuring 'u's are followed by a number
        if (len(re.findall('(u(?:\D|$))', dw)) > 0):
            raise Exception(''u' must be followed by a number.')
        # The number is only allowed to start with 0, when the number has one digit
        match = re.findall('u[0-9]+.', dw+'.')  # adding '.' in the end is a trick to also match a 'u' if it's in the end
        for m in match:
            if (re.search('u[1-9][0-9]+|u[0-9][^0-9]', m) is None):
                raise Exception("If 'u' is followed by a number with more than one digit, it cannot start with a '0'.")

        # In this emulator, 'u' is only supported up to 'u9'
        if (re.search('u[0-9][0-9]+', dw) is not None):
            raise Exception("'u' is currently only supported between u0 and u9.")

        # Check if ^ is prepended by 2 and is followed by a number or +/- and a number
        # The number has to be between -7 and 9, calculations (+/-/*) are not allowed in the exponent
        # Remove matches from string, if a ^ is remaining, it is malformed
        match = re.sub('2\^\+?[0-9]|2\^-?[0-7]', '', dw)
        if (re.search('\^', match) is not None):
            raise Exception("There is a malformed '^' in the equation.")

        # Find terms in the equations and check if every term has an event variable (so called dependency factor)
        match = re.sub('(?<=\([^)])([+-])(?=.*?\))|(?<=2\^)(\+*?)(?=[0-9])|(?<=2\^)(\-*?)(?=[0-7])', '*', dw)
        for m in re.split('[\+-]', match):
            if (re.search('(x0|y0|u[0-9]+)', m) is None):
                raise Exception("There is at least one term in the equation that does not contain a dependency factor (x0, y0 or u[0-9]).")

        # Check if sign mode is mixed
        is_mixed = 1 if (self.sign_mode == synapse_sign_mode.MIXED) else 0

        # Define number of available bits
        num_bits = 8 - (self.num_weight_bits - is_mixed)

        # Define weight limit: 21 bits with last 6 bits zeros
        limit = 2**21 - 2**6

        # Define variables for equation
        p = {
            'dw': dw,
            'nb': num_bits,
            'w_exp': self.w_exp,
            'limit': limit
        }

        # Build learning rule equations
        learning_equations = '''
            u0 = 1 : 1
            u1 = int(t/ms % 2**1 == 0) : 1
            u2 = int(t/ms % 2**2 == 0) : 1
            u3 = int(t/ms % 2**3 == 0) : 1
            u4 = int(t/ms % 2**4 == 0) : 1
            u5 = int(t/ms % 2**5 == 0) : 1
            u6 = int(t/ms % 2**6 == 0) : 1
            u7 = int(t/ms % 2**7 == 0) : 1
            u8 = int(t/ms % 2**8 == 0) : 1
            u9 = int(t/ms % 2**9 == 0) : 1

            w_updated = w + {dw} : 1
            dw/dt = w_updated / ms : 1 (clock-driven)

            w_shifted = int(w_updated / 2**{nb}) * 2**{nb} : 1
            w_scaled = w_shifted * 2**(6 + {w_exp}) : 1
            w_scaled_shifted = int(floor(w_scaled / 2**6)) * 2**6 : 1
            w_clipped = clip(w_scaled_shifted, -{limit}, {limit}) : 1
            dw_act/dt = w_clipped / ms : 1 (clock-driven)

            dx0/dt = 0 / ms : 1 (clock-driven)
            dy0/dt = 0 / ms : 1 (clock-driven)
        '''.format(**p)

        # Remove preceding spaces and tabs and return
        return re.sub('(?<=\\n)[ \t]*', '', learning_equations)

    @property
    def w(self):
        """Property decorator to inclulde a getter for the weight w

        Returns
        -------
        int/list
            A single integer value or a list of weights
        """
        return self.__w

    @w.setter
    def w(self, weights):
        """Property decorator to inclulde a setter for the weight w

        A setter for the connection weight that takes weights and checks
        if weights match Loihi values. If not, exceptions are raised.

        Parameters
        ----------
        source : SpikeSource
            The source of spikes, e.g. a NeuronGroup.

        Raises
        ------
        Exception
            If weights are not integer.
        Exception
            If weights is not in range of (-255...255) for mixed syanpses sign mode,
            (0...255) for excitatory and (-255...0) for inhibitory.
        """

        # Make sure that weights are a numpy array
        weights = np.array(weights)

        # First check if all values are int
        if (weights.dtype not in  [np.dtype('int8'), np.dtype('int16'), np.dtype('int32'), np.dtype('int64')]):
            raise Exception("Weights have to be integer values.")

        # If sign mode is mixed, check weight range and round to precision
        if (self.sign_mode == synapse_sign_mode.MIXED and
            (np.any(weights < -256 or weights > 254))):
                raise Exception("Weights have to be between -256 and 254 in sign mode MIXED.")

        # If sign mode is excitatory, check range
        if (self.sign_mode == synapse_sign_mode.EXCITATORY and
            (np.any(weights < 0 or weights > 255))):
                raise Exception("Weights have to be between 0 and 255 in sign mode EXCITATORY.")

        # If sign mode is inhibitory, check range
        if (self.sign_mode == synapse_sign_mode.INHIBITORY and
            (np.any(weights < -256 or weights > 0))):
                raise Exception("Weights have to be between -256 and 0 in sign mode INHIBITORY.")

        """ Old stuff, remove
        # Check if sign mode is mixed
        is_mixed = 1 if (self.sign_mode == synapse_sign_mode.MIXED) else 0

        # Define number of available bits
        num_bits = 8 - (self.num_weight_bits - is_mixed)

        # Shift weight by number of availbale bits
        w_shifted = (weights / 2**num_bits).astype(int) * 2**num_bits

        # Scale weight with weight exponent
        w_scaled = w_shifted * 2**(6.0 + self.w_exp)

        # Shift scaled values by 6 bits back and forth
        w_scaled_shifted = (np.floor(w_scaled / 2**6)).astype(int) * 2**6

        # Clip to 21 bits with last 6 bits zeros
        # Note: We cannot clip the value before shifting it.
        #       The 2**6 shifting trick makes problems with flooring the value.
        limit = 2**21 - 2**6
        w = np.clip(w_scaled_shifted, -limit, limit)
        """

        # Store weights
        #self.__w = w
        self.__w = weights

    def __init__(
            self, source, target=None, delay=0, dw='', w_exp=0,
            sign_mode=2, num_weight_bits=8,
            imp_x1=False, tau_x1=False, imp_x2=False, tau_x2=False,
            imp_y1=False, tau_y1=False, imp_y2=False, tau_y2=False, imp_y3=False, tau_y3=False
        ):
        """ Initializes the LoihiNetwork and the Network

        The init method checks all parameters and build the equations for those
        traces, where values were given as parameters. The euqations are then
        combined and used to initialise the parent Synapses class from Brian2.
        Note that the exact_clipped method is used to match the calculation
        of the traces on Loihi.

        The source and target parameters equal the parameters from the parent class.

        Parameters
        ----------
        source : SpikeSource
            The source of spikes, e.g. a NeuronGroup.
        target : Group, optional
            The target of the spikes, typically a NeuronGroup. If none is given, the same as source().
        delay: int, optional
            The synaptic delay.
        dw: str, optional
            Learning rule, using the pre- and post-synaptic traces. Also constant values are allowed.
            Note that only `*`, `-` and `+` is allowed.
        w_exp: int, optional
            Weight exponent which scales the weights by 2^(6 + w_exp).
            The weight exponent can be between -8 and 7.
        sign_mode: int, optional
            Defines if the synapses are mixed (1), excitatory (2) or inhibitory (3).
            Excitatory synapses are default.
            `synapse_sign_mode` can be used for defining the sign mode.
        num_weight_bits: int, optional
            Defines the precision of the weight, default is 8 bits.
            `num_weight_bits` is in a range between 0 and 8.
        imp_x1: int, optional
            The impulse of the first synaptic pre trace x1.
        tau_x1: int, optional
            The time constant of the first synaptic pre trace x1.
        imp_x2: int, optional
            The impulse of the first synaptic pre trace x2.
        tau_x2: int, optional
            The time constant of the first synaptic pre trace x2.
        imp_y1: int, optional
            The impulse of the first synaptic post trace y1.
        tau_y1: int, optional
            The time constant of the first synaptic pre trace y1.
        imp_y2: int, optional
            The impulse of the first synaptic post trace y2.
        tau_y2: int, optional
            The time constant of the first synaptic pre trace y2.
        imp_y3: int, optional
            The impulse of the first synaptic post trace y3.
        tau_y3: int, optional
            The time constant of the first synaptic pre trace y3.
        """

        # Check and set synapses sign mode
        check_range_and_int(sign_mode, 'sign_mode', low=1, high=3)
        self.sign_mode = sign_mode

        # Check and set weight exponent
        check_range_and_int(w_exp, 'w_exp', low=-8, high=7)
        self.w_exp = w_exp

        # Check and set number of weight bits
        check_range_and_int(num_weight_bits, 'num_weight_bits', low=0, high=8)
        self.num_weight_bits = num_weight_bits

        # Check if impulse value is in a range of 0...62 and integer
        check_range_and_int(delay, 'delay', low=0, high=62)

        # Define weight equations
        #synaptic_input_update = '''I += w\n'''
        synaptic_input_update = '''I += w_act\n'''
        learning_rule = self.__buildLearningRule(dw)

        # Define trace equations
        x1_model, x1_pre = self.__defineTraceEquation('x1', imp_x1, tau_x1)
        x2_model, x2_pre = self.__defineTraceEquation('x2', imp_x2, tau_x2)
        y1_model, y1_post = self.__defineTraceEquation('y1', imp_y1, tau_y1)
        y2_model, y2_post = self.__defineTraceEquation('y2', imp_y2, tau_y2)
        y3_model, y3_post = self.__defineTraceEquation('y3', imp_y3, tau_y3)

        # Define dependency factors
        x0_factor = '''x0 = 1\n'''
        y0_factor = '''y0 = 1\n'''

        # Combine equations
        model = x1_model + x2_model + y1_model + y2_model + y3_model + learning_rule
        print(model)
        on_pre = synaptic_input_update + x0_factor + x1_pre + x2_pre
        print(on_pre)
        on_post = y0_factor + y1_post + y2_post + y3_post
        print(on_post)

        # Create Brian synapses
        super().__init__(
            source,
            target,
            model=model,
            on_pre=on_pre,
            on_post=on_post,
            delay=delay*ms,
            method='exact_synapse'
        )
