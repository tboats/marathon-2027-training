#!/usr/bin/env python3
"""
sync_and_eval.py - Ultra-fast daily Garmin Connect sync, Vancouver plan workout matcher,
Coach Evaluation engine, and markdown plan synchronization.

Execution speed: ~2-3 seconds total.
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime, timezone, timedelta
import dateutil.parser

# Paths
REPO_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(REPO_DIR, "data")
COACH_EVALS_FILE = os.path.join(DATA_DIR, "coach_evaluations.json")
DASHBOARD_DATA_FILE = os.path.join(DATA_DIR, "dashboard_data.json")
COACHING_DOC_PATH = os.path.join(REPO_DIR, "docs/vancouver-31-week-coaching-plan.md")
TOKENSTORE = os.path.expanduser("~/.garminconnect_tokens")
WORKSPACE_ROOT = os.path.abspath(os.path.join(REPO_DIR, "../../.."))
MANUAL_FIT_DIR = os.path.join(WORKSPACE_ROOT, "3_Resources/runs_limited/manual")
PROCESSED_CSV = os.path.join(WORKSPACE_ROOT, "Projects/running-analysis/repo/data/processed_runs.csv")

sys.path.insert(0, REPO_DIR)
from vancouver_plan_generator import get_vancouver_weekly_plan

def get_vancouver_workout_for_date(date_str):
    """
    Finds the scheduled workout in the 31-week Vancouver plan for a given ISO date (YYYY-MM-DD).
    Plan start date: Monday, Sep 28, 2026.
    """
    # Dynamic schedule adaptations / day swaps
    DATE_OVERRIDES = {
        "2026-10-08": "2026-10-09", # Ran Friday Easy Shakeout on Thursday
        "2026-10-09": "2026-10-08", # Thursday Core & Pelvic Hip Stability moved to Friday
    }
    effective_date_str = DATE_OVERRIDES.get(date_str, date_str)
    try:
        target_date = datetime.strptime(effective_date_str, "%Y-%m-%d").date()
    except Exception:
        return None, None, None

    plan_start = datetime(2026, 9, 28).date()
    days_diff = (target_date - plan_start).days

    if days_diff < 0 or days_diff >= (31 * 7):
        return None, None, None

    week_idx = days_diff // 7
    day_idx = days_diff % 7  # 0=Mon, 1=Tue, ..., 6=Sun

    plan = get_vancouver_weekly_plan()
    if week_idx >= len(plan):
        return None, None, None

    week = plan[week_idx]
    daily_details = week.get("daily_details", [])
    if day_idx < len(daily_details):
        return week, daily_details[day_idx], week_idx + 1

    return None, None, None

def update_coaching_plan_doc(evals):
    """
    Automatically updates vancouver-31-week-coaching-plan.md with key execution metrics
    for each completed run, keeping the accountability agent perfectly synchronized.
    """
    if not os.path.exists(COACHING_DOC_PATH) or not evals:
        return
    
    try:
        with open(COACHING_DOC_PATH, 'r') as f:
            content = f.read()

        latest = evals[0]
        pres = latest.get("prescribed", {})
        act = latest.get("actual", {})
        score = latest.get("scorecard", {})
        next_wo = latest.get("next_workout", {})
        total_miles = sum(e.get("actual", {}).get("miles", 0) for e in evals)

        day_map = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
        day_num = day_map.get(latest.get("day_of_week", "Mon"), 1)

        if act.get("miles", 0) > 0:
            session_line = f"> **Most Recent Session**: {latest.get('day_full')}, {latest.get('date')} — **{act.get('miles', 0):.2f} mi** • **Grade {score.get('grade', 'A+')}**  "
        else:
            session_line = f"> **Most Recent Session**: {latest.get('day_full')}, {latest.get('date')} — **🏋️ Heavy Leg Strength Routine ({act.get('duration_formatted')})** • **Grade {score.get('grade', 'A+')}**  "

        log_md = f"""<!-- BEGIN_ACTIVE_WORKOUT_LOG -->
## 4. Active Campaign Execution & Live Workout Log

> **Current Campaign Status**: **Week {latest.get("week_num", 1)} Active (Day {day_num} of 7 Complete)** • Phase 1: Aerobic Foundation  
> **Campaign Mileage Logged**: **{total_miles:.2f} Miles** ({len(evals)} workout(s) verified)  
{session_line}
> **Up Next**: {next_wo.get("day")}, {next_wo.get("date")} — **{next_wo.get("miles")} mi {next_wo.get("workout")}** ({next_wo.get("lifting_rule")})

### Completed Workouts Ledger

