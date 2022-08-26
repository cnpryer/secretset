# secretset

Command line program to anonymize data.

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

```console
$ secretset file.xlsx --target col1
```

### Anonymize multiple files

You can anonymize multiple related files using:

```console
$ secretset file1.xlsx file2.csv --related \
    --align col1 \
    --target col2 \
    --target col3
```
