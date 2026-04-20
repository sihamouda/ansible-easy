---
icon: file-code
---

# Template Format

A template file combines schema definition and execution metadata in one YAML document.

## Top-level shape

```yaml
name: my_workflow
keys:
  - name: environment
    type: str
    required: true

playbooks:
  - name: setup
    condition:
      type: always
    mapping:
      - ansible_variable_name: ENVIRONMENT
        config_variable_name: environment
```

## `name`

`name` is required and identifies the generated model.

## `keys`

`keys` is required and must be a list. Each item defines one input field.

Supported field types:

- `str`
- `int`
- `enum`
- `list`
- `object`

## `playbooks`

`playbooks` is required and must be a list.

Each playbook entry must define:

- `name`
- `condition`
- `mapping`

## Nested fields

Nested input is supported through `object` fields:

```yaml
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
```

You can then map nested values with dot notation:

```yaml
config_variable_name: connection.host
```

## Conditions

### `always`

Runs the playbook every time.

```yaml
condition:
  type: always
```

### `field_present`

Runs only when the referenced top-level field is not empty and not `null`.

```yaml
condition:
  type: field_present
  field: app_role
```

### `field_absent`

Runs only when the referenced top-level field is empty or not provided.

```yaml
condition:
  type: field_absent
  field: app_role
```

{% hint style="warning" %}
Condition fields are currently checked with top-level lookup only. Dot notation is supported in `mapping.config_variable_name`, but not in `condition.field`.
{% endhint %}

## `dir_path`

Each mapping entry can optionally set `dir_path: true`:

```yaml
- ansible_variable_name: INPUT_PATH
  config_variable_name: input_path
  dir_path: true
```

When enabled on a string field, the runner prefixes the value with the current working directory.
