from pathlib import Path

from govtext_client.common.constants import Environment

########################
# System
########################

AUTH_STAGING_URL: str = "https://stg.govtext.gov.sg/auth-api"
AUTH_PRODUCTION_URL: str = "https://govtext.gov.sg/auth-api"
AUTH_API_VERSION: str = "/v1"

CORE_STAGING_URL: str = "https://stg.govtext.gov.sg/core-api"
CORE_PRODUCTION_URL: str = "https://govtext.gov.sg/core-api"
CORE_API_VERSION: str = "/v1"

########################
# CLI
########################

CREDENTIALS_FILEPATH: str = str(
    Path.home().joinpath(".text").joinpath("credentials.yml")
)
CONFIGURATIONS_FILEPATH: str = str(
    Path.home().joinpath(".text").joinpath("configurations.yml")
)
CONTEXT_SETTINGS: dict = {"help_option_names": ["-h", "--help"]}

DEFAULT_CONFIGURATIONS_DATA: dict = {
    "environment": Environment.PRODUCTION.value,
    "auth_server_url": None,
    "core_server_url": None,
    "auth_api_version": AUTH_API_VERSION,
    "core_api_version": CORE_API_VERSION,
}
