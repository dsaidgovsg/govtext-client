from govtext_client.common.configurations import (
    AUTH_PRODUCTION_URL,
    AUTH_STAGING_URL,
    CORE_PRODUCTION_URL,
    CORE_STAGING_URL,
)
from govtext_client.common.constants import Environment, ServerType


class Settings:
    ENVIRONMENT: dict = {
        Environment.STAGING: {
            ServerType.AUTH: {"url": AUTH_STAGING_URL},
            ServerType.CORE: {"url": CORE_STAGING_URL},
        },
        Environment.PRODUCTION: {
            ServerType.AUTH: {"url": AUTH_PRODUCTION_URL},
            ServerType.CORE: {"url": CORE_PRODUCTION_URL},
        },
    }
