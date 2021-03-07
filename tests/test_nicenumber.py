import pandas as pd
import numpy as np
import pytest as pt
from nicenumber import __version__
from nicenumber import nicenumber as nn
from pytest import raises


def test_version():
    assert __version__ == '0.1.0'

def check_expected_result(func, vals : list):
    """Call function with kw args for each dict in list

    Parameters
    ----------
    func : callable
        Function to call
    vals : list
        List of dicts with kw args
    """

    for kw, expected_result in vals:
        result = func(**kw)

        # handle pd.NA without equality
        if pd.isnull(expected_result):
            assert pd.isnull(result)
        else:
            assert result == expected_result

def test_to_human():
    """Test to_human function"""
    f = nn.to_human
    
    # test 'family' ValueError raised with wrong family
    raises(ValueError, f, n=69420, family='wrong family').match('family')

    # test 'numeric' TypeError raised wth wrong input type
    raises(TypeError, f, n='69420').match('numeric')

    # test too large error is raised
    large_vals = [
        dict(n=1e30),
        dict(n=1e12, custom_suff=['apple', 'banana'])]

    for kw in large_vals:
        raises(ValueError, f, **kw).match('too large')

    # test multiple combinations of kw args with expected results
    vals = [
        (dict(n=0, prec=0), '0'),
        (dict(n=0.12, prec=2), '0.12'),
        (dict(n=4500, prec=1), '4.5K'),
        (dict(n=4500, prec=1, custom_suff=['apple', 'banana']), '4.5apple'),
        (dict(n=4510, prec=2), '4.51K'),
        (dict(n=4510.1234, prec=2), '4.51K'),
        (dict(n=4510, prec=2, currency=True), '$4.51K'),
        (dict(n=4510, prec=2, currency=True, family='filesize'), '4.51KB'),
        (dict(n=4510000, prec=2), '4.51M'),
        (dict(n=69420090000, prec=3), '69.420B'),
        (dict(n=4510000, prec=2, family='filesize'), '4.51MB'),
        (dict(n='69420090000', prec=3, errors='coerce'), pd.NA),
        (dict(n=1e30, prec=3, errors='coerce'), pd.NA)]
    
    check_expected_result(func=f, vals=vals)

def test_to_numeric():
    """Test to_numeric function"""
    f = nn.to_numeric
    
    # test 'family' ValueError raised with wrong family
    raises(ValueError, f, string = '12.2M', family='wrong family').match('family')

    # test TypeError raised with wrong input type
    raises(TypeError, f, string = [0]).match('string')

    # test 'format' TypeError raised wth wrong input type
    raises(ValueError, f, string = '69420kk').match('string')

    vals = [
        (dict(string='1.2K'), 1200.0),
        (dict(string='4.51k'), 4510.0),
        (dict(string='4.5apple', custom_suff=['apple', 'banana']), 4500),
        (dict(string='#@#$220k'), 220000.0),
        (dict(string='4.51KB', family='filesize'), 4510.0),
        (dict(string='4.51m'), 4510000.0),
        (dict(string='69.420B'), 69420000000),
        (dict(string='4.51mb', family='filesize'), 4510000.0),
        (dict(string='6942klkl', errors='coerce'), pd.NA)]

def test_to_pandas():
    """Test to_pandas function"""
    f = nn.to_pandas
    test_df = pd.DataFrame(np.array([['1_000', '1_000_000'], ['1_000_000_000', '1_000_000_000_000']]), columns=['A', 'B'])
    
    # test 'df' TypeError raised with wrong type
    raises(TypeError, f, df=[1,2,3]).match('pd.DataFrame')

    # test 'col_names' TypeError raised wth wrong input type
    raises(TypeError, f, df=test_df, col_names=1).match('str or list')

    # test 'col_names' ValueError raised wth wrong input values
    raises(ValueError, f, df=test_df, col_names=['X']).match('not present')

    # test 'transform_type' ValueError raised wth wrong input values
    raises(ValueError, f, df=test_df, transform_type='wrong').match('invalid')

    # test shape of dataframes is equal
    assert nn.to_pandas(test_df).shape == test_df.shape 

    # test convert to human, convert to numeric, see if equal
    assert test_df.equals(nn.to_pandas(nn.to_pandas(test_df), transform_type='num')) 

def test_to_color():
    """ Test to_color() function"""

    # test exception handing
    with raises(TypeError, match=r".* int .*"):
        nn.to_color('abc')

    #test one digit number
    assert nn.to_color(1, ['yellow', 'red']) == '\x1b[33m1\x1b[0m'

    #test even digits number with default color
    assert nn.to_color(1234) == '\x1b[31m1\x1b[0m\x1b[32m234\x1b[0m'

    #test a large number of digits with default color
    assert nn.to_color(123123123123123123123123123) == '\x1b[31m123\x1b[0m\x1b[32m123\x1b[0m\x1b[33m123\x1b[0m\x1b[34m123\x1b[0m\x1b[31m123\x1b[0m\x1b[32m123\x1b[0m\x1b[33m123\x1b[0m\x1b[34m123\x1b[0m\x1b[31m123\x1b[0m'

   
