# OpenPowerlifting import — Kveldúlfur Logs

Official dataset: https://data.openpowerlifting.org

OpenPowerlifting publishes its competition data to the public domain. Attribution is recommended:
"This page uses data from the OpenPowerlifting project, https://www.openpowerlifting.org."

## Run locally

1. Download `openpowerlifting-latest.zip` from the official data site.
2. From the repository root, run:

```bash
python tools/import_openpowerlifting.py /path/to/openpowerlifting-latest.zip
```

3. This generates `logs/data/openpowerlifting.json`, which the site can use for the rankings view. Commit that generated JSON only if its size is manageable. The ZIP itself should not be committed.

## Rules for this first importer

- Reads the official ZIP as a stream without loading the entire CSV into memory.
- Excludes disqualified, doping-disqualified and no-show entries.
- Uses positive best successful squat, bench, deadlift and total results.
- Keeps sex and equipment categories separate.
- Retains each athlete's best result within each feat/sex/equipment category.
- Exports top 100 per category by default; use `--limit` to change.
- Includes source meet, federation, date and bodyweight when available.
- **Does not** calculate meaningful population percentiles from top-N exports.
- **Does not** merge different names, categories, rulesets or federations.
- This is a historical ranking prototype, not official OpenPowerlifting rankings.

## Next

Connect the generated JSON to the site, add filters and provenance, then build database storage and a reproducible import/update process.
