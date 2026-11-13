# KFA Húsmet — kraftlyftingar

Public live board: https://hjalteyri-png.github.io/kfa-logs/logs/kfa.html

The website loads **only** `logs/data/kfa-house-records.json`. The older competition results and OpenPowerlifting imports stay separate.

## Eligibility and publication

- Members and visiting athletes may hold records.
- Training and competition attempts may both count, after KFA staff review.
- A separate USAPL weight class applies to every division.
- The public site is read-only; only GitHub repository maintainers may change the published records file.
- Previous approved performances remain in the JSON. The board displays the highest for each lift/division/weight class.
- The file is public: don't store unapproved claims, private athlete information or submissions in it.
- Use evidence and a known date; do not infer an athlete's bodyweight class from the old class label alone.

## Example record

Add a verified record to the `records` array:

```json
{
  "id": "kfa-house-unique-001",
  "athlete": "Name published with permission",
  "division": "Karlar",
  "weight_class": "100",
  "lift": "bench",
  "value": 165,
  "date": "2026-11-13",
  "affiliation": "visitor",
  "performance_type": "training",
  "venue": "Síldarkastalinn, Hjalteyri",
  "event": "Open gym",
  "source_url": "",
  "status": "approved"
}
```

The value is in kilograms. Valid `lift`: `squat`, `bench`, `deadlift`, `total`. Valid `affiliation`: `member` or `visitor`. Valid `performance_type`: `training` or `competition`. Valid `division`: `Karlar` or `Konur`.

**This is not instantaneous real-time editing:** commit the result to GitHub, then the Pages deployment publishes it. An authenticated in-site moderation dashboard and live update service are future work.
