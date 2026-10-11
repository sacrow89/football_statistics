import argparse
from pathlib import Path

import nbformat
import yaml
from nbclient import NotebookClient


REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Execute a notebook using a YAML job configuration.")
    parser.add_argument(
        "--config",
        required=True,
        help="Path to the YAML configuration, relative to the repository root or absolute.",
    )
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = REPO_ROOT / config_path
    config_path = config_path.resolve()
    if not config_path.is_relative_to(REPO_ROOT):
        raise ValueError("The job configuration must be inside the repository.")

    with config_path.open(encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)
    if not isinstance(config, dict):
        raise ValueError(f"Job configuration must contain a YAML mapping: {config_path}")

    notebook_name = config.get("notebook")
    kernel_name = config.get("kernel_name")
    timeout_seconds = config.get("timeout_seconds")
    if not isinstance(notebook_name, str) or not notebook_name:
        raise ValueError("Job configuration must provide a non-empty 'notebook' path.")
    if not isinstance(kernel_name, str) or not kernel_name:
        raise ValueError("Job configuration must provide a non-empty 'kernel_name'.")
    if type(timeout_seconds) is not int or timeout_seconds <= 0:
        raise ValueError("Job configuration must provide a positive integer 'timeout_seconds'.")

    notebook_path = (REPO_ROOT / notebook_name).resolve()
    if not notebook_path.is_relative_to(REPO_ROOT):
        raise ValueError("The notebook path must be inside the repository.")
    if not notebook_path.is_file():
        raise FileNotFoundError(f"Notebook not found: {notebook_path}")

    print(f"Executing {notebook_path.relative_to(REPO_ROOT)}")
    notebook = nbformat.read(notebook_path, as_version=4)
    NotebookClient(
        notebook,
        timeout=timeout_seconds,
        kernel_name=kernel_name,
        resources={"metadata": {"path": str(REPO_ROOT)}},
    ).execute(cwd=str(REPO_ROOT))

    for cell in notebook.cells:
        for output in cell.get("outputs", []):
            if output.output_type == "stream":
                print(output.text, end="")
            elif output.output_type == "execute_result" and "text/plain" in output.data:
                print(output.data["text/plain"])

    print(f"Notebook completed successfully: {notebook_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
