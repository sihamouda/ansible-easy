from pydantic import create_model, Field
from typing import Literal
import yaml


class ParseStructureException(Exception):
    def __init__(self, reason: str):
        self.message = f"Failed to parse YAML: {reason}"
        super().__init__(self.message)


def _check_name(data: dict):
    if data.get("name") in ["", None]:
        raise ParseStructureException("the key 'name' is missing")


def _check_keys(data: dict):
    if data.get("keys") in ["", None]:
        raise ParseStructureException("the key 'keys' is missing")
    if type(data["keys"]) is not list:
        raise ParseStructureException("the key 'keys' should be a list")


def _check_type(data: dict):
    if data.get("type") in ["", None]:
        raise ParseStructureException("the key 'type' is missing")


def _check_required(data: dict):
    if data.get("required") in ["", None]:
        raise ParseStructureException("the key 'required' is missing")
    if type(data["required"]) is not bool:
        raise ParseStructureException("the key 'required' should be bool")


def _check_possible_values(data: dict):
    if data.get("possible_values") in ["", None]:
        raise ParseStructureException("the key 'possible_values' is missing")
    if type(data["possible_values"]) is not list:
        raise ParseStructureException("the key 'possible_values' should be list")


def _check_list_field(data: dict):
    if data.get("elements_type") in ["", None]:
        raise ParseStructureException("the key 'elements_type' is missing")


def _return_str_field(data: dict):
    if data["required"]:
        return {data["name"]: (str, Field(strict=True))}
    else:
        return {data["name"]: (str | None, Field(default=None, strict=True))}


def _return_int_field(data: dict):
    if data["required"]:
        return {data["name"]: (int, Field(strict=True))}
    else:
        return {data["name"]: (int | None, Field(default=None, strict=True))}


def _parse_key(data: dict):
    _check_name(data)
    _check_type(data)
    _check_required(data)

    match data["type"]:
        case "str":
            return _return_str_field(data)
        case "int":
            return _return_int_field(data)
        case "enum":
            _check_possible_values(data)
            return {data["name"]: (Literal[*data["possible_values"]])}
        case "list":
            _check_list_field(data)
            match data["elements_type"]:
                case "str":
                    return {data["name"]: (list[str], Field(strict=data["required"]))}
                case _:
                    raise ParseStructureException("Only supported type of list is str")
        case "object":
            return {
                data["name"]: (_parse_structure(data), Field(strict=data["required"]))
            }


def _parse_structure(data: dict):
    _check_name(data)
    _check_keys(data)

    fields = {}
    for key in data["keys"]:
        fields.update(_parse_key(key))

    return create_model(data["name"], **fields)


def _check_playbook_name(playbook: dict):
    if playbook.get("name") in ["", None]:
        raise ParseStructureException("a playbook is missing its 'name'")


def _check_playbook_condition(playbook: dict):
    condition = playbook.get("condition")
    if condition in ["", None]:
        raise ParseStructureException(
            f"playbook '{playbook['name']}' is missing 'condition'"
        )

    condition_type = condition.get("type")
    if condition_type not in ["always", "field_present", "field_absent"]:
        raise ParseStructureException(
            f"playbook '{playbook['name']}' has unknown condition type '{condition_type}'"
        )
    if condition_type in ["field_present", "field_absent"] and condition.get(
        "field"
    ) in ["", None]:
        raise ParseStructureException(
            f"playbook '{playbook['name']}' condition '{condition_type}' requires a 'field'"
        )


def _check_playbook_mapping(playbook: dict):
    mapping = playbook.get("mapping")
    if mapping in ["", None]:
        raise ParseStructureException(
            f"playbook '{playbook['name']}' is missing 'mapping'"
        )
    if type(mapping) is not list:
        raise ParseStructureException(
            f"playbook '{playbook['name']}' 'mapping' should be a list"
        )
    for entry in mapping:
        if entry.get("ansible_variable_name") in ["", None]:
            raise ParseStructureException(
                f"playbook '{playbook['name']}' mapping entry is missing 'ansible_variable_name'"
            )
        if entry.get("config_variable_name") in ["", None]:
            raise ParseStructureException(
                f"playbook '{playbook['name']}' mapping entry is missing 'config_variable_name'"
            )
        if "dir_path" in entry and type(entry["dir_path"]) is not bool:
            raise ParseStructureException(
                f"playbook '{playbook['name']}' mapping entry 'dir_path' should be bool"
            )


def _parse_playbook(playbook: dict) -> dict:
    _check_playbook_name(playbook)
    _check_playbook_condition(playbook)
    _check_playbook_mapping(playbook)

    return {
        "name": playbook["name"],
        "condition": playbook["condition"],
        "mapping": [
            {
                "ansible_variable_name": entry["ansible_variable_name"],
                "config_variable_name": entry["config_variable_name"],
                "dir_path": entry.get("dir_path", False),
            }
            for entry in playbook["mapping"]
        ],
    }


def _parse_playbooks(data: dict) -> list[dict]:
    playbooks = data.get("playbooks")
    if playbooks in ["", None]:
        raise ParseStructureException("the key 'playbooks' is missing")
    if type(playbooks) is not list:
        raise ParseStructureException("the key 'playbooks' should be a list")

    return [_parse_playbook(pb) for pb in playbooks]


def parse_config(config_path: str):
    with open(config_path, "r") as file:
        config_data = yaml.safe_load(file)

    PydanticModel = _parse_structure(config_data)
    playbooks_definition = _parse_playbooks(config_data)

    return PydanticModel, playbooks_definition
