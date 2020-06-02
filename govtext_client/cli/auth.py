import click
from wasabi import msg, table

from govtext_client.cli.error_handler import ErrorHandlerGroup
from govtext_client.client import Client
from govtext_client.common.configurations import CONTEXT_SETTINGS, CREDENTIALS_FILEPATH
from govtext_client.helper import (
    create_file,
    file_exists,
    is_successful_status,
    newline,
    read_yaml_file,
)


@click.group(cls=ErrorHandlerGroup, context_settings=CONTEXT_SETTINGS)
@click.pass_obj
def auth(obj: dict):
    if not file_exists(CREDENTIALS_FILEPATH):
        msg.info("No credentials file detected. Creating one...")

        try:
            create_file(CREDENTIALS_FILEPATH)
            msg.good("Credentials file created at {}".format(CREDENTIALS_FILEPATH))
            newline()
        except Exception as e:
            msg.fail("Failed to create file at {}".format(CREDENTIALS_FILEPATH))
            raise e

    msg.info("Reading credentials...")
    credentials = read_yaml_file(CREDENTIALS_FILEPATH)
    msg.good("Credentials read from {}".format(CREDENTIALS_FILEPATH))
    newline()

    obj["credentials"] = credentials


@auth.command(help="Registers a new account with GovText.")
@click.option(
    "--email", prompt=True, help="The email used for logging into your GovText account."
)
@click.option(
    "--password",
    prompt=True,
    confirmation_prompt=True,
    hide_input=True,
    help="The string of characters used to gain access to your GovText account.",
)
@click.option("--display-name", prompt=True, help="The name to be addressed you by.")
@click.pass_obj
def signup(obj: dict, email: str, password: str, display_name: str):
    configurations = obj["configurations"]
    client = Client(**configurations)

    msg.info("Signing up...")
    (data, status_code) = client.signup(
        email=email, password=password, display_name=display_name
    )

    if is_successful_status(status_code):
        msg.good(
            "Signup successful! Please check your email to complete the signup process."
        )
        newline()
        t = table(data, header=["Key", "Value"], divider=True)
        click.echo(t)
    else:
        msg.fail("Signup unsuccessful!")
        newline()
        t = table(data, header=["Key", "Value"], divider=True)
        click.echo(t)
