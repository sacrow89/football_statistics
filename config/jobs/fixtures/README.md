# Running fixture ingestion locally

The fixture notebook calls API-Football directly, so run it on a computer or
runner that can reach the API. This job is not a Databricks job. By default,
the notebook loads seasons 2026, 2025, 2024, and 2023; set the `FIXTURE_SEASONS`
environment variable to a comma-separated list to select seasons for a run.

From the repository root in PowerShell:

```powershell
python -m pip install -r requirements.txt
python scripts\run_notebook.py --config config\jobs\fixtures\premier_league_fixtures.yml
```

Make sure `API_FOOTBALL_KEY` is available to that PowerShell process before
starting the runner. The job uses the `python3` Jupyter kernel and writes raw
responses into separate timestamped folders under
`data\bronze\fixtures\league_id=39\season=YYYY` for each season. The optional
`BRONZE_DATA_ROOT` environment variable selects an absolute bronze root;
otherwise the repository's `data\bronze` folder is used.

The YAML file configures the notebook, kernel, and per-cell timeout. The runner
does not save execution results into the notebook itself.

`azure-pipelines.yml` defines the optional Azure Pipelines schedule. To enable
it, connect an Azure Pipeline to this GitHub repository, register a Windows
self-hosted agent in the `Default` pool, and add `API_FOOTBALL_KEY` as a secret
pipeline variable. The workflow runs every Monday at 06:00 UTC, selects only
season 2026, and writes bronze data to the configured local path on the agent
computer. Update `BRONZE_DATA_ROOT` in the pipeline YAML if the data folder is
different on that computer. Run the self-hosted agent under an account that
has Python available and write access to `BRONZE_DATA_ROOT`; the agent must be
online for scheduled runs. Fixture JSON files under `data\bronze\fixtures` are
ignored by Git so recurring snapshots are not added to commits.
