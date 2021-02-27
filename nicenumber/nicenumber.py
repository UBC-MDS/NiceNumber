import pandas as pd
import math
import re

from .__init__ import getlog

log = getlog(__name__)

# TODO should define conversion type prefixes for "filesize" or "large/small numbers" (eg B T Q etc) here at module level?

def to_human(n : float, precision : int = 0, family : str = 'number'):
    """Convert numeric value to human readable string representation

    Parameters
    ----------
    n : float
        Number to convert
    precision : int, optional
        decimal precision within string output, by default 0
    family : str, optional
        'number' or 'filesize', by default 'number'
        - (get it because humans have families!!)
        - NOTE could probably think of more types
    """

    return

def to_numeric(string:str, family:str = "number"):
    """Convert human readable string representation to numeric value

    Parameters
    ----------
    string : str
        human readable string representation to convert
    family : str, optional
        'number' or 'filesize', by default 'number'
        
    Returns
    -------
    int
    
    Examples
    --------
    >>> to_numeric(1.5M)
    1500000
    """

    return