from typing import Optional

import click
from wasabi import msg, table

from govtext_client.cli.error_handler import ErrorHandlerGroup
from govtext_client.common.configurations import (
    CONFIGURATIONS_FILEPATH,
    CONTEXT_SETTINGS,
    DEFAULT_CONFIGURATIONS_DATA,
)
from govtext_client.helper import write_yaml_file


@click.group(cls=ErrorHandlerGroup, context_settings=CONTEXT_SETTINGS)
@click.pass_obj
def config(obj: dict):
    pass


@config.command(help="List current configurations.")
@click.pass_obj
def list(obj: dict):
    configurations = obj["configurations"]
    msg.info("Listing configs...")
    t = table(configurations, header=["Key", "Value"], divider=True)
    click.echo(t)


@config.command(help="Set configurations.")
@click.option("--default", is_flag=True)
@click.option(
    "--env",
    type=click.Choice(["STAGING", "PRODUCTION"], case_sensitive=False),
    help="Changes subdomains of API endpoints based on the environment set.",
)
@click.option(
    "--asu", type=str, help="Auth server URL. Overrides URL set by environment."
)
@click.option(
    "--csu", type=str, help="Core server URL. Overrides URL set by environment."
)
@click.option(
    "--av",
    type=click.Choice(["/v1"], case_sensitive=False),
    help="Auth server API version.",
)
@click.option(
    "--cv",
    type=click.Choice(["/v1"], case_sensitive=False),
    help="Core server API version.",
)
@click.pass_obj
def set(
    obj: dict,
    default: bool,
    env: Optional[str],
    asu: Optional[str],
    csu: Optional[str],
    av: Optional[str],
    cv: Optional[str],
):
    configurations = obj["configurations"]
    if default:
        configurations = DEFAULT_CONFIGURATIONS_DATA

    configurations["environment"] = env if env else configurations["environment"]
    configurations["auth_server_url"] = (
        asu if asu else configurations["auth_server_url"]
    )
    configurations["core_server_url"] = (
        csu if csu else configurations["core_server_url"]
    )
    configurations["auth_api_version"] = (
        av if av else configurations["auth_api_version"]
    )
    configurations["core_api_version"] = (
        cv if cv else configurations["core_api_version"]
    )

    msg.info("Saving configs...")
    write_yaml_file(CONFIGURATIONS_FILEPATH, configurations)
    msg.good("Configs saved to {}.".format(CONFIGURATIONS_FILEPATH))
