from pathlib import Path

import yaml
from wasabi import msg


def is_successful_status(status_code: int) -> bool:
    return 200 <= status_code < 300


def is_redirect_status(status_code: int) -> bool:
    return 300 <= status_code < 400


def is_client_error_status(status_code: int) -> bool:
    return 400 <= status_code < 500


def is_server_error_status(status_code: int) -> bool:
    return 500 <= status_code < 600


def file_exists(filepath: str) -> bool:
    return Path(filepath).is_file()


def create_file(filepath: str):
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    if not file_exists(filepath):
        Path(filepath).touch()


def read_yaml_file(filepath: str) -> dict:
    with open(filepath) as f:
        data = yaml.safe_load(f) or {}
        return data


def write_yaml_file(filepath: str, data: dict):
    with open(filepath, "w") as f:
        yaml.safe_dump(data, f)


def newline():
    msg.text()
