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
from __future__ import annotations

from pathlib import Path

import click

from secretset.anon import anonymize_df
from secretset.collect import collect_df_data
from secretset.io import read_file
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

    # read all of the data from the collumns targeted or aligned
    # between each file.
    # TODO: this is an optimization of a bunch of older code.
    #       i'll simplify command arguments/flags later.
    cols = [col for col in kwargs["target"] + kwargs["align"]]

    # all unique data from the selected fields
    data = set()

    # collect unique data from a df into a set
    for df in dfs:
        data.update(collect_df_data(df, data, cols))

    # create a dataframe mapping dictionary out of a set of uniques
    mapping = map_sequence(data)

    # update each field selected with anonymous data using the mapping
    for i in range(len(dfs)):
        dfs[i] = anonymize_df(df, mapping, cols)

    for filename, df in zip(args, dfs):
        df.to_excel(f"{Path(filename).stem}_anon.xlsx", index=False)


if __name__ == "__main__":
    main()
