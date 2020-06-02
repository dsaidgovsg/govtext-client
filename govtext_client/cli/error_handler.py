import sys
import traceback

import click
from wasabi import TracebackPrinter, msg

from govtext_client.common.exceptions import ClientError
from govtext_client.helper import newline


class ErrorHandlerGroup(click.Group):
    def __call__(self, *args, **kwargs):
        tbp = TracebackPrinter(
            tb_base="govtext-client", tb_range_start=-10, tb_range_end=None
        )
        try:
            return self.main(*args, **kwargs)
        except ClientError as ce:
            error = tbp(
                type(ce).__name__, ce.message, tb=traceback.extract_tb(ce.__traceback__)
            )
            msg.fail("Unexpected error while making HTTP request.")
            newline()
            click.echo(error)
            sys.exit(1)
        except Exception as e:
            error = tbp(type.__name__, tb=traceback.extract_tb(e.__traceback__))
            click.echo(error)
            sys.exit(1)
