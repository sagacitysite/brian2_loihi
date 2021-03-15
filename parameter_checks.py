def check_range_and_int(val, name, low=0, high=127):
    """Checks a parameter to match Loihi

    Calls two methods to check if the parameter value is
    integer and in a range between low and high.

    Parameters
    ----------
    val : int
        The value of the parameter
    name : str
        The name of the parameter
    low : int, optional
        The lower bound of the parameter
    high : int, optional
        The upper bound of the parameter
    """
    check_int(val, name)
    check_range(val, name, low, high)

def check_lower_and_int(val, name, low=0):
    """Checks a parameter to match Loihi

    Calls two methods to check if the parameter value is
    integer and in greater than low.

    Parameters
    ----------
    val : int
        The value of the parameter
    name : str
        The name of the parameter
    low : int, optional
        The lower bound of the parameter
    """
    check_int(val, name)
    check_lower(val, name, low)

def check_lower(val, name, low=0):
    """Checks if a parameter is greater or equal than low

    Parameters
    ----------
    val : int
        The value of the parameter
    name : str
        The name of the parameter
    low : int, optional
        The lower bound of the parameter

    Raises
    ------
    Exception
        If value is lower than low.
    """
    if (val < low):
        raise Exception(str(name) + " has to be greater or equal to " +str(low)+ ".")

def check_range(val, name, low=0, high=127):
    """Checks if a parameter is between low and high

    Parameters
    ----------
    val : int
        The value of the parameter
    name : str
        The name of the parameter
    low : int, optional
        The lower bound of the parameter
    high : int, optional
        The upper bound of the parameter

    Raises
    ------
    Exception
        If value is lower than low of greater than high.
    """
    if (val < low) or (val > high):
        raise Exception(str(name) + " has to be between " +str(low)+ " and " +str(high)+ ".")

def check_int(val, name):
    """Checks if a parameter is of type integer

    Parameters
    ----------
    val : int
        The value of the parameter
    name : str
        The name of the parameter

    Raises
    ------
    Exception
        If value not integer
    """
    if not isinstance(val, int):
        raise Exception(str(name) + " has to be an integer.")
