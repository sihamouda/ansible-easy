---
icon: download
---

# Installation

## Requirements

- Python `3.12+`
- Ansible available in the execution environment
- access to any Ansible collections required by your playbooks

The package depends on:

- `ansible`
- `ansible-lint`
- `ansible-runner`
- `pydantic`
- `pydantic-settings`
- `pyyaml`
- `colorlog`

## Install from PyPI

```bash
pip install ansible-easy
```

## Install from source

From the repository root:

```bash
pip install .
```

If you prefer editable local development:

```bash
pip install -e .
```

## Verify the CLI

```bash
ansible-easy --help
```

Expected command shape:

```bash
ansible-easy run --template TEMPLATE --input INPUT --playbooks-dir PLAYBOOKS_DIR
```

## Install playbook-specific collections

`ansible-easy` does not vendor your workflow dependencies. If your playbooks require external collections, install them separately.

Example:

```bash
ansible-galaxy collection install community.postgresql
```

## Runtime logging environment variables

The package reads runtime settings through `pydantic-settings`. In practice, these environment variables are useful:

```bash
export LOG_FILE_PATH=/tmp
export LOG_FILE_NAME=ansible-easy.log
export LOG_LEVEL=INFO
```

Defaults:

- `LOG_FILE_PATH=/tmp`
- `LOG_FILE_NAME=ansible-easy.log`
- `LOG_LEVEL=INFO`

{% hint style="warning" %}
The log file handler is created when the package logger is imported. Make sure the configured log directory already exists and is writable by the current user.
{% endhint %}
