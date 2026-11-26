---
name: sync-running-dashboard
description: >-
  Sync new Garmin Connect runs or strength sessions, evaluate them against the
  Vancouver 31-week marathon plan, update the running heatmap and coaching
  markdown doc, rebuild the standalone HTML dashboard (index.html), and push
  all updates to GitHub Pages. Use whenever the user says "update with latest
  run", "run completed", "sync", "update github html", or asks to log/evaluate
  a workout or modify the training schedule.
---

# Sync Running Dashboard & Marathon Coaching Pipeline

Runbook for syncing Garmin Connect activities, generating forensic coaching evaluations, rebuilding the standalone GitHub Pages dashboard (`index.html`), and pushing updates to GitHub.

---

## 1. Environment & Prerequisites

- **Python Dependencies**: Always run Garmin scripts with `uv run --with garminconnect==0.2.8 --with fitparse python3 ...` (pinned to `0.2.8` to match `requirements.txt` and long-lived Garth OAuth1/OAuth2 tokens).
- **Garmin Auth**: Uses saved OAuth tokens at `~/.garminconnect_tokens` (or the `GARMIN_TOKENS` environment variable if running in CI/cloud).
- **Repositories**:
  - **Heatmap Repo** (if present in workspace): `Projects/running-heatmap/repo` (`origin`: `tboats/garmin_heatmap`)
  - **Marathon Coaching & Dashboard Repo**: `Projects/la-marathon-2027/repo` (`origin`: `tboats/marathon-2027-training`, GitHub Pages serves `index.html` from `main`)

---

## 2. Standard Sync & Push Workflow

When the user finishes a run or strength session and asks to sync/update:

### Step 1: Sync Running Heatmap (if `Projects/running-heatmap/repo` exists)

```bash
cd Projects/running-heatmap/repo && uv run --with garminconnect==0.2.8 --with fitparse python3 sync_garmin.py --auto-push
```

This downloads new `.fit` routes into `data/runs.json`, refreshes `data/segments.json`, and pushes to `tboats/garmin_heatmap`.

### Step 2: Sync, Evaluate & Rebuild Marathon Dashboard

```bash
cd Projects/la-marathon-2027/repo && uv run --with garminconnect==0.2.8 --with fitparse python3 sync_and_eval.py --auto-push
```

What `sync_and_eval.py --auto-push` automatically executes:
1. Fetches recent running and strength activities from Garmin Connect (default `--lookback 3` days).
2. Evaluates each activity against the 31-week Vancouver plan (`vancouver_plan_generator.py`).
3. Extracts rep-by-rep interval splits and recovery HR drops (`extract_intervals`) for quality/interval workouts.
4. Updates `data/coach_evaluations.json` and `docs/vancouver-31-week-coaching-plan.md`.
5. Runs `build_data.py` -> `data/dashboard_data.json` and `generate_dashboard_html.py` -> `index.html`.
6. Commits and pushes updated files to `origin/main` (updating GitHub Pages).

**Useful Flags**:
- `--lookback 7` — Look back further than 3 days if multiple workouts were missed.
- `--force-id <activity_id>` — Re-evaluate a specific Garmin activity ID.

### Step 3: Verify Push

Confirm `git status` is clean and the latest commit was pushed to `origin/main`.

---

## 3. Modifying the Training Schedule

If the user asks to rearrange or modify upcoming workouts:

1. Edit `Projects/la-marathon-2027/repo/vancouver_plan_generator.py` (update both the week dictionary in `get_vancouver_weekly_plan()` and any day-specific overrides in `get_vancouver_daily_details()`).
2. Update the matching week section in `Projects/la-marathon-2027/repo/docs/vancouver-31-week-coaching-plan.md`.
3. Rebuild data and HTML:
   ```bash
   cd Projects/la-marathon-2027/repo && python3 build_data.py && python3 generate_dashboard_html.py
   ```
4. If the immediate next workout (`next_workout` in `data/coach_evaluations.json` entry `0`) changed, update it so the Coach tab's "Up Next" card matches, then rebuild `generate_dashboard_html.py`.
5. Commit and push all modified files to `origin/main`.

---

## 4. Coaching Response Standards

### For Interval / Quality Runs
Whenever `intervals_breakdown` is present (Cruise Intervals, Threshold Reps, Tempo Intervals, Track, Time Trials), **always** include:
1. **Rep-by-Rep Table**: Rep #, Distance, Time, Pace, Avg HR, Peak HR, Cadence (Avg/Max spm), Ground Contact Time (ms), Vertical Ratio (%), and Avg Power (W).
2. **Recovery Telemetry**: Recovery duration, distance, and HR drop (peak rep HR down to recovery floor).
3. **Physiological Insights**: Pacing precision, elevation modulation, cardiac drift, and running economy.

### For Standard Runs & Strength Sessions
1. **Prescribed vs. Actual Table**: Distance, Duration, Raw Pace, Grade-Adjusted Pace (GAP), Avg/Max HR, Cadence, Elevation Gain, Training Effect (Aerobic/Anaerobic), and Grade.
2. **Up Next Preview**: Show the next scheduled session's workout, lifting rule, target pace, and HR ceiling.
3. **Always Commit & Push**: Never leave code, data, or `index.html` changes unpushed.
