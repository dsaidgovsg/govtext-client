import click
from wasabi import msg

from govtext_client.cli.auth import auth
from govtext_client.cli.config import config
from govtext_client.cli.error_handler import ErrorHandlerGroup
from govtext_client.common.configurations import (
    CONFIGURATIONS_FILEPATH,
    CONTEXT_SETTINGS,
    DEFAULT_CONFIGURATIONS_DATA,
)
from govtext_client.helper import (
    create_file,
    file_exists,
    newline,
    read_yaml_file,
    write_yaml_file,
)


@click.group(cls=ErrorHandlerGroup, context_settings=CONTEXT_SETTINGS)
@click.pass_context
def govtext(ctx: click.Context):
    if not file_exists(CONFIGURATIONS_FILEPATH):
        msg.info("No configs file detected. Creating one...")

        try:
            create_file(CONFIGURATIONS_FILEPATH)
            write_yaml_file(CONFIGURATIONS_FILEPATH, DEFAULT_CONFIGURATIONS_DATA)
            msg.good("Configs file created at {}".format(CONFIGURATIONS_FILEPATH))
            newline()
        except Exception as e:
            msg.fail("Failed to create file at {}".format(CONFIGURATIONS_FILEPATH))
            raise e

    msg.info("Reading configs...")
    configurations = read_yaml_file(CONFIGURATIONS_FILEPATH)
    msg.good("Configs read from {}".format(CONFIGURATIONS_FILEPATH))
    newline()

    ctx.obj = {"configurations": configurations}


govtext.add_command(config)
govtext.add_command(auth)
