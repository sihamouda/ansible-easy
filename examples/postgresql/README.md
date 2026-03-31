# Example: PostgreSQL database provisioning

This example shows how to use ansible-easy to provision a PostgreSQL database, including roles, schema, privileges, backup, and restore. It is one specific use case — ansible-easy itself is not tied to PostgreSQL or databases in any way.

## Prerequisites

### Python dependencies
```bash
pip install ansible-easy
pip install psycopg2-binary   # PostgreSQL driver required by the Ansible collection
```

### Ansible collection
```bash
ansible-galaxy collection install community.postgresql
```

## What this example does

Three templates are provided:

| Template                          | Description                                    |
|-----------------------------------|------------------------------------------------|
| `database-project.template.yaml`  | Creates roles, database, schema, and grants    |
| `database-backup.template.yaml`   | Dumps a plain SQL backup, no owner or ACLs     |
| `database-restore.template.yaml`  | Restores a dump and optionally re-grants roles |

### Playbook execution order for `database-project`

1. `create_nologin_role` — creates the owner role (no login) if an app role is also present
2. `create_login_role` — creates a login role (owner if no app role, app role if present)
3. `setup_database` — creates the database and schema with the owner role
4. `grant_app_role_privileges` — grants CRUD + future object privileges to the app role (if present)
5. `add_owner_role_members` — adds members to the owner role group (if provided)

## Usage

### Provision a new database
```bash
ansible-easy run \
  --template ./config-templates/database-project.template.yaml \
  --input ./workflow-input/my-project.yaml \
  --playbooks-dir ./playbooks
```

### Backup a database
```bash
ansible-easy run \
  --template ./config-templates/database-backup.template.yaml \
  --input ./workflow-input/my-backup.yaml \
  --playbooks-dir ./playbooks
```

### Restore a database
```bash
ansible-easy run \
  --template ./config-templates/database-restore.template.yaml \
  --input ./workflow-input/my-restore.yaml \
  --playbooks-dir ./playbooks
```

## Input config examples

### Project
```yaml
database_type: postgresql
database_name: myapp-dev
password: secret123
owner_role: myapp-dev-owner
app_role: myapp-dev-app-role
owner_role_members:
  - jenkins
  - deploy-bot
connection:
  username: postgres
  password: secret123
  host: localhost
  port: 5432
  database_name: myapp-dev
```

### Backup
```yaml
connection:
  username: postgres
  password: secret123
  host: localhost
  port: 5432
  database_name: myapp-dev

output_path: /var/backups/myapp-dev.sql
```

### Restore
```yaml
connection:
  username: postgres
  password: secret123
  host: localhost
  port: 5432
  database_name: myapp-dev

input_path: /var/backups/myapp-dev.sql
target_role: myapp-dev-owner
app_role: myapp-dev-app-role
owner_role_members:
  - jenkins
  - deploy-bot
``` 