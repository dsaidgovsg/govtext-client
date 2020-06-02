from enum import Enum


class ContentType(Enum):
    MULTIPART_FORM = "multipart/form-data"
    JSON = "application/json"


class Environment(Enum):
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"


class ServerType(Enum):
    AUTH = "AUTH"
    CORE = "CORE"
