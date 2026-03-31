# ansible-easy

A YAML-driven Ansible playbook runner. Define your infrastructure configuration schema and playbook execution logic in YAML — no Python required.

ansible-easy is generic and can be used for any automation workflow. You define the schema, the conditions, and the playbook mappings — ansible-easy handles validation and execution.

## Installation
```bash
pip install ansible-easy
```

## How it works

ansible-easy has three concepts:

- **Template** — defines the schema of your config (field names, types, required/optional) and which playbooks to run and under what conditions
- **Input** — the actual values for a specific project, validated against the template
- **Playbooks** — standard Ansible playbooks that receive variables from the input via the mapping defined in the template

## Usage
```bash
ansible-easy run \
  --template ./config-templates/my-template.yaml \
  --input ./workflow-input/my-input.yaml \
  --playbooks-dir ./playbooks
```

## Template config

Templates define the schema and playbook execution logic:
```yaml
name: my_workflow
keys:
  - name: environment
    type: enum
    possible_values:
      - staging
      - production
    required: true
  - name: app_role
    type: str
    required: false
  - name: connection
    type: object
    required: true
    keys:
      - name: host
        type: str
        required: true
      - name: port
        type: int
        required: true

playbooks:
  - name: setup
    condition:
      type: always
    mapping:
      - ansible_variable_name: HOST
        config_variable_name: connection.host

  - name: configure_app_role
    condition:
      type: field_present
      field: app_role
    mapping:
      - ansible_variable_name: APP_ROLE
        config_variable_name: app_role
```

### Supported field types

| Type     | Description                       | Extra keys               |
|----------|-----------------------------------|--------------------------|
| `str`    | String                            | —                        |
| `int`    | Integer                           | —                        |
| `enum`   | One of a fixed set of values      | `possible_values: [...]` |
| `list`   | List of strings                   | `elements_type: str`     |
| `object` | Nested object with its own `keys` | `keys: [...]`            |

### Condition types

| Type            | Description                                      |
|-----------------|--------------------------------------------------|
| `always`        | Playbook always runs                             |
| `field_present` | Runs only if the specified field has a value     |
| `field_absent`  | Runs only if the specified field is not provided |

### Variable mapping

The `mapping` block maps your config fields to Ansible `--extra-vars`. Dot notation is supported for nested fields:
```yaml
- ansible_variable_name: HOST
  config_variable_name: connection.host
```

## Logging

ansible-easy routes all Ansible output through Python's standard `logging` module:
```
2026-03-31 10:38:10 [INFO] [setup] [Create resource] ok (no change)
2026-03-31 10:38:12 [INFO] [setup] [Configure resource] changed
2026-03-31 10:38:14 [INFO] [setup] finished
```

## Requirements

- Python 3.12+
- `ansible-runner`
- `pydantic`
- `pyyaml`