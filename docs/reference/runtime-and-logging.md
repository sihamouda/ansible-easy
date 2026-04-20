---
icon: scroll
---

# Runtime and Logging

`ansible-easy` uses standard Python logging and configures both console and file handlers at import time.

## Default runtime settings

| Setting | Default |
| --- | --- |
| `log_file_path` | `/tmp` |
| `log_file_name` | `ansible-easy.log` |
| `log_level` | `INFO` |

## Environment variables

These settings are read through `pydantic-settings`, so environment variables such as the following are useful in practice:

```bash
export LOG_FILE_PATH=/var/log/ansible-easy
export LOG_FILE_NAME=workflow.log
export LOG_LEVEL=DEBUG
```

## Log destinations

Logs are written to:

- stdout or stderr through a stream handler
- a file handler at `<LOG_FILE_PATH>/<LOG_FILE_NAME>`

## Typical output

```text
2026-03-31 10:38:10 [INFO] [setup] started
2026-03-31 10:38:10 [INFO] [setup] [Create resource] ok (no change)
2026-03-31 10:38:12 [INFO] [setup] [Configure resource] changed
2026-03-31 10:38:14 [INFO] [setup] finished
```

## Failure behavior

- unreachable hosts are logged as errors
- failed tasks are logged as errors
- a failed playbook raises an exception after `ansible-runner` returns

## Operational guidance

- ensure the log directory exists before execution
- set `LOG_LEVEL=DEBUG` when diagnosing mapping or playbook behavior
- use a writable, workflow-specific log path in CI or automation runners
