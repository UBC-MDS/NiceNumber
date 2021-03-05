import pandas as pd
import pytest as pt
from nicenumber import __version__
from nicenumber import nicenumber as nn
from pytest import raises


def test_version():
    assert __version__ == '0.1.0'

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
        (dict(n=4510, prec=2), '4.51K'),
        (dict(n=4510.1234, prec=2), '4.51K'),
        (dict(n=4510, prec=2, currency=True), '$4.51K'),
        (dict(n=4510, prec=2, currency=True, family='filesize'), '4.51KB'),
        (dict(n=4510000, prec=2), '4.51M'),
        (dict(n=69420090000, prec=3), '69.420B'),
        (dict(n=4510000, prec=2, family='filesize'), '4.51MB'),
        (dict(n='69420090000', prec=3, errors='coerce'), pd.NA),
        (dict(n=1e30, prec=3, errors='coerce'), pd.NA)]

    for kw, expected_result in vals:
        result = f(**kw)

        # handle pd.NA without equality
        if expected_result is pd.NA:
            assert result is pd.NA
        else:
            assert result == expected_result

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
        (dict(string = '4.51k'), 4510.0),
        (dict(string= '#@#$220k'), 220000.0),
        (dict(string ='4.51KB',  family='filesize'), 4510.0),
        (dict(string = '4.51m'), 4510000.0),
        (dict(string = '69.420B'), 69420000000),
        (dict(string = '4.51mb', family='filesize'), 4510000.0),
        (dict(string = '6942klkl',  errors='coerce'), pd.NA)]