# NiceNumber 

![](https://github.com/camharris22/nicenumber/workflows/build/badge.svg) [![codecov](https://codecov.io/gh/camharris22/nicenumber/branch/main/graph/badge.svg)](https://codecov.io/gh/camharris22/nicenumber) ![Release](https://github.com/camharris22/nicenumber/workflows/Release/badge.svg) [![Documentation Status](https://readthedocs.org/projects/nicenumber/badge/?version=latest)](https://nicenumber.readthedocs.io/en/latest/?badge=latest)

This Python package provides basic functions that make numbers display nicely. In most real-world problems, the datasets are raw and we need to deal with number formats to make them readable for humans or for computers. Usually, a few or more lines of coding are needed while dealing with number-display problems so we are thinking of compressing the time and programming work on this issue. This package solves this kind of problems in a way of transfer forward and backward from long digit numbers to human-readable ones. There are functions doing single number transactions, column transactions from a pandas data frame, and displaying colors of input numbers.  

## Installation

```bash
$ pip install -i https://test.pypi.org/simple/ nicenumber
```

## Features

There are four functions in this package:

- `to_human`
This function converts numeric value to human-readable string representations. Users need to use a specific number as input and choose decimal precision and prefixes of filesize or numbers as optionals. The function will return a human-readable string.

```python
import nicenumber as nn

n = 1234.5
nn.to_human(n=n, precision=1, family='number')

>>> '1.2K'
```

- `to_numeric`
This function converts a human-readble value to a Python readable numeric value. Users need to use a specific human-readable string of numbers as input and choose the prefixes of filesize or numbers as optionals. The function will return a float.

```python
import nicenumber as nn

string = '4.51k'
nn.to_numeric(string=string, family='number')

>>> '4510.0'
```

- `to_pandas`
This function changes the formatting of text in one or more columns of data in a dataframe. The inputs should include a pandas data frame, column name(s), and two optionals: transform type(eg. human) and type of prefixes. The function will return a dataframe with the values from the input columns transferred to the transform type (human-readable by default).

```python
import nicenumber as nn

df = pd.DataFrame(np.array([[1_000, 1_000_000], [1_000_000_000, 1_000_000_000_000]]), columns=['A', 'B'])

nn.to_pandas(df, columns=['A'], transform_type='human')

>>>
|        |      A      |       B       |
|:------:|:-----------:|:-------------:|
|   0    |     1K      |    1000000    |
|   1    |     1B      | 1000000000000 |
```

- `to_color`
This function separate numeric values to parts starting from the right and each part contains three digits. Then it gives different colors to each part and the default colors are red, green, yellow, and blue. Users need to use a specific number as input and choose a list of colors they want to assign on the number as an optional. The function will return a string that can be used in `print()` function to visual numbers with colors.

```python
import nicenumber as nn

nn.to_color(1234567, ['green', 'red', 'blue'])
```
<span style="color: green;">1</span><span style="color: red;">234</span><span style="color: blue;">567</span>
## Python Ecosystem

There are several python packages that have similar functionalities with this package in the Python ecosystem. For example:
- [`numerize`](https://github.com/davidsa03/numerize) converts large numbers like 1234567.12 into 1.23M.
- [`millify`](https://github.com/azaitsev/millify) not only does the same thing as `numerize` but also adds separators to large number and plays around with filesize prefixes(kB, MB, GB).
- [`humanreadable`](https://github.com/thombashi/humanreadable) converts from human-readable values to Python values.
- [`humanfriendly`](https://humanfriendly.readthedocs.io/en/latest/#) formats numbers text interfaces more user friendly from different aspects such as transferring between units.
 
We aim to optimize those existing packages so that the users can use one package instead of using several packages at the same time.


## Dependencies

- TODO

## Usage

- TODO

## Documentation

The official documentation is hosted on Read the Docs: https://nicenumber.readthedocs.io/en/latest/

## Contributors

We welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/UBC-MDS/NiceNumber/blob/main/CONTRIBUTORS.md).

### Credits

This package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).