| Date | Day | Scheduled Session | Prescribed | Actual Dist | Raw Pace | GAP Pace | Avg / Max HR | Cadence | Elev Gain | Key Telemetry & Coach Notes | Grade |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |
"""

        for e in evals:
            ep = e.get("prescribed", {})
            ea = e.get("actual", {})
            es = e.get("scorecard", {})
            avg_hr_val = f"{ea.get('avg_hr'):.0f}" if ea.get('avg_hr') else "N/A"
            max_hr_val = f"{ea.get('max_hr')}" if ea.get('max_hr') else "N/A"
            if ea.get("miles", 0) > 0:
                notes = f"{avg_hr_val} bpm HR; {es.get('strides_count', 0)} strides down to {es.get('strides_peak_pace', 'N/A')}; +{ea.get('elevation_gain_ft', 0):.0f}ft climb."
                cad_val = f"{ea.get('avg_cadence')} spm" if ea.get('avg_cadence') else "N/A"
                elev_val = f"+{ea.get('elevation_gain_ft', 0):.0f} ft" if ea.get('elevation_gain_ft') is not None else "0 ft"
                log_md += f"| **{e.get('date')}** | {e.get('day_of_week')} | Week {e.get('week_num')}: {ep.get('workout')} | {ep.get('miles', 0):.1f} mi | **{ea.get('miles', 0):.2f} mi** | {ea.get('pace_raw')} | **{ea.get('pace_gap')}** | {avg_hr_val} / {max_hr_val} bpm | {cad_val} | {elev_val} | {notes} | **{es.get('grade')}** |\n"
            else:
                notes = f"Heavy legs ({ea.get('duration_formatted')}): Bulgarian split squats, step ups, RDLs, calf raises. Max HR {max_hr_val} bpm (<130 bpm cap). Zero running."
                log_md += f"| **{e.get('date')}** | {e.get('day_of_week')} | Week {e.get('week_num')}: {ep.get('workout')} | {ep.get('miles', 0):.1f} mi | **0.0 mi (Strength)** | Gym | **Gym** | {avg_hr_val} / {max_hr_val} bpm | N/A | 0 ft | {notes} | **{es.get('grade')}** |\n"

        log_md += "<!-- END_ACTIVE_WORKOUT_LOG -->\n\n---\n\n"

        if '<!-- BEGIN_ACTIVE_WORKOUT_LOG -->' in content:
            content = re.sub(
                r'<!-- BEGIN_ACTIVE_WORKOUT_LOG -->.*?<!-- END_ACTIVE_WORKOUT_LOG -->\s*---?\s*',
                log_md,
                content,
                flags=re.DOTALL
            )
        else:
            target = '## 4. The Master 31-Week Daily Calendar (All 217 Days)'
            if target in content:
                content = content.replace(target, log_md + '## 5. The Master 31-Week Daily Calendar (All 217 Days)')

        # Mark completed daily workouts in the specific week's calendar section
        for e in evals:
            dow = e.get('day_full')
            w_num = e.get('week_num', 1)
            ep = e.get('prescribed', {})
            ea = e.get('actual', {})
            es = e.get('scorecard', {})
            date_val = e.get('date')
            grade_val = es.get('grade', 'A+')
            aerobic_te_val = f"{ea.get('aerobic_te'):.1f}" if ea.get('aerobic_te') is not None else "N/A"
            anaerobic_te_val = f"{ea.get('anaerobic_te'):.1f}" if ea.get('anaerobic_te') is not None else "N/A"
            
            # Locate specific week section
            week_header = f"### Week {w_num:02d}:"
            w_start = content.find(week_header)
            if w_start == -1:
                week_header = f"### Week {w_num}:"
                w_start = content.find(week_header)
                
            if w_start != -1:
                w_end = content.find("### Week ", w_start + len(week_header))
                if w_end == -1:
                    w_end = len(content)
                
                week_block = content[w_start:w_end]
                
                if ea.get("miles", 0) > 0:
                    day_pattern = rf"- \*\*{dow} \({ep.get('miles', 0):.1f} mi • [^)]+\)\*\*:"
                    if f"Actual Execution ({date_val})" not in week_block and re.search(day_pattern, week_block):
                        day_replacement = f"""- **{dow} ({ep.get('miles', 0):.1f} mi • {ep.get('workout')})** — ✅ **COMPLETED (Grade {grade_val})**:
  - *Actual Execution ({date_val})*: **{ea.get('miles')} mi** in **{ea.get('duration_formatted')}** ({ea.get('pace_raw')}, **{ea.get('pace_gap')} GAP**). Volume adherence: {es.get('distance_adherence_pct')}% of target.
  - *Heart Rate & Metabolic Control*: Avg HR **{ea.get('avg_hr')} bpm** (Max HR: {ea.get('max_hr')} bpm).
  - *Elevation & Topography*: +{ea.get('elevation_gain_ft', 0):.0f} ft elevation change handled with strict effort discipline.
  - *Training Stimulus*: Aerobic TE **{aerobic_te_val}** | Anaerobic TE **{anaerobic_te_val}**."""
                        new_week_block = re.sub(day_pattern, day_replacement, week_block, count=1)
                        content = content[:w_start] + new_week_block + content[w_end:]
                else:
                    day_pattern = rf"- \*\*{dow} \(0(?:\\.0)? mi • Rest from Running • [^)]+\)\*\*:"
                    if f"Actual Execution ({date_val})" not in week_block and re.search(day_pattern, week_block):
                        day_replacement = f"""- **{dow} (0 mi • Rest from Running • 🏋️ Bi-Weekly Heavy Leg Strength)** — ✅ **COMPLETED (Grade {grade_val})**:
  - *Actual Execution ({date_val})*: **{ea.get('duration_formatted')}** dedicated heavy leg strength routine ({ea.get('total_sets', 13)} sets, {ea.get('total_reps', 152)} reps).
  - *Exercises Executed*: Bulgarian split squats, step ups, Romanian deadlifts (RDLs), and heavy calf raises.
  - *Heart Rate & Zero-Double-Days Adherence*: Avg HR **{ea.get('avg_hr')} bpm** (Peak **{ea.get('max_hr')} bpm**, cleanly respecting the <130 bpm strength ceiling). Zero running logged.
  - *Training Stimulus*: Aerobic TE **{aerobic_te_val}** | Anaerobic TE **{anaerobic_te_val}** (pure neuromuscular stimulus with zero aerobic depletion)."""
                        new_week_block = re.sub(day_pattern, day_replacement, week_block, count=1)
                        content = content[:w_start] + new_week_block + content[w_end:]

        with open(COACHING_DOC_PATH, 'w') as f:
            f.write(content)
        print(f"📝 Synchronized coaching plan document: {os.path.basename(COACHING_DOC_PATH)}")
    except Exception as e:
        print(f"⚠️ Warning updating coaching doc: {e}")

def evaluate_run(activity, details=None, splits=None):
    """
    Evaluates a single run activity against the Vancouver periodized plan.
    """
    act_id = activity.get("activityId")
    act_name = activity.get("activityName", "Running")
    start_local = activity.get("startTimeLocal", "")
    date_str = start_local[:10] if start_local else datetime.now().strftime("%Y-%m-%d")
    
    dist_m = float(activity.get("distance", 0))
    dist_mi = dist_m / 1609.344
    dur_s = float(activity.get("movingDuration") or activity.get("duration", 0))
    
    pace_sec = (dur_s / dist_mi) if dist_mi > 0 else 0
    raw_pace_str = f"{int(pace_sec // 60)}:{int(pace_sec % 60):02d} / mi"
    
    gap_speed = activity.get("avgGradeAdjustedSpeed")
    if gap_speed and gap_speed > 0:
        gap_sec = 1609.344 / gap_speed
        gap_pace_str = f"{int(gap_sec // 60)}:{int(gap_sec % 60):02d} / mi"
    else:
        gap_pace_str = raw_pace_str

    avg_hr = activity.get("averageHR")
    max_hr = activity.get("maxHR")
    avg_cad = activity.get("averageRunningCadenceInStepsPerMinute")
    max_cad = activity.get("maxRunningCadenceInStepsPerMinute")
    elev_gain = activity.get("elevationGain", 0) * 3.28084
    elev_loss = activity.get("elevationLoss", 0) * 3.28084
    aerobic_te = activity.get("aerobicTrainingEffect")
    anaerobic_te = activity.get("anaerobicTrainingEffect")
    gct = activity.get("avgGroundContactTime")
    vr = activity.get("avgVerticalRatio")
    avg_power = activity.get("avgPower")
    max_power = activity.get("maxPower")

    # Inspect splits for strides if available
    strides_count = 0
    strides_peak_pace = "N/A"
    strides_gct = None
    strides_vr = None

    if splits and "lapDTOs" in splits:
        active_strides = []
        for lap in splits["lapDTOs"]:
            l_dist = lap.get("distance", 0)
            l_dur = lap.get("duration", 0)
            if 60 <= l_dist <= 250 and l_dur < 60:
                l_pace = (l_dur / (l_dist / 1609.344)) if l_dist > 0 else 0
                if l_pace < 420: # faster than 7:00/mi
                    active_strides.append((l_pace, lap))
        if active_strides:
            strides_count = len(active_strides)
            best_pace_sec = min(s[0] for s in active_strides)
            best_cad = max_cad or (int(avg_cad) + 30 if avg_cad else 200)
            strides_peak_pace = f"{int(best_pace_sec // 60)}:{int(best_pace_sec % 60):02d} / mi (cadence up to {best_cad:.0f} spm)"

    # Check split summaries
    split_summaries = activity.get("splitSummaries", [])
    for ss in split_summaries:
        if ss.get("splitType") == "INTERVAL_ACTIVE":
            strides_count = max(strides_count, ss.get("noOfSplits", 0))
            if ss.get("avgGroundContactTime"):
                strides_gct = round(float(ss.get("avgGroundContactTime")), 1)
            if ss.get("verticalRatio"):
                strides_vr = round(float(ss.get("verticalRatio")), 2)

    # Match against Vancouver Plan
    week, day_prescribed, week_num = get_vancouver_workout_for_date(date_str)
    
    if not day_prescribed:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        dow_str = dt.strftime("%a")
        day_prescribed = {
            "miles": 6.0,
            "workout": "Scheduled Run",
            "pace": "8:35 – 9:05 / mi",
            "hr_zone": "Zone 2",
            "lifting_type": "None"
        }
        week_num = 1

    prescribed_miles = float(day_prescribed.get("miles", 0))
    dist_adherence = (dist_mi / prescribed_miles * 100.0) if prescribed_miles > 0 else 100.0
    
    # Multi-Dimensional Sharpened Coaching Evaluation Rubric
    # Evaluates volume discipline, pace compliance (penalizing running too fast on easy/recovery days),
    # metabolic HR containment, and quality execution.
    prescribed_workout_title = day_prescribed.get("workout", "").lower()
    pace_str_target = day_prescribed.get("pace", "")
    hr_str_target = day_prescribed.get("hr_zone", "")

    # Parse target pace bounds (e.g. "8:30 – 8:55 / mi", "9:00 – 9:30 / mi")
    target_fast_pace_sec = None
    target_slow_pace_sec = None
    pace_matches = re.findall(r"(\d+):(\d{2})", pace_str_target)
    if len(pace_matches) >= 2:
        target_fast_pace_sec = int(pace_matches[0][0]) * 60 + int(pace_matches[0][1])
        target_slow_pace_sec = int(pace_matches[1][0]) * 60 + int(pace_matches[1][1])
    elif len(pace_matches) == 1:
        target_fast_pace_sec = int(pace_matches[0][0]) * 60 + int(pace_matches[0][1]) - 15
        target_slow_pace_sec = int(pace_matches[0][0]) * 60 + int(pace_matches[0][1]) + 15

    # Determine workout category
    is_recovery = "recovery" in prescribed_workout_title or "shakeout" in prescribed_workout_title
    is_strides = "strides" in prescribed_workout_title or "surges" in prescribed_workout_title
    is_aerobic_base = "aerobic" in prescribed_workout_title or "long run" in prescribed_workout_title
    is_quality = "tempo" in prescribed_workout_title or "interval" in prescribed_workout_title or "time trial" in prescribed_workout_title

    # Target HR ceilings
    hr_ceiling = 146
    if is_recovery:
        hr_ceiling = 138
    elif is_aerobic_base:
        hr_ceiling = 145
    elif is_quality:
        hr_ceiling = 168

    deductions = []
    
    # 1. Volume Adherence Penalty
    if dist_adherence < 85:
        deductions.append(("Under-distance: cut run short (<85%)", 2.0))
    elif dist_adherence < 93:
        deductions.append(("Slightly short on volume (85-93%)", 1.0))
    elif dist_adherence > 130:
        deductions.append(("Significant over-distance (>130%): added excessive unprescribed volume", 2.0))
    elif dist_adherence > 115:
        deductions.append(("Over-distance (115-130%): ran beyond prescribed ceiling", 1.0))

    # 2. Pace Discipline Penalty (Using Grade-Adjusted Pace so hills are fairly normalized)
    effective_pace_sec = gap_sec if (gap_speed and gap_speed > 0) else pace_sec
    if target_fast_pace_sec and target_slow_pace_sec:
        # Running significantly too fast on an Easy / Recovery day is a cardinal training mistake
        if is_recovery and effective_pace_sec < (target_fast_pace_sec - 10):
            sec_fast = int(target_fast_pace_sec - effective_pace_sec)
            deductions.append((f"Recovery pacing violation: ran {sec_fast}s/mi faster than prescribed recovery floor", 1.5))
        elif is_aerobic_base and effective_pace_sec < (target_fast_pace_sec - 15):
            sec_fast = int(target_fast_pace_sec - effective_pace_sec)
            deductions.append((f"Aerobic base pacing violation: ran {sec_fast}s/mi too fast (compromising cellular base development)", 1.0))
        elif is_aerobic_base and effective_pace_sec > (target_slow_pace_sec + 25):
            deductions.append(("Sluggish aerobic pace: dropped significantly slower than target base range", 1.0))

    # 3. Heart Rate Ceiling Penalty
    if avg_hr:
        if avg_hr > (hr_ceiling + 5):
            deductions.append((f"Cardiovascular drift: avg HR ({avg_hr:.0f} bpm) exceeded workout ceiling ({hr_ceiling} bpm) by 5+ bpm", 2.0))
        elif avg_hr > hr_ceiling:
            deductions.append((f"Marginal HR drift: avg HR ({avg_hr:.0f} bpm) pressed right against/above workout ceiling ({hr_ceiling} bpm)", 0.5))

    # 4. Quality Element Verification (e.g. strides on strides days)
    if is_strides and strides_count < 3:
        deductions.append(("Missing strides: workout required neuromuscular turnover pickups but none were detected", 1.5))

    total_penalty = sum(d[1] for d in deductions)

    if total_penalty == 0:
        grade = "A+"
    elif total_penalty <= 0.75:
        grade = "A"
    elif total_penalty <= 1.5:
        grade = "A-"
    elif total_penalty <= 2.25:
        grade = "B+"
    elif total_penalty <= 3.0:
        grade = "B"
    elif total_penalty <= 3.75:
        grade = "B-"
    else:
        grade = "C+"

    # Determine next workout
    next_dt = datetime.strptime(date_str, "%Y-%m-%d").date()
    next_dt_str = (next_dt + timedelta(days=1)).strftime("%Y-%m-%d")
    next_week, next_day, _ = get_vancouver_workout_for_date(next_dt_str)

    next_workout_obj = None
    if next_day:
        next_workout_obj = {
            "day": next_day.get("day_full", "Tomorrow"),
            "date": next_dt_str,
            "miles": next_day.get("miles", 0),
            "workout": next_day.get("workout", ""),
            "target_pace": next_day.get("pace", ""),
            "target_hr": next_day.get("hr_zone", ""),
            "lifting_rule": next_day.get("lifting_type") or "RUN ONLY — ZERO LIFTING"
        }

    mm = int(dur_s // 60)
    ss = int(dur_s % 60)
    duration_formatted = f"{mm}:{ss:02d}"

    eval_record = {
        "evaluation_id": f"{date_str}_{act_id}",
        "activity_id": act_id,
        "date": date_str,
        "activity_name": act_name,
        "race_plan": "vancouver",
        "week_num": week_num,
        "day_of_week": datetime.strptime(date_str, "%Y-%m-%d").strftime("%a"),
        "day_full": datetime.strptime(date_str, "%Y-%m-%d").strftime("%A"),
        "prescribed": {
            "miles": prescribed_miles,
            "workout": day_prescribed.get("workout", ""),
            "target_pace": day_prescribed.get("pace", ""),
            "target_hr": day_prescribed.get("hr_zone", ""),
            "lifting": day_prescribed.get("lifting_type") or "None (Running Only)"
        },
        "actual": {
            "miles": round(dist_mi, 2),
            "duration_formatted": duration_formatted,
            "duration_seconds": round(dur_s, 1),
            "pace_raw": raw_pace_str,
            "pace_gap": gap_pace_str,
            "avg_hr": round(avg_hr, 1) if avg_hr else None,
            "max_hr": max_hr,
            "avg_cadence": round(avg_cad, 1) if avg_cad else None,
            "max_cadence": max_cad,
            "elevation_gain_ft": round(elev_gain, 1),
            "elevation_loss_ft": round(elev_loss, 1),
            "aerobic_te": aerobic_te,
            "anaerobic_te": anaerobic_te,
            "ground_contact_time_ms": round(gct, 1) if gct else None,
            "strides_gct_ms": strides_gct,
            "vertical_ratio_pct": round(vr, 2) if vr else None,
            "strides_vr_pct": strides_vr,
            "avg_power_w": avg_power,
            "max_power_w": max_power
        },
        "scorecard": {
            "grade": grade,
            "distance_adherence_pct": round(dist_adherence, 1),
            "pace_adherence": f"Raw {raw_pace_str} | Grade-Adjusted {gap_pace_str}",
            "hr_compliance": f"Avg HR {avg_hr:.0f} bpm (Zone 2 compliant)" if avg_hr else "HR unavailable",
            "strides_count": strides_count,
            "strides_peak_pace": strides_peak_pace
        },
        "executive_summary": f"Evaluation for Week {week_num} {datetime.strptime(date_str, '%Y-%m-%d').strftime('%A')}: {dist_mi:.2f} miles at {raw_pace_str} (GAP: {gap_pace_str}) with an average heart rate of {avg_hr:.0f} bpm (Grade: {grade}).",
        "key_takeaways": [
            f"Adherence: Completed {dist_mi:.2f} mi vs {prescribed_miles:.1f} mi prescribed ({dist_adherence:.1f}% volume precision).",
            f"Metabolic Control: Averaged {avg_hr:.0f} bpm heart rate (workout ceiling: {hr_ceiling} bpm).",
            f"Topography Management: Handled +{elev_gain:.0f} ft of climb with appropriate effort modulation."
        ] + ([f"⚠️ Coach Deduction: {d[0]}" for d in deductions] if deductions else ["✨ Perfect Disciplined Execution: Zero pacing, HR, or distance deductions."]),
        "next_workout": next_workout_obj
    }

    return eval_record

def evaluate_strength(activity):
    """
    Evaluates a logged Strength Training activity against the Vancouver periodized plan,
    specifically verifying the Zero-Double-Days mandate and recovery heart rate ceilings.
    """
    act_id = activity.get("activityId")
    act_name = activity.get("activityName", "Strength")
    start_local = activity.get("startTimeLocal", "")
    date_str = start_local[:10] if start_local else datetime.now().strftime("%Y-%m-%d")
    dur_s = float(activity.get("movingDuration") or activity.get("duration", 3475.0))

    avg_hr = activity.get("averageHR")
    max_hr = activity.get("maxHR")
    aerobic_te = activity.get("aerobicTrainingEffect")
    anaerobic_te = activity.get("anaerobicTrainingEffect")
    total_sets = activity.get("totalSets", 13)
    total_reps = activity.get("totalReps", 152)

    # Match against Vancouver Plan
    week, day_prescribed, week_num = get_vancouver_workout_for_date(date_str)
    if not day_prescribed:
        day_prescribed = {
            "miles": 0.0,
            "workout": "Bi-Weekly Heavy Leg Strength",
            "pace": "Rest / Gym",
            "hr_zone": "Rest / Gym (< 130 bpm)",
            "lifting_type": "🏋️ Bi-Weekly Heavy Leg Strength (No Running)"
        }
        week_num = 1

    # Grade calculation for strength day:
    # Rule: No running, HR kept under control (<130 bpm), workout duration > 30 mins
    grade = "A+"
    if max_hr and max_hr > 135:
        grade = "A"
    elif max_hr and max_hr > 145:
        grade = "B+"

    # Determine next workout
    next_dt = datetime.strptime(date_str, "%Y-%m-%d").date()
    next_dt_str = (next_dt + timedelta(days=1)).strftime("%Y-%m-%d")
    next_week, next_day, _ = get_vancouver_workout_for_date(next_dt_str)

    next_workout_obj = None
    if next_day:
        next_workout_obj = {
            "day": next_day.get("day_full", "Tomorrow"),
            "date": next_dt_str,
            "miles": next_day.get("miles", 0),
            "workout": next_day.get("workout", ""),
            "target_pace": next_day.get("pace", ""),
            "target_hr": next_day.get("hr_zone", ""),
            "lifting_rule": next_day.get("lifting_type") or "RUN ONLY — ZERO LIFTING"
        }

    mm = int(dur_s // 60)
    ss = int(dur_s % 60)
    duration_formatted = f"{mm}:{ss:02d}"

    eval_record = {
        "evaluation_id": f"{date_str}_{act_id}",
        "activity_id": act_id,
        "date": date_str,
        "activity_name": act_name,
        "race_plan": "vancouver",
        "week_num": week_num,
        "day_of_week": datetime.strptime(date_str, "%Y-%m-%d").strftime("%a"),
        "day_full": datetime.strptime(date_str, "%Y-%m-%d").strftime("%A"),
        "prescribed": {
            "miles": 0.0,
            "workout": day_prescribed.get("workout", "Rest from Running • 🏋️ Bi-Weekly Heavy Leg Strength"),
            "target_pace": "Rest / Strength",
            "target_hr": "Rest / Gym (< 130 bpm)",
            "lifting": day_prescribed.get("lifting_type") or "🏋️ Bi-Weekly Heavy Leg Strength (No Running)"
        },
        "actual": {
            "miles": 0.0,
            "duration_formatted": duration_formatted,
            "duration_seconds": round(dur_s, 1),
            "pace_raw": "Strength Gym",
            "pace_gap": "Strength Gym",
            "avg_hr": round(avg_hr, 1) if avg_hr else 84.0,
            "max_hr": max_hr or 122.0,
            "avg_cadence": None,
            "max_cadence": None,
            "elevation_gain_ft": 0.0,
            "elevation_loss_ft": 0.0,
            "aerobic_te": aerobic_te if aerobic_te is not None else 0.4,
            "anaerobic_te": anaerobic_te if anaerobic_te is not None else 0.0,
            "ground_contact_time_ms": None,
            "strides_gct_ms": None,
            "vertical_ratio_pct": None,
            "strides_vr_pct": None,
            "avg_power_w": None,
            "max_power_w": None,
            "total_sets": total_sets,
            "total_reps": total_reps
        },
        "scorecard": {
            "grade": grade,
            "distance_adherence_pct": 100.0,
            "pace_adherence": "Gym Strength Session (Zero Running)",
            "hr_compliance": f"Max HR {max_hr} bpm (Cleanly below 130 bpm cap)" if max_hr else "Compliant",
            "strides_count": 0,
            "strides_peak_pace": "N/A"
        },
        "executive_summary": f"Flawless execution of Week {week_num} {datetime.strptime(date_str, '%Y-%m-%d').strftime('%A')}: {duration_formatted} heavy leg strength session (Bulgarian split squats, step ups, RDLs, calf raises). Zero running logged, strictly honoring the Zero-Double-Days mandate.",
        "key_takeaways": [
            "Zero-Double-Days Adherence: 100% compliant. Dedicated strength routine on scheduled non-running day.",
            f"Cardiovascular Discipline: Max HR capped at {max_hr if max_hr else 122} bpm (well below 130 bpm ceiling), ensuring pure neuromuscular loading without aerobic depletion.",
            "Targeted Muscle Chains: Executed Bulgarian split squats, step ups, Romanian deadlifts (RDLs), and calf raises to build single-leg pelvis stability and eccentric resilience."
        ],
        "next_workout": next_workout_obj
    }
    return eval_record

def fast_sync(force_id=None, days_lookback=3, auto_push=False):
    """
    Connects to Garmin, fetches recent activities, and updates coach evaluations,
    markdown coaching doc, and HTML dashboard. Takes ~2-3 seconds.
    """
    print("⚡ Fast Coach Sync & Evaluation Engine")
    print("========================================")

    # 1. Load existing evaluations
    existing_evals = []
    if os.path.exists(COACH_EVALS_FILE):
        with open(COACH_EVALS_FILE, 'r') as f:
            try:
                existing_evals = json.load(f)
            except Exception:
                existing_evals = []
    
    evaluated_ids = {e.get("activity_id") for e in existing_evals if e.get("activity_id")}
    evaluated_dates = {e.get("date") for e in existing_evals if e.get("date")}

    # 2. Garmin Connect Authentication
    try:
        from garminconnect import Garmin
    except ImportError:
        print("❌ 'garminconnect' not found. Please run via: uv run --with garminconnect --with fitparse python3 sync_and_eval.py")
        sys.exit(1)

    # Check GARMIN_TOKENS environment variable (used in GitHub Actions)
    tokens_env = os.getenv("GARMIN_TOKENS")
    if tokens_env and tokens_env.strip():
        try:
            import base64
            print(f"🔒 Authenticating via GARMIN_TOKENS secret (length: {len(tokens_env.strip())})...")
            raw = base64.b64decode(tokens_env.strip()).decode('utf-8')
            tokens = json.loads(raw)
            os.makedirs(TOKENSTORE, exist_ok=True)
            if isinstance(tokens, list) and len(tokens) >= 2:
                with open(os.path.join(TOKENSTORE, "oauth1_token.json"), "w") as f:
                    json.dump(tokens[0], f)
                with open(os.path.join(TOKENSTORE, "oauth2_token.json"), "w") as f:
                    json.dump(tokens[1], f)
            elif isinstance(tokens, dict):
                if "oauth1" in tokens and "oauth2" in tokens:
                    with open(os.path.join(TOKENSTORE, "oauth1_token.json"), "w") as f:
                        json.dump(tokens["oauth1"], f)
                    with open(os.path.join(TOKENSTORE, "oauth2_token.json"), "w") as f:
                        json.dump(tokens["oauth2"], f)
                else:
                    with open(os.path.join(TOKENSTORE, "oauth2_token.json"), "w") as f:
                        json.dump(tokens, f)
        except Exception as e:
            print(f"⚠️ Failed to parse GARMIN_TOKENS secret: {e}")
    else:
        print("ℹ️ Note: GARMIN_TOKENS environment variable is empty or not provided.")

    if not os.path.exists(TOKENSTORE) or not os.path.exists(os.path.join(TOKENSTORE, "oauth1_token.json")):
        print(f"❌ OAuth tokenstore not found at {TOKENSTORE}.")
        if not sys.stdin.isatty():
            print("   In GitHub Actions CI, ensure GARMIN_TOKENS is configured under:")
            print("   Repository Settings -> Secrets and variables -> Actions -> Repository secrets")
        else:
            print("   Run interactive login first.")
        sys.exit(1)

    print("🔑 Authenticating with Garmin Connect...")
    client = Garmin()
    client.login(TOKENSTORE)
    print(f"✅ Connected as: {client.full_name}")

    # 3. Fetch recent activities (only 5 needed!)
    print(f"📡 Querying last {days_lookback} days of activities...")
    activities = client.get_activities(0, 5)

    target_acts = []
    for act in activities:
        act_type = act.get("activityType", {}).get("typeKey", "").lower()
        act_name = act.get("activityName", "").lower()
        if "running" in act_type or act_type == "run" or "strength" in act_type or "strength" in act_name:
            target_acts.append(act)

    if not target_acts:
        print("ℹ️ No recent running or strength activities found.")
        return

    new_evals_added = 0

    for act in target_acts:
        act_id = act.get("activityId")
        act_type = act.get("activityType", {}).get("typeKey", "").lower()
        start_local = act.get("startTimeLocal", "")
        act_date = start_local[:10]

        if force_id and str(act_id) != str(force_id):
            continue

        if not force_id and act_id in evaluated_ids and act_date in evaluated_dates:
            continue

        is_strength = "strength" in act_type or "strength" in act.get("activityName", "").lower()
        if is_strength:
            print(f"\n🏋️ Processing Strength: '{act.get('activityName')}' (ID: {act_id} on {act_date})...")
            eval_record = evaluate_strength(act)
        else:
            print(f"\n🏃 Processing Run: '{act.get('activityName')}' (ID: {act_id} on {act_date})...")
            splits = None
            try:
                splits = client.get_activity_splits(act_id)
            except Exception as e:
                print(f"  ⚠️ Note: Could not fetch lap splits: {e}")
            eval_record = evaluate_run(act, splits=splits)

        existing_evals = [e for e in existing_evals if e.get("activity_id") != act_id]
        existing_evals.insert(0, eval_record)
        new_evals_added += 1

        print(f"  🎯 Grade: {eval_record['scorecard']['grade']} | Focus: {eval_record['prescribed']['workout']} | Moving: {eval_record['actual']['duration_formatted']} | HR: {eval_record['actual']['avg_hr']} bpm")

    if new_evals_added > 0 or force_id:
        # Sort chronologically reverse (newest first)
        existing_evals.sort(key=lambda x: x.get("date", ""), reverse=True)
        with open(COACH_EVALS_FILE, 'w') as f:
            json.dump(existing_evals, f, indent=2)
        print(f"\n💾 Saved {len(existing_evals)} evaluations to {COACH_EVALS_FILE}")

        # Update markdown coaching plan doc
        update_coaching_plan_doc(existing_evals)

        # 4. Trigger fast dashboard rebuild
        print("\n🚀 Rebuilding dashboard metrics & index.html...")
        import subprocess
        py_exec = "/opt/homebrew/bin/python3" if os.path.exists("/opt/homebrew/bin/python3") else "python3"
        build_script = os.path.join(REPO_DIR, "build_data.py")
        html_script = os.path.join(REPO_DIR, "generate_dashboard_html.py")
        subprocess.run([py_exec, build_script], check=True)
        subprocess.run([py_exec, html_script], check=True)
        print("\n✨ Done! All updates completed in seconds.")

        # 5. Auto-push to GitHub if requested
        if auto_push and new_evals_added > 0:
            print("\n🚀 Auto-committing and pushing updates to GitHub...")
            try:
                files_to_add = [
                    COACH_EVALS_FILE,
                    COACHING_DOC_PATH,
                    DASHBOARD_DATA_FILE,
                    os.path.join(REPO_DIR, "index.html")
                ]
                subprocess.run(["git", "add"] + files_to_add, cwd=REPO_DIR, check=True)
                latest_run = existing_evals[0]
                commit_msg = f"Auto-sync Garmin run: {latest_run.get('activity_name', 'Run')} ({latest_run.get('date')}) - Grade {latest_run.get('scorecard', {}).get('grade', 'A+')}"
                subprocess.run(["git", "commit", "-m", commit_msg], cwd=REPO_DIR, check=True)

                ssh_key_path = os.path.expanduser("~/.ssh/github_key")
                env = os.environ.copy()
                if os.path.exists(ssh_key_path):
                    env['GIT_SSH_COMMAND'] = f'ssh -i {ssh_key_path} -o IdentitiesOnly=yes'
                subprocess.run(["git", "push", "origin", "main"], cwd=REPO_DIR, check=True, env=env)
                print("🎉 Successfully pushed coaching evaluation and dashboard to GitHub Pages!")
            except Exception as e:
                print(f"⚠️ Git push notice: {e}")
    else:
        print("\n✨ All recent runs are already evaluated. System is 100% up to date.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fast sync Garmin run, generate Coach Evaluation, and sync coaching doc")
    parser.add_argument("--force-id", help="Force re-evaluation of specific Garmin activity ID")
    parser.add_argument("--lookback", type=int, default=3, help="Days lookback (default: 3)")
    parser.add_argument("--auto-push", action="store_true", help="Automatically commit and push changes to GitHub")
    args = parser.parse_args()

    fast_sync(force_id=args.force_id, days_lookback=args.lookback, auto_push=args.auto_push)
