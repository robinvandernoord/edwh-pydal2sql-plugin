from invoke import task

from pydal2sql_core.cli_support import core_create, core_alter

# todo:
#  - other settings,
#  - edwh migration boilerplate around core output

@task()
def create(_, filename: str, magic: bool = False):
    return core_create(filename, magic=magic)


@task
def alter(_, file_before: str, file_after: str, magic: bool = False):
    return core_alter(file_before, file_after, magic=magic)
