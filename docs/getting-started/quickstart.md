---
icon: bolt
---

# Quickstart

This quickstart shows the smallest complete workflow:

- one template file
- one input file
- one Ansible playbook
- one CLI command

## 1. Create a template

Create `template.yaml`:

```yaml
name: demo_workflow
keys:
  - name: environment
    type: enum
    possible_values:
      - staging
      - production
    required: true

  - name: app_name
    type: str
    required: true

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
  - name: deploy_app
    condition:
      type: always
    mapping:
      - ansible_variable_name: ENVIRONMENT
        config_variable_name: environment
      - ansible_variable_name: APP_NAME
        config_variable_name: app_name
      - ansible_variable_name: HOST
        config_variable_name: connection.host
      - ansible_variable_name: PORT
        config_variable_name: connection.port
```

## 2. Create an input file

Create `input.yaml`:

```yaml
environment: staging
app_name: billing-api
connection:
  host: db.internal.example
  port: 5432
```

## 3. Create a playbook directory

Create `playbooks/deploy_app.yaml`:

```yaml
- name: Demo deployment
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Show received variables
      ansible.builtin.debug:
        msg:
          environment: "{{ ENVIRONMENT }}"
          app_name: "{{ APP_NAME }}"
          host: "{{ HOST }}"
          port: "{{ PORT }}"
```

{% hint style="info" %}
The playbook file name must match the template playbook `name`. In this example, `deploy_app` maps to `playbooks/deploy_app.yaml`.
{% endhint %}

## 4. Run the workflow

```bash
ansible-easy run \
  --template ./template.yaml \
  --input ./input.yaml \
  --playbooks-dir ./playbooks
```

## 5. What happens next

The command will:

1. parse `template.yaml`
2. validate `input.yaml`
3. build Ansible extra-vars from the `mapping` section
4. execute `playbooks/deploy_app.yaml`

## Next steps

- Read [CLI Usage](../usage/cli.md) for the command surface.
- Read [Python Usage](../usage/python.md) if you want to embed the workflow in your own code.
- Read [Template Format](../concepts/template-format.md) for supported field types and conditions.
