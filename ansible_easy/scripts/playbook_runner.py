import os
import ansible_runner
from ansible_easy.scripts.log import logger


def _resolve_field(config: dict, config_variable_name: str):
    """Supports dot notation like connection.host"""
    parts = config_variable_name.split(".")
    value = config
    for part in parts:
        value = value[part]
    return value


def _evaluate_condition(config: dict, condition: dict) -> bool:
    match condition["type"]:
        case "always":
            return True
        case "field_present":
            return config.get(condition["field"]) not in ["", None]
        case "field_absent":
            return config.get(condition["field"]) in ["", None]


def _build_ansible_vars(config: dict, mapping: list[dict]) -> dict:
    vars = {}
    for entry in mapping:
        value = _resolve_field(config, entry["config_variable_name"])
        if entry.get("dir_path") and isinstance(value, str):
            value = f"{os.getcwd()}/{value}"
        vars[entry["ansible_variable_name"]] = value
    return vars


def _run_ansible(playbook_name: str, vars: dict, playbooks_dir: str):

    def _handle_ansible_event(event: dict):
        event_type = event.get("event", "")
        stdout = event.get("stdout", "").strip()
        task_name = event.get("event_data", {}).get("task", "")

        if not stdout:
            return

        prefix = (
            f"[{playbook_name}] [{task_name}]" if task_name else f"[{playbook_name}]"
        )

        match event_type:
            case "runner_on_ok":
                changed = (
                    event.get("event_data", {}).get("res", {}).get("changed", False)
                )
                if changed:
                    logger.info(f"{prefix} changed")
                else:
                    logger.info(f"{prefix} ok (no change)")
            case "runner_on_failed":
                logger.error(f"{prefix} failed — {stdout}")
            case "runner_on_skipped":
                logger.debug(f"{prefix} skipped")
            case "runner_on_unreachable":
                logger.error(f"{prefix} unreachable — {stdout}")
            case "playbook_on_start":
                logger.info(f"[{playbook_name}] started")
            case "playbook_on_stats":
                logger.info(f"[{playbook_name}] finished")
            case _:
                logger.debug(f"{prefix} {stdout}")

    result = ansible_runner.run(
        project_dir=playbooks_dir,
        playbook=f"{playbook_name}.yaml",
        extravars=vars,
        quiet=True,
        event_handler=_handle_ansible_event,
    )

    if result.status == "failed":
        raise Exception(f"Playbook '{playbook_name}' failed: {result.stats}")

    return result


def run_playbooks(config: dict, playbooks_definition: list[dict], playbooks_dir: str):
    for playbook in playbooks_definition:
        if not _evaluate_condition(config, playbook["condition"]):
            continue

        ansible_vars = _build_ansible_vars(config, playbook["mapping"])
        _run_ansible(
            playbook_name=playbook["name"],
            vars=ansible_vars,
            playbooks_dir=playbooks_dir,
        )
