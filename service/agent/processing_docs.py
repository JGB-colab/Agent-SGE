import yaml
from pathlib import Path

ROOT_PROJECT = Path(__file__).resolve().parent


def read_yaml(path: str =  ROOT_PROJECT / "config.yaml") -> yaml:
    with open(path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return data