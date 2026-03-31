import argparse
import yaml
from ansible_easy.scripts.config_parser import parse_config
from ansible_easy.scripts.playbook_runner import run_playbooks
from ansible_easy.scripts.log import logger


def cli():
    parser = argparse.ArgumentParser(
        description="ansible-easy: YAML-driven Ansible playbook runner"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a workflow")
    run_parser.add_argument(
        "--template", required=True, help="Path to the template config"
    )
    run_parser.add_argument(
        "--input", required=True, help="Path to the workflow input config"
    )
    run_parser.add_argument(
        "--playbooks-dir", required=True, help="Path to the ansible playbooks directory"
    )

    args = parser.parse_args()

    if args.command == "run":
        _run(args.template, args.input, args.playbooks_dir)


def _run(template_path: str, input_path: str, playbooks_dir: str):
    logger.info(f"Loading template: {template_path}")
    PydanticModel, playbooks_definition = parse_config(template_path)

    logger.info(f"Loading input: {input_path}")
    with open(input_path, "r") as f:
        input_data = yaml.safe_load(f)

    project = PydanticModel(**input_data)
    run_playbooks(project.model_dump(), playbooks_definition, playbooks_dir)
