import math
import re
from typing import Union

import numpy as np
import pandas as pd


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


def check_family(family: str) -> bool:
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
        family: str,
        custom_suff: Union[list, None] = None,
        lower: bool = False) -> list:
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
        n: float,
        prec: int = 0,
        family: str = 'number',
        custom_suff: Union[list, None] = None,
        currency: bool = False,
        currency_sym: str = '$',
        errors: str = 'raise',
        **kw) -> str:
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
        err = TypeError(
            f'Value must be numeric, not "{type(n)}". Invalid value: "{n}"')
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
            'Number too large for conversion. Maximum order: 100e{e} ({suff})'
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
        string: str,
        family: str = 'number',
        custom_suff: Union[list, None] = None,
        errors: str = 'raise',
        **kw) -> float:
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

    # if input is number, just return
    if is_numeric(string):
        return float(string)

    # assert type of string
    if not isinstance(string, str):
        err = TypeError(
            f'Input value must be a string or number, not "{type(string)}". Invalid value: "{string}"')

        return raise_err(err, errors)

    # get rid of symbols before digit
    string = re.sub(r'^[\D]+', '', string)

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
    # pattern = digit one or more times, decimal zero or more, digit zero or more
    number = re.search(r'\d+\.*\d*', string)[0]
    return float(number) * (base ** power)


def to_pandas(
        df: pd.DataFrame,
        col_names: Union[str, list] = None,
        transform_type: str = 'human',
        family: str = 'number',
        **kw) -> pd.DataFrame:
    """Change the formatting of data in column(s) of a dataframe to either human readable or numeric

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        dataframe to apply formatting
    col_names : Union[str, list], optional
        list of column(s) names to apply formatting to, default is all columns
    transform_type : str
        type of transformation, either 'human' (default) for human readable format or 'num' for numeric format
    family : str, optional
        'number' or 'filesize', by default 'number'
    **kw : kw args
        extra args to pass to conversion function

    Returns
    ----------
    df : pandas.core.frame.DataFrame
        dataframe with the values in user specified columns transformed to a formatting of their choice

    Examples
    ----------
    >>> to_pandas(df, col_names=['A', 'B', 'C'], transform_type='human')
    """

    if not type(df) == pd.DataFrame:
        raise TypeError(
            'Input must be of type pd.DataFrame')

    # TODO -> Add additional arguments option such as precision, etc. if time
    if col_names is None:
        col_names = df.columns.tolist()

    if not isinstance(col_names, (str, list)):
        raise TypeError(
            'col_names must be of type str or list')

    if any(not item in df.columns for item in col_names):
        raise ValueError(
            'One or more columns not present in dataframe!')

    # convert transform type to function for df.assign
    m_funcs = dict(
        human=to_human,
        num=to_numeric,
        color=to_color)

    func = m_funcs.get(transform_type, None)

    if func is None:
        raise ValueError(
            f'Invalid transform_type. Valid options: {list(m_funcs.keys())}')

    # create dict of eg {column_name: to_human(**kw)} for each col to convert
    assign_cols = {col: lambda df: df[col].apply(
        func, **kw) for col in col_names}

    return df.assign(**assign_cols)


def to_color(
        number: int,
        color: list = None,
        errors: str = 'raise',
        **kw) -> str:
    """Give all parts of the number with different colors

    Parameters
    ----------
    number : int
        Integer number to be colored
    color : list, optional
        List of colors, by default includes 'red', 'green', 'yellow' and 'blue'
    errors : str
        'raise', 'coerce', default 'raise'
        If 'raise', then invalid parsing will raise an exception.
        If 'coerce', then invalid parsing will return pd.NA.

    Returns
    -------
    str
        String number with different colors

    Examples
    ----------
    >>> print(to_color(13637373737348738787, ['yellow', 'red']))
    """
    palette = dict(
        black=30,
        red=31,
        green=32,
        yellow=33,
        blue=34,
        cyan=36,
        white=37,
        underline=4,
        reset=0)

    # create full color codes as a dict comp
    palette = {k: f'\033[{color_code}m' for k, color_code in palette.items()}

    # print(number)
    if not is_numeric(number):
        err = TypeError('Input number should be int type')
        return raise_err(err, errors)

    c = ['red', 'green', 'yellow', 'blue'] if color is None else color

    d = str(number)
    offset = len(d) % 3
    if offset != 0:
        s = [d[0:offset]] + [d[i:i + 3] for i in range(offset, len(d), 3)]
    else:
        s = [d[i:i + 3] for i in range(offset, len(d), 3)]

    ans = ''

    for i, num in enumerate(s):
        fill = palette[c[i % len(c)]]
        ans += fill
        ans += num
        ans += palette['reset']

    return ans
