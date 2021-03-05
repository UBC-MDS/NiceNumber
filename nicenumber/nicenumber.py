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

    def raise_err(err):
        """Internal helper func to raise err if 'raise' else pd.NA"""
        if errors == 'coerce':
            return pd.NA
        else:
            raise err

    # assert correct dtype
    if not issubclass(np.dtype(type(n)).type, np.number):
        err = TypeError(f'Value must be numeric, not "{type(n)}". Invalid value: "{n}"')
        return raise_err(err)

    # assert family in suffixs
    if not family in suffixs:
        raise ValueError(
            f'Invalid family: "{family}". Valid options: {list(suffixs)}')

    # calculate final number and index position for suffix
    base = 3
    order = 0 if n == 0 else int(math.log10(abs(n)) // 1)
    idx = int(order / base)
    number = n / 10 ** (3 * idx)

    # get suffix from list of suffixes
    suffix_list = [''] + (custom_suff or suffixs.get(family))

    # check if number is too large for conversion
    max_len = len(suffix_list) - 1

    if idx > max_len:
        err = ValueError(
            'Number too large for conversion. Maximum order: 100e{e} ({suff})' \
                .format(
                    e=max_len * base,
                    suff=suffix_list[-1]))

        return raise_err(err)

    if not family == 'number':
        currency = False

    return '{currency_sym}{number:.{prec}f}{suffix}'.format(
        currency_sym=currency_sym if currency else '',
        number=number,
        prec=prec,
        suffix=suffix_list[idx])

def to_numeric(string:str, family:str = 'number'):
    """Convert human readable string representation to numeric value

    Parameters
    ----------
    string : str
        human readable string representation to convert
    family : str, optional
        'number' or 'filesize', by default 'number'
        
    Returns
    -------
    float
    
    Examples
    --------
    >>> to_numeric(1.5M)
    1500000
    """

    return

def to_pandas(df : pd.DataFrame, col_names : Union[str, list] = df.columns.values.tolist(), transform_type : str ='human', family : str ='number'):
    """Change the formatting of data in column(s) of a dataframe to either human readable or numeric

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        dataframe to apply formatting
    col_names : Union[str, list], optional
        list of column(s) names to apply formatting to, default is all columns
    transform_type : str
        type of transformation, either 'human' (default) for human readable format or 'num' for numeric format

    Returns
    ----------
    df : pandas.core.frame.DataFrame
    Returns a dataframe with the values in user specified columns transformed to a formatting of their choice

    Examples
    ----------
    >>> to_pandas(df, col_names=['A', 'B', 'C'], transform_type='human')
    For discussion with group: My function isn't actually modifying the style at all so I don't think we need the df.style.applymap here
    """     
    # test ideas: 
    # check if dataframe object passed to function
    # check datatypes in dataframe (must be numeric)

    # Loop through input variable col_names (default is all) and rows in df
    # Check transform type to apply to df
    # Apply transformations element-wise
    # TODO -> Add additional arguments option such as precision, etc. 
    for col in col_names:
        for row in df.index:
            if transform_type == 'human':
                df.loc[df.index[row], col] = to_human(float(df.loc[df.index[row], col]))
            elif transform_type == 'num':
                df.loc[df.index[row], col] = to_numeric(float(df.loc[df.index[row], col]))
            # should we add a color option too????
            #elif transform_type == 'color':
            #    df.loc[df.index[row], col] = to_color(df.loc[df.index[row], col])

    return df

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
