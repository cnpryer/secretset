"""Anonymize data from files.
For files that contain data that should overlap (could be joined), run
anonymizing functions to map original data to the same set of new data.
Example:
You might have two datasets with a common field `a` that can be used to join
the files together with.
>> df1
a   b   c
9   2   3
9   3   5
10  2   3
10  3   5
>> df2
a   d   e
9   10  13
10  10  13
If you anonymize data from `df1` you'd want `a` to be mapped to the same
anonymous data as `df2`.`a`.
To do this, run the script pointing at the two files and add a flag for each
common field.
```
secretset df1.xlsx df2.xlsx --align=a
```
NOTE: Currently aligned fields must have the same field name.
"""
from collections import defaultdict
from pathlib import Path

import click
import pandas as pd  # type: ignore

from secretset.map import map_sequence


class DefaultCommandGroup(click.Group):
    """allow a default command for a group"""

    def command(self, *args, **kwargs):
        default_command = kwargs.pop("default_command", False)

        if default_command and not args:
            kwargs["name"] = kwargs.get("name", "<>")

        decorator = super(DefaultCommandGroup, self).command(*args, **kwargs)

        if default_command:

            def new_decorator(f):
                cmd = decorator(f)
                self.default_command = cmd.name
                return cmd

            return new_decorator

        return decorator

    def resolve_command(self, ctx, args):
        try:
            # test if the command parses
            return super(DefaultCommandGroup, self).resolve_command(ctx, args)
        except click.UsageError:
            # command did not parse, assume it is the default command
            args.insert(0, self.default_command)
            return super(DefaultCommandGroup, self).resolve_command(ctx, args)


@click.group(cls=DefaultCommandGroup, invoke_without_command=True)
@click.pass_context
def main(ctx) -> None:
    """Invoked entrypoint to script."""


def read_file(filename: str) -> pd.DataFrame:
    """Read file from current directory using filename.
    Args:
        filename (str): Filename. Only reads xlsx, xls, and csv.
    Returns:
        pd.DataFrame: Pandas DataFrame
    """
    if filename.lower().endswith(".xls") or filename.lower().endswith(".xlsx"):
        return pd.read_excel(filename)

    if filename.lower().endswith(".csv"):
        return pd.read_csv(filename)

    raise Exception("File must be .xls, .xlsx, .csv.")


@main.command(default_command=True)  # type: ignore
@click.option(
    "--target",
    default=[],
    multiple=True,
    help="Field to anonymize.",
)
@click.option(
    "--align",
    default=[],
    multiple=True,
    help="Common field to anonymize across files.",
)
@click.argument("args", nargs=-1)
def main(args: str, **kwargs) -> None:
    dfs = [read_file(filename=_) for _ in args]

    # initialize each field marked to align across files
    aligned_data_inputs = defaultdict(set)
    for field in kwargs["align"]:
        for df in dfs:
            aligned_data_inputs[field].update(df[field].unique().tolist())

    # anonymize regular targets for each dataframe
    for field in [_ for _ in kwargs["target"] if _ not in kwargs["align"]]:
        for df in dfs:
            if field not in df.columns:
                continue
            inputs = df[field].unique().tolist()
            df[field] = df[field].replace(map_sequence(inputs))

    # anonymize fields to align
    for field in aligned_data_inputs:
        for df in dfs:
            inputs = aligned_data_inputs[field]
            df[field] = df[field].replace(map_sequence(inputs))

    for filename, df in zip(args, dfs):
        df.to_excel(f"{Path(filename).stem}_anon.xlsx", index=False)


if __name__ == "__main__":
    main()
