import pandas as pd
import math
import re

from typing import Union

#from .__init__ import getlog

#log = getlog(__name__)

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

    Examples
    ----------
    >>> print(to_color(13637373737348738787, ['Yellow', 'Red']))
    """

    
    palette = {'Black':'\033[30m', 'Red':'\033[31m', 'Green':'\033[32m', 'Yellow':'\033[33m', 'Blue':'\033[34m', 'Cyan':'\033[36m', 'White':'\033[37m', 'Underline':'\033[4m', 'Reset':'\033[0m'}
    c = ['Red', 'Green', 'Yellow', 'Blue'] if color==None else color
    
    d = str(number)
    offset = len(d)%3
    if offset != 0:
        s = [d[0:offset]]+[d[i:i+3] for i in range(offset, len(d), 3)]
    else:
        s = [d[i:i+3] for i in range(offset, len(d), 3)]

    ans = ''

    for i, num in enumerate(s):
        fill = palette[c[i%len(c)]]
        ans += fill
        ans += num
        ans += palette['Reset']

    return ans



if __name__ == '__main__':
    print(to_color(13637373737348738787, ['Yellow', 'Red']))