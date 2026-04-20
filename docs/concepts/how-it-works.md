---
icon: gears
---

# How It Works

`ansible-easy` connects a validated config model to a sequence of Ansible playbooks.

## Execution pipeline

### 1. Template parsing

The template YAML defines:

- the workflow `name`
- the allowed configuration `keys`
- the `playbooks` to run

From that file, `ansible-easy` generates a Pydantic model dynamically at runtime.

### 2. Input validation

The input YAML is loaded and validated against the generated model.

This gives you:

- strict type checking for supported fields
- nested object validation
- enum validation for constrained values

### 3. Condition evaluation

Each playbook has a `condition` block. Supported condition types are:

- `always`
- `field_present`
- `field_absent`

If the condition evaluates to `true`, the playbook is executed.

### 4. Variable mapping

Each playbook declares a `mapping` list that translates validated config values into Ansible variable names.

Example:

```yaml
mapping:
  - ansible_variable_name: HOST
    config_variable_name: connection.host
```

This produces an Ansible extra-var equivalent to:

```text
HOST=<resolved value from connection.host>
```

### 5. Playbook execution

The runner executes:

```text
<playbooks_dir>/<playbook_name>.yaml
```

through `ansible-runner`, one playbook at a time, in declaration order.

## Logging model

Ansible events are translated into standard Python log records. Output is sent to:

- the console
- a log file configured through environment variables

Typical event flow:

- playbook start
- task result events
- playbook finish

## What ansible-easy does not do

`ansible-easy` does not:

- generate your Ansible playbooks for you
- manage inventory design for your workflows
- install collections automatically
- provide a stable high-level SDK beyond the current parser and runner modules
