import ansible_runner


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
        vars[entry["ansible_variable_name"]] = _resolve_field(
            config, entry["config_variable_name"]
        )
    return vars


def _run_ansible(playbook_name: str, vars: dict, playbooks_dir: str):
    result = ansible_runner.run(
        project_dir=playbooks_dir,
        playbook=f"{playbook_name}.yaml",
        extravars=vars,
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
            playbook_dir=playbooks_dir,
        )
