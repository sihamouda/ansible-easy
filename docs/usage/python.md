---
icon: python
---

# Python Usage

`ansible-easy` can be used as an imported library when you want to integrate validation and playbook execution into a larger Python tool.

## Recommended import path

The cleanest current programmatic flow is:

```python
import yaml

from ansible_easy.scripts.config_parser import parse_config
from ansible_easy.scripts.playbook_runner import run_playbooks
```

## End-to-end example

```python
import yaml

from ansible_easy.scripts.config_parser import parse_config
from ansible_easy.scripts.playbook_runner import run_playbooks


def run_workflow(template_path: str, input_path: str, playbooks_dir: str) -> None:
    model_class, playbooks_definition = parse_config(template_path)

    with open(input_path, "r") as handle:
        input_data = yaml.safe_load(handle)

    project = model_class(**input_data)

    run_playbooks(
        config=project.model_dump(),
        playbooks_definition=playbooks_definition,
        playbooks_dir=playbooks_dir,
    )
```

## Convenience wrapper

The CLI uses an internal helper:

```python
from ansible_easy.main import _run

_run("./template.yaml", "./input.yaml", "./playbooks")
```

{% hint style="info" %}
`_run()` mirrors the CLI behavior, but the leading underscore signals an internal convenience function rather than a dedicated public API.
{% endhint %}

## Returned objects

`parse_config(template_path)` returns:

- `model_class`: a dynamically created Pydantic model
- `playbooks_definition`: the parsed playbook metadata list

This gives you room to:

- validate input separately from execution
- inspect or transform the validated config before running playbooks
- wrap the runner in your own retry, audit, or orchestration code

## Common integration pattern

If you are building a service or internal automation wrapper, a practical pattern is:

1. keep workflow templates version-controlled
2. accept user or pipeline input as YAML or JSON
3. validate input with `parse_config()`
4. log or persist the validated payload
5. call `run_playbooks()`

## Exceptions to expect

- malformed template structure raises `ParseStructureException`
- invalid input values raise Pydantic validation errors
- failed playbook runs raise a generic exception from the runner layer

## Current API boundaries

Today, the importable surface is best treated as low-level workflow primitives, not a high-level SDK. The most useful modules are:

- `ansible_easy.scripts.config_parser`
- `ansible_easy.scripts.playbook_runner`
- `ansible_easy.main`
