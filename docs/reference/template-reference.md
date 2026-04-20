---
icon: list-check
---

# Template Reference

This page documents the template fields supported by the current implementation.

## Top-level fields

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `name` | `str` | Yes | Used as the generated Pydantic model name |
| `keys` | `list` | Yes | Input schema definition |
| `playbooks` | `list` | Yes | Ordered list of playbook execution rules |

## Key definition fields

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `name` | `str` | Yes | Input field name |
| `type` | `str` | Yes | One of `str`, `int`, `enum`, `list`, `object` |
| `required` | `bool` | Yes | Required by the parser for every key |
| `possible_values` | `list` | For `enum` | Allowed enum values |
| `elements_type` | `str` | For `list` | Currently only `str` is supported |
| `keys` | `list` | For `object` | Nested field definitions |

## Playbook definition fields

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `name` | `str` | Yes | Resolves to `<name>.yaml` |
| `condition` | `object` | Yes | Execution rule |
| `mapping` | `list` | Yes | Config-to-Ansible variable mapping |

## Condition fields

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `type` | `str` | Yes | `always`, `field_present`, `field_absent` |
| `field` | `str` | Only for `field_present` and `field_absent` | Evaluated as a top-level config key |

## Mapping fields

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `ansible_variable_name` | `str` | Yes | Name sent to Ansible extra-vars |
| `config_variable_name` | `str` | Yes | Field path in the validated config |
| `dir_path` | `bool` | No | Defaults to `false` |

## Supported types

| Type | Supported | Notes |
| --- | --- | --- |
| `str` | Yes | Optional and required forms work |
| `int` | Yes | Optional and required forms work |
| `enum` | Yes | Values are constrained with `Literal[...]` |
| `list[str]` | Yes | Only string lists are implemented |
| `object` | Yes | Nested structures are supported |

## Current implementation caveats

The docs for your workflows should account for the current behavior of the package:

- `mapping.config_variable_name` supports dot notation.
- `condition.field` does not support dot notation.
- `list` only supports `elements_type: str`.
- `dir_path` only affects string values.
- Relative path expansion uses the current process working directory.

{% hint style="warning" %}
Although every key requires a `required` flag in the template, the current parser behavior is stricter for some types than others. In particular, `enum`, `list`, and `object` fields should be treated as required in real workflows, even if you set `required: false`.
{% endhint %}
