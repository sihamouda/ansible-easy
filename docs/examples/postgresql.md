---
icon: database
---

# PostgreSQL Workflow

The repository includes a PostgreSQL-focused example under `examples/postgresql/README.md`.

This example shows how `ansible-easy` can be used for:

- database provisioning
- role creation
- grants
- backups
- restores

## Prerequisites

Install the package and the PostgreSQL Ansible collection dependencies:

```bash
pip install ansible-easy
pip install psycopg2-binary
ansible-galaxy collection install community.postgresql
```

## Workflow variants

The example describes three template-driven workflows:

| Template | Purpose |
| --- | --- |
| `database-project.template.yaml` | create roles, database, schema, and grants |
| `database-backup.template.yaml` | create a plain SQL backup |
| `database-restore.template.yaml` | restore a dump and optionally re-grant roles |

## Provision a database

```bash
ansible-easy run \
  --template ./config-templates/database-project.template.yaml \
  --input ./workflow-input/my-project.yaml \
  --playbooks-dir ./playbooks
```

## Backup a database

```bash
ansible-easy run \
  --template ./config-templates/database-backup.template.yaml \
  --input ./workflow-input/my-backup.yaml \
  --playbooks-dir ./playbooks
```

## Restore a database

```bash
ansible-easy run \
  --template ./config-templates/database-restore.template.yaml \
  --input ./workflow-input/my-restore.yaml \
  --playbooks-dir ./playbooks
```

## Why this example matters

It demonstrates the intended project model well:

- keep business-specific logic in playbooks
- keep allowed inputs in a template
- let `ansible-easy` validate and route variables between the two
