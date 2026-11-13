# Unified Kveldúlfur data model — beta

All external datasets feed **one PostgreSQL database**, using adapters. There is no need for a separate database per sport.

## Classification

- **Discipline / Role** — Lifting, Climbing, Projectiles, etc.
- **Class** — Powerlifting, Weightlifting, Strongman, Bouldering, etc.
- **Feat** — Bench press maximum, stone to shoulder, route completion, timed sprint, etc.
- **Performance** — A measured result, with units, source, date, conditions, and evidence.
- **Ranking definition** — A rule for which performances can actually be compared.

## Source rules

1. Preserve source identity, original event and raw record.
2. Maintain original source license and attribution.
3. Use stable source record keys so an import can safely be repeated.
4. Do **not** merge people by name. Link source identities only when verified.
5. Keep equipment, sex, weight class, ruleset, implement and grading system as explicit conditions where relevant.
6. Do not treat external source data as independently verified by Kveldúlfur.
7. Only import sources where reuse and redistribution are permitted.
8. Imported data is not the same as an athlete account; athletes should eventually be able to claim profiles and control their own contributed data.
9. Private records must not be exposed through public rankings or other exports.

## OpenPowerlifting mapping (first adapter)

| Source CSV field | Unified destination |
| --- | --- |
| Name | athlete_source_identities.source_display_name |
| Federation, MeetName, Date | events and provenance |
| Best3SquatKg | feat: squat single maximum |
| Best3BenchKg | feat: bench single maximum |
| Best3DeadliftKg | feat: deadlift single maximum |
| TotalKg | feat: powerlifting total |
| Equipment, Sex, BodyweightKg, WeightClassKg | performances.context |
| Place | performances.context; DQ/DD/NS excluded from ranked positive results |
| Original CSV row identifier / deterministic source key | performances.source_performance_key |

For the **beta**, the published top-N JSON is a small static cache for the existing rankings website. The SQL schema is **not yet deployed**, so the website still uses the JSON. A future database import should use *individual source rows*, not only the top-N cache, to enable athlete histories and legitimate percentile calculations.

## Planned adapters

- OpenPowerlifting — implemented beta top-N export; full source-row adapter next.
- OpenWeightlifting — adapter pending source-format and license verification.
- Strongman — adapter pending source-format and license verification.
- Climbing — adapter pending permission and consistent grading/benchmark semantics.
- KFA archives — manual or file-based import, with provenance.

The SQL definition is in `database/schema.sql`.
