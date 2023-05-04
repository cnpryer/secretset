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
secretset df1.xlsx df2.xlsx --col a
```
NOTE: Currently aligned fields must have the same field name.
"""
from __future__ import annotations

from pathlib import Path

import click

from secretset.anon import anonymize_dataframes
from secretset.io import read_file, write_file


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
    "--col",
    default=[],
    multiple=True,
    help="Column to anonymize.",
)
@click.option("--output", default=[], multiple=True, help="output file path")
@click.option("--format", default=[], multiple=True, help="output format")
@click.argument("args", nargs=-1)
def main(args: str, **kwargs) -> None:
    if not args:
        return

    cols = tuple(col for col in kwargs["col"])
    files = tuple(Path(f) for f in args)
    dfs = list(read_file(f) for f in files)

    fmts = tuple(f for f in kwargs["format"])
    if not fmts:
        fmts = tuple("csv" for _ in files)
    elif len(fmts) == 1:
        fmts = tuple(fmts[0].lstrip(".").lower() for _ in files)
    else:
        fmts = tuple(f.lstrip(".").lower() for f in fmts)

    outs = tuple(Path(f) for f in kwargs["output"])
    if not outs:
        outs = tuple(
            Path(".") / f"{f.stem}.{fmt.lstrip('.')}"
            for (f, fmt) in zip(files, fmts)
        )

    if not cols:
        cols = tuple(col for col in dfs[0].columns)
        for df in dfs[1:]:
            cols += tuple(col for col in df.columns)

    dfs = anonymize_dataframes(dfs, cols)

    for df, p, f in zip(dfs, outs, fmts):
        write_file(df, p, format=f)
