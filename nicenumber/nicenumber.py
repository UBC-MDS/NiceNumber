import math
import re
from typing import Union

import numpy as np
import pandas as pd

from .__init__ import getlog

log = getlog(__name__)

# global suffix lists
suffixs = dict(
    number=['K', 'M', 'B', 'T', 'Q'],
    filesize=['KB', 'MB', 'GB', 'TB', 'PB'])

def raise_err(err, errors):
    """Internal helper func to raise err if 'raise' else pd.NA"""
    if errors == 'coerce': 
        return pd.NA
    else:
        raise err

def is_numeric(val) -> bool:
    """Check if value is float/int"""
    return issubclass(np.dtype(type(val)).type, np.number)

def check_family(family : str) -> bool:
    """Check if family in suffixes

    Parameters
    ----------
    family : str
        Family to check

    Returns
    -------
    bool
        If family exists in suffixes

    Raises
    ------
    ValueError
        If family doesn't exist in suffixes
    """    
    if not family in suffixs:
        raise ValueError(
            f'Invalid family: "{family}". Valid options: {list(suffixs)}')

def get_suffix(
    family : str,
    custom_suff : Union[list, None] = None,
    lower : bool = False):
    """Get suffix list

    Parameters
    ----------
    family : str
        Family of suffixes
    custom_suff : Union[list, None], optional
        List of custom suffixes, default None
    lower : bool, optional
        Lowercase vals or not, default False

    Returns
    -------
    list
        List of suffixes
    """        
    suffix_list = [''] + (custom_suff or suffixs.get(family))
    return suffix_list if not lower else [s.lower() for s in suffix_list]

def to_human(
    n : float,
    prec : int = 0,
    family : str = 'number',
    custom_suff : Union[list, None] = None,
    currency : bool = False,
    currency_sym : str = '$',
    errors : str = 'raise') -> str:
    """Convert numeric value to human readable string representation

    Parameters
    ----------
    n : float
        Number to convert
    prec : int, optional
        Decimal precision within string output, by default 0
    family : str, optional
        Suffix family, ['number', 'filesize'], default 'number'
    custom_suff : Union[list, None], optional
        List of custom suffixes, default None
    currency : bool, optional
        Add currency symbol, default False
    currency_sym : str, optional
        Currency symbol, default '$'
    errors : str
        'raise', 'coerce', default 'raise'
        If 'raise', then invalid parsing will raise an exception.
        If 'coerce', then invalid parsing will return pd.NA.

    Returns
    -------
    str
        Formatted number

    Examples
    --------
    >>> from nicenumber import nicenumber as nn
    >>> n = 69420
    >>> nn.to_human(n, prec=1, family='number')
    >>> '69.4K'
    """

    # assert correct dtype
    if not is_numeric(n):
        err = TypeError(f'Value must be numeric, not "{type(n)}". Invalid value: "{n}"')
        return raise_err(err, errors)

    # assert family in suffixs
    check_family(family=family)

    # calculate final number and index position for suffix
    base = 3
    order = 0 if n == 0 else int(math.log10(abs(n)) // 1)
    idx = int(order / base)
    number = n / 10 ** (3 * idx)

    suffix_list = get_suffix(family, custom_suff)

    # check if number is too large for conversion
    max_len = len(suffix_list) - 1

    if idx > max_len:
        err = ValueError(
            'Number too large for conversion. Maximum order: 100e{e} ({suff})' \
                .format(
                    e=max_len * base,
                    suff=suffix_list[-1]))

        return raise_err(err, errors)

    if not family == 'number':
        currency = False

    return '{currency_sym}{number:.{prec}f}{suffix}'.format(
        currency_sym=currency_sym if currency else '',
        number=number,
        prec=prec,
        suffix=suffix_list[idx])

def to_numeric(
    string : str,
    family : str = 'number',
    custom_suff : Union[list, None] = None,
    errors : str = 'raise'):
    """Convert human readable string representation to numeric value

    Parameters
    ----------
    string : str
        human readable string representation to convert
    family : str, optional
        Suffix family, ['number', 'filesize'], default 'number'
    custom_suff : Union[list, None], optional
        List of custom suffixes, default None
    errors : str
        'raise', 'coerce', default 'raise'
        If 'raise', then invalid parsing will raise an exception.
        If 'coerce', then invalid parsing will return pd.NA.
        
    Returns
    -------
    float
    
    Examples
    --------
    >>> to_numeric('1.5M')
    1500000
    """

    # check if string can be converted to a number    
    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False
        
    # test whether input string can be convert to number
    if is_float(string):
        return float(string)

    # get rid of symbols before digit
    string = re.sub(r'^[\D]+', '', string)

    # assert type of string 
    if not isinstance(string, str):
        err = TypeError(
            f'Input value must be a string or number, not "{type(string)}". Invalid value: "{string}"')

        return raise_err(err, errors)

    # assert family in suffixs
    check_family(family=family)
    
    # get suffix list as all lower
    suffix_list = get_suffix(family, custom_suff, lower=True)

    # extract suffix as all alphanumeric characters at end of string
    suff = re.search(r'[a-zA-Z]*$', string, flags=re.IGNORECASE)[0].lower()
    
    base = 10 ** 3

    if not suff in suffix_list: 
        err = ValueError(
            f'Invalid string suffix: "{suff}". Valid options: {suffix_list}')
        return raise_err(err, errors)

    power = suffix_list.index(suff)

    # extract number from string
    # pattern = digit one or more times, decimal zero or more, digit one or more
    number = re.search(r'\d+\.*\d*', string)[0]
    return float(number) * (base ** power)

def to_pandas(df : pd.DataFrame, col : Union[str, list], transform_type : str ='human', family : str ='number'):
    """Change the formatting of text in column(s) of data in a dataframe

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        dataframe to apply formatting
    col : str, list
        list of column(s) to apply formatting
    transform_type : str
        type of transformation, either 'human' (default) for human readable format or 'num' for numeric format
    family : str, optional
        'number' or 'filesize', by default 'number'

    Returns
    ----------
    df : pandas.core.frame.DataFrame
    When passed to a style function call, returns a dataframe with the values in columns A, B and C converted to a human readable numeric format.

    Examples
    ----------
    >>> df.style.apply(to_pandas, col=['A','B','C'])
    """      

    return

def to_color(number:int, color:list = None):
    """Give all parts of the number with different colors

    Parameters
    ----------
    number : int
        Integer number to be colored
    color : list, optional
        List of colors, by default includes 'Red', 'Green', 'Yellow' and 'Blue'

    Returns
    -------
    str
        String number with different colors
    """

    return ""
