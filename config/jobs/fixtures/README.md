# Running fixture ingestion locally

The fixture notebook calls API-Football directly, so run it on a computer or runner
that can reach the API. This job is not a Databricks job.

From the repository root in PowerShell:

```powershell
python -m pip install -r requirements.txt
python scripts\run_notebook.py --config config\jobs\fixtures\premier_league_2026.yml
```

Make sure `API_FOOTBALL_KEY` is available to that PowerShell process before
starting the runner. The job uses the `python3` Jupyter kernel and writes raw
responses into `data\bronze\fixtures\league_id=39\season=2026`.

The YAML file configures the notebook, kernel, and per-cell timeout. The runner
does not save execution results into the notebook itself. Scheduling is
intentionally not configured yet; once manual runs are confirmed, this command
can be added to Windows Task Scheduler or a cron environment.
