---
icon: terminal
---

# CLI Usage

The CLI currently exposes a single workflow command:

```bash
ansible-easy run \
  --template ./path/to/template.yaml \
  --input ./path/to/input.yaml \
  --playbooks-dir ./path/to/playbooks
```

## Arguments

| Argument | Required | Description |
| --- | --- | --- |
| `--template` | Yes | Path to the YAML template definition |
| `--input` | Yes | Path to the YAML input payload |
| `--playbooks-dir` | Yes | Directory that contains `<playbook-name>.yaml` files |

## How the CLI maps to execution

When you run the command, `ansible-easy`:

1. loads the template YAML
2. creates a Pydantic model dynamically
3. loads the input YAML
4. validates the input
5. evaluates playbook conditions in the order they are declared
6. runs matching playbooks through `ansible-runner`

## Example

```bash
ansible-easy run \
  --template ./config-templates/database-project.template.yaml \
  --input ./workflow-input/my-project.yaml \
  --playbooks-dir ./playbooks
```

## Recommended project layout

```text
my-workflow/
├── config-templates/
│   └── database-project.template.yaml
├── workflow-input/
│   └── my-project.yaml
└── playbooks/
    ├── create_login_role.yaml
    ├── create_nologin_role.yaml
    └── setup_database.yaml
```

## Exit behavior

- Invalid template structure raises a parser exception before any playbook runs.
- Invalid input data fails during Pydantic validation before any playbook runs.
- If a playbook fails, execution stops and the runner raises an exception.

## Important execution details

- Playbooks are run sequentially in the order declared in `playbooks:`.
- The playbook file name is always `<name>.yaml`.
- `mapping.config_variable_name` supports dot notation such as `connection.host`.
- `condition.field` is evaluated as a top-level key only.
- If `dir_path: true` is set on a mapped string, the value is resolved relative to the current working directory of the process.

{% hint style="warning" %}
Because `dir_path` is resolved with `os.getcwd()`, it is not based on the location of the template file or input file. Run the CLI from a directory where relative paths make sense for your workflow.
{% endhint %}
