from typing import Optional

from invoke import task

from pydal2sql_core import core_create, core_alter

from pydal2sql_core.types import SUPPORTED_DATABASE_TYPES_WITH_ALIASES


# todo:
#  - other settings,
#  - edwh migration boilerplate around core output


@task(
    iterable=["tables"],
    help=dict(
        filename="Python file containing create_table statements. "
        "A specific git commit or branch can be added using @. "
        "Example: myfile@development. "
        "Additionally, @latest can be used for the last commit and @current can be used for the file as it currently is on disk. "
        "Instead of supplying a filename, - can be used to read from stdin.",
        magic="If --magic is passed, the program will try to fill in missing (irrelevant) variables to extract the define_tables statements.",
        db_type="SQL dialect to use. Supported are sqlite, postgres and mysql. For postgres, the psycopg2-binary package is required. For mysql, the pymysql package is required. Sqlite should work out of the box.",
        noop="Don't run any Python code but only show what the program would execute.",
        verbose="Print more information about what's going on.",
        function="If your define_table statements live in a function (not named `define_tables`), you can specify this so the program knows where to look. "
        "If more arguments are required, you can specify that: `--function my_table_definitions`, `--function my_table_definitions(db, 'other arg')` etc.",
    ),
)
def create(
    _,
    filename: str,
    magic: bool = False,
    tables: Optional[list[str]] = None,
    db_type: Optional[SUPPORTED_DATABASE_TYPES_WITH_ALIASES] = None,
    noop: bool = False,
    verbose: bool = False,
    function: Optional[str] = None,
):
    """
    Write CREATE TABLE statements for one or more tables in 'filename'.

    Usage:
    `edwh pydal2sql.create <filename>[@git-branch-or-commit-hash] [--options]`
    `ew pydal2sql.create - < myfile.py`
    """
    return core_create(
        filename, magic=magic, tables=tables, db_type=db_type, noop=noop, verbose=verbose, function=function
    )


@task(
    iterable=["tables"],
    help=dict(
        file_before="Python file containing create_table statements. "
        "A specific git commit or branch can be added using @. "
        "Example: myfile@development. "
        "Additionally, @latest can be used for the last commit and @current can be used for the file as it currently is on disk. "
        "Instead of supplying a filename, - can be used to read from stdin.",
        file_after="Same idea is file_before, but containing the desired state to migrate to (from the state in file_before). If you specify the same file as 'before' and 'after', the difference between the @latest commit and the @current version will be used.",
        magic="If --magic is passed, the program will try to fill in missing (irrelevant) variables to extract the define_tables statements.",
        db_type="SQL dialect to use. Supported are sqlite, postgres and mysql. For postgres, the psycopg2-binary package is required. For mysql, the pymysql package is required. Sqlite should work out of the box.",
        noop="Don't run any Python code but only show what the program would execute.",
        verbose="Print more information about what's going on.",
        function="If your define_table statements live in a function (not named `define_tables`), you can specify this so the program knows where to look. "
        "If more arguments are required, you can specify that: `--function my_table_definitions`, `--function my_table_definitions(db, 'other arg')` etc.",
    ),
)
def alter(
    _,
    file_before: str,
    file_after: str,
    magic: bool = False,
    tables: Optional[list[str]] = None,
    db_type: Optional[SUPPORTED_DATABASE_TYPES_WITH_ALIASES] = None,
    noop: bool = False,
    verbose: bool = False,
    function: Optional[str] = None,
):
    """
    Write migration logic (CREATE TABLE, ALTER TABLE) from the state is it is in file_before to the state as it is in file_after.

    'file before' and 'file after' can also be the same file at different points in time using git.
    Example: `ew pydal2sql.alter models.py@latest models.py@current`: this shows the difference between the latest git commit and the current file on disk.
    @<some-git-branch> or @<specific-git-commit-hash> is also supported.

    Using '-' instead of a filename allows you to read from stdin:
    `ew pydal2sql.alter - models.py` < old_file.py`
    """

    return core_alter(
        file_before,
        file_after,
        magic=magic,
        tables=tables,
        db_type=db_type,
        noop=noop,
        verbose=verbose,
        function=function,
    )
