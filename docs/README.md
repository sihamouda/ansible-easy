---
icon: rocket
---

# ansible-easy

`ansible-easy` is a YAML-driven Ansible workflow runner for teams that want a simple contract between:

- a template that defines allowed input
- a project input file that is validated with Pydantic
- one or more Ansible playbooks that receive mapped variables

It is designed for DevOps engineers who want to package repeatable automation behind a predictable configuration format instead of writing a custom Python wrapper for every workflow.

## What the project really does

At runtime, `ansible-easy`:

1. Loads a template YAML file.
2. Builds a Pydantic model from the template's `keys`.
3. Loads an input YAML file and validates it against that generated model.
4. Evaluates each playbook condition in order.
5. Runs matching playbooks with `ansible-runner`, passing mapped values as `--extra-vars`.

This makes the project useful for workflows such as:

- database provisioning
- backups and restores
- infrastructure bootstrap tasks
- platform-specific operational runbooks
- internal automation with a stable self-service config contract

## Interfaces

You can use the project in two ways:

- as a CLI with `ansible-easy run`
- as a Python library by importing the parser and playbook runner modules

{% hint style="info" %}
The Python interface is currently low-level by design. The most direct building blocks are `parse_config()` and `run_playbooks()`.
{% endhint %}

## Start here

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Installation</strong></td><td>Set up Python, Ansible, and package dependencies</td><td><a href="getting-started/installation.md">installation.md</a></td></tr><tr><td><strong>Quickstart</strong></td><td>Run your first template-driven workflow end to end</td><td><a href="getting-started/quickstart.md">quickstart.md</a></td></tr><tr><td><strong>CLI Usage</strong></td><td>Use `ansible-easy` from the terminal</td><td><a href="usage/cli.md">cli.md</a></td></tr><tr><td><strong>Python Usage</strong></td><td>Import the parser and runner into your own code</td><td><a href="usage/python.md">python.md</a></td></tr></tbody></table>

## Core ideas

- Templates define structure and execution rules.
- Input files provide concrete values for one workflow run.
- Playbook mapping translates validated config fields into Ansible variables.
- Conditions decide whether a playbook runs.
- Logs are emitted through Python logging and written both to console and a log file.
