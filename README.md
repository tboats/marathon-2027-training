# Marathon 2027: Sub-3:15 Training & Telemetry Hub

Personal telemetry, physiological analytics, and periodized training system targeting a **3:15:00 marathon finish** in 2027 (advancing from the 3:34:04 Seattle Marathon baseline on Nov 30, 2025).

Supports dual candidate races with interactive periodized schedules, course elevation profiles, and proxy metric tracking:
1. **ASICS Los Angeles Marathon**: Sunday, March 7, 2027 (23-Week Periodized Plan)
2. **BMO Vancouver Marathon**: Sunday, May 2, 2027 (31-Week Periodized Plan)

---

## 🏃 Executive Benchmark

| Metric | Seattle 2025 (Baseline) | Marathon 2027 (Goal) | The Delta |
| :--- | :--- | :--- | :--- |
| **Finish Time** | 3:34:04 | **3:15:00** | -19m 04s |
| **Flat-Course Equivalent** | 3:27:44 (36.3 ft/mi hills) | **3:15:00** | **-12m 44s true physiological gap** |
| **Target Pace** | 8:09 min/mile (5:04/km) | **7:26 min/mile** (4:37/km) | -43s / mile (+8.8% speed) |
| **VDOT Score** | 45.5 (47.1 flat) | **50.5** | +3.4 to +5.0 VDOT points |
| **Target Race HR** | 152.7 bpm | **151 – 155 bpm** | Zone 3 Aerobic Cruise |
| **Peak Mileage** | ~45 miles / week | **56 – 58 miles / week** | +11–13 mpw with MP quality blocks |

---

## 🖥️ Interactive HTML Dashboard

The dashboard is completely standalone (`index.html`), zero-dependency, and works locally or on **GitHub Pages**:
- **Race Selector**: Toggle between **🌴 LA Marathon**, **🌲 Vancouver Marathon**, and **⚖️ Head-to-Head Comparison**.
- **Interactive Training Calendars**:
  - Full 23-Week LA Plan (5 phases) and 31-Week Vancouver Plan (6 phases).
  - Exact daily running mileages (Mon–Sun) with collapsible workout detail cards.
  - Integrated concurrent strength training schedule (bi-weekly alternating heavy legs and pelvic/hip stability).
- **Elevation & Grade-Adjusted Pace (GAP)**: Course profile vs Seattle training terrain (52.4 ft/mi climbing).
- **6 Core Proxy Indicators**: Live telemetry tracking Aerobic Efficiency Factor (EF & GAP-EF), Cardiac Drift (Pw:HR), Threshold Pace, MP HR Convergence, VDOT tune-up races, and volume density.

### Viewing Locally
```bash
# On macOS:
open index.html

# Or with local web server:
python3 -m http.server 8080
# Visit http://localhost:8080
```

---

## 📖 In-Depth Strategy Guides

- [**Los Angeles Marathon 2027 Master Strategy Guide**](docs/la-marathon-3-15-plan.md): Forensic Seattle analysis, 23-week periodization, mile-by-mile tactics.
- [**BMO Vancouver Marathon 2027 Master Strategy Guide**](docs/vancouver-marathon-3-15-plan.md): 31-week periodization, Camosun Hill pacing, Seawall tactics.
- [**Vancouver 31-Week Master Coaching & Accountability Plan**](docs/vancouver-31-week-coaching-plan.md): Complete day-by-day 217-day schedule, daily execution notes, lifting assignments, and AI agent operating directives.
- [**Head-to-Head Decision Matrix (LA vs. Vancouver)**](docs/la-vs-vancouver-comparison.md): 8-dimension comparison (weather, elevation, logistics, 85% vs 92% probability).

---

## 🔄 Updating Data with New Garmin Runs

Whenever new runs are completed or synced:

```bash
python3 sync_and_update.py
```

This pipeline will:
1. Connect to Garmin Connect (using your cached OAuth token in `~/.garminconnect_tokens`).
2. Download any new FIT activities.
3. Re-calculate Aerobic Efficiency Factor (EF), Grade-Adjusted Pace (GAP), monthly miles, and recent runs.
4. Regenerate `data/dashboard_data.json` and compile the standalone `index.html`.
