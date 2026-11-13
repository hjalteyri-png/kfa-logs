# KFA Performance Ladder — admin-published beta

Public board: https://hjalteyri-png.github.io/kfa-logs/logs/kfa.html

## Publication and permissions

The public website is read-only. Only GitHub collaborators with write permission can edit `logs/data/kfa-results.json` on the published branch. GitHub commit history is the audit log for the beta. This is **not** an in-browser login system.

To publish a result, open `logs/data/kfa-results.json` via GitHub, edit it while signed in with write permission, and commit. The site updates when GitHub Pages deploys.

To collect submissions without granting write access, have members send details to club staff outside the public website. An actual submission queue and admin login will need authenticated server-side infrastructure. Do not put secrets in HTML/JavaScript.

## Result entry

Add objects in `results` with these fields:

```json
{
  "id": "kfa-unique-0001",
  "athlete": "Public display name with permission",
  "feat": "bench",
  "value": 120,
  "category": "Raw / Open",
  "date": "2026-11-13",
  "event": "Named club event",
  "source": "KFA",
  "source_url": "",
  "notes": "Competition attempt",
  "status": "approved"
}
```

Only entries with `status: "approved"` appear on the public ladder. Drafts and pending submissions should **not** be put in this publicly accessible JSON at all, even with a different status: the whole file is public.

- Numeric `value` uses the feat's unit.
- Use consistent category labels (e.g. `Raw / Open`, `Equipped / Open`).
- Define feats in `feats` before referencing them.
- The board ranks the best approved result for each athlete **and category**; all approved historical logs are retained in the data file.
- Avoid publishing sensitive data about minors without proper permission.
- Link to results.kraft.is records if authorized; do not bulk-copy its copyrighted database without permission.

## Current scope

The board starts deliberately empty rather than publishing invented or unapproved KFA performances. A historical source reference is linked on the page. When staff approve initial results, they will appear immediately after the static site is redeployed.

Next phase: staff authentication, athlete identity reconciliation, review queue, and private storage.

## Historical record divisions (v0.2)

The public board now filters by **sex / record division**, **weight class**, and **equipment / category** separately. The historical KFA source links are recorded in `record_classes` in `kfa-results.json`.

The original 2019 record tables were not retrievable, so `weight_classes` are intentionally empty. **Do not invent or substitute modern weight classes.** After verifying the original class labels, place them in the corresponding `record_classes[].weight_classes` arrays (e.g. labels exactly as printed), and add `sex` and `weight_class` fields to each approved result. A rank under 'All weight classes' is an exploratory comparison only, not a single official record class.
