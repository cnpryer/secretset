[![ci](https://github.com/cnpryer/secretset/workflows/ci/badge.svg)](https://github.com/cnpryer/secretset/actions)
[![PyPI Latest Release](https://img.shields.io/pypi/v/secretset.svg)](https://pypi.org/project/secretset/)

# secretset

Command line interface to anonymize data.

## Installation

```console
$ pip install secretset
```

## Usage

For information on commands available run `secretset --help`.

### Compatible sources

- Excel
- CSV

### Anonymize files

You can anonymize files using:

```
$ secretset file.xlsx --target col1
```

### Anonymize multiple files

You can anonymize multiple related files using:

```
$ secretset file1.xlsx file2.csv \
    --align col1 \
    --target col2 \
    --target col3
```
