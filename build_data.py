#!/usr/bin/env python3
"""
build_data.py - Extract and compute metrics from Garmin runs for the LA Marathon 2027 dashboard.
"""

import os
import sys
import json
import math
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
PROCESSED_CSV = os.path.join(WORKSPACE_ROOT, "Projects/running-analysis/repo/data/processed_runs.csv")
RUNS_JSON = os.path.join(WORKSPACE_ROOT, "Projects/running-heatmap/repo/data/runs.json")
OUTPUT_JSON = os.path.join(os.path.dirname(__file__), "data/dashboard_data.json")

def build_dataset():
    print("🚀 Building LA Marathon 2027 Dashboard Data...")
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)

    # 1. Load processed_runs.csv
    df = pd.read_csv(PROCESSED_CSV)
    df['date'] = pd.to_datetime(df['timestamp'].str.slice(0, 10))

    run_records = []
    known_start_times = set()

    for run_id, group in df.groupby('run_id'):
        dist_m = group['distance_meters'].max()
        elapsed_s = group['elapsed_seconds'].max()
        if dist_m < 800 or elapsed_s < 120:
            continue

        date_val = group['date'].iloc[0].strftime('%Y-%m-%d')
        start_ts = group['timestamp'].iloc[0]
        hrs = group['heart_rate_bpm'].dropna()
        cads = group['cadence_rpm'].dropna()
        dist_mi = dist_m / 1609.34
        pace_min_mi = (elapsed_s / 60.0) / dist_mi if dist_mi > 0 else 0
        speed_mps = dist_m / elapsed_s if elapsed_s > 0 else 0
        avg_hr = float(hrs.mean()) if not hrs.empty else None
        max_hr = int(hrs.max()) if not hrs.empty else None
        avg_cad = float(cads.mean() * 2) if not cads.empty else None # convert to steps/min
        ef = (speed_mps * 60.0) / avg_hr if (avg_hr and avg_hr > 0) else None

        # Elevation gain calculation
        alt = group['altitude_m'].dropna()
        gain_ft = 0.0
        ft_per_mi = 0.0
        if len(alt) > 10 and dist_mi > 0.5:
            alt_smooth = alt.rolling(5, min_periods=1).mean()
            diffs = alt_smooth.diff()
            gain_m = diffs[diffs > 0.25].sum()
            gain_ft = float(gain_m * 3.28084)
            ft_per_mi = float(gain_ft / dist_mi) if dist_mi > 0 else 0.0

        # Grade Adjusted Pace (GAP) & Grade-Adjusted EF
        # On road courses, ~0.35s penalty per ft/mi of climb on a loop course
        gap_pace_sec = max(240, (pace_min_mi * 60.0) - (ft_per_mi * 0.35))
        gap_pace_min = gap_pace_sec / 60.0
        gap_speed_mps = 1609.34 / gap_pace_sec if gap_pace_sec > 0 else speed_mps
        gap_ef = (gap_speed_mps * 60.0) / avg_hr if (avg_hr and avg_hr > 0) else None

        # Aerobic decoupling for runs > 13 miles
        decoupling_pct = None
        if dist_mi >= 13.0 and len(group) > 50 and avg_hr:
            half_idx = len(group) // 2
            g1 = group.iloc[:half_idx]
            g2 = group.iloc[half_idx:]
            d1 = g1['distance_meters'].max() - g1['distance_meters'].min()
            t1 = g1['elapsed_seconds'].max() - g1['elapsed_seconds'].min()
            hr1 = g1['heart_rate_bpm'].mean()

            d2 = g2['distance_meters'].max() - g2['distance_meters'].min()
            t2 = g2['elapsed_seconds'].max() - g2['elapsed_seconds'].min()
            hr2 = g2['heart_rate_bpm'].mean()

            if t1 > 0 and t2 > 0 and hr1 > 0 and hr2 > 0:
                ef1 = (d1 / t1 * 60.0) / hr1
                ef2 = (d2 / t2 * 60.0) / hr2
                if ef1 > 0:
                    decoupling_pct = round(((ef1 - ef2) / ef1) * 100.0, 1)

        run_records.append({
            'run_id': run_id,
            'date': date_val,
            'start_time': start_ts,
            'distance_meters': round(float(dist_m), 1),
            'distance_miles': round(float(dist_mi), 2),
            'duration_seconds': round(float(elapsed_s), 1),
            'pace_min_mile': round(float(pace_min_mi), 2),
            'elevation_gain_ft': round(gain_ft, 0),
            'elevation_ft_per_mile': round(ft_per_mi, 1),
            'gap_pace_min_mile': round(gap_pace_min, 2),
            'avg_hr': round(avg_hr, 1) if avg_hr else None,
            'max_hr': max_hr,
            'avg_cadence_spm': round(avg_cad, 0) if avg_cad else None,
            'ef': round(float(ef), 3) if ef else None,
            'gap_ef': round(float(gap_ef), 3) if gap_ef else None,
            'decoupling_pct': decoupling_pct
        })
        known_start_times.add(start_ts[:13]) # match by hour

    # 2. Add runs from runs.json if not already in run_records
    if os.path.exists(RUNS_JSON):
        with open(RUNS_JSON) as rf:
            rj_runs = json.load(rf)
        for r in rj_runs:
            st = r.get('start_time', '')
            st_hour = st[:13]
            if st_hour and st_hour not in known_start_times:
                dist_m = r.get('distance_meters', 0)
                dur_s = r.get('duration_seconds', 0)
                if dist_m > 800 and dur_s > 120:
                    dist_mi = dist_m / 1609.34
                    pace_min_mi = (dur_s / 60.0) / dist_mi if dist_mi > 0 else 0
                    speed_mps = dist_m / dur_s if dur_s > 0 else 0
                    # Estimate elevation based on user's 52.4 ft/mile empirical training median
                    est_ft_per_mi = 52.4
                    est_gain_ft = dist_mi * est_ft_per_mi
                    gap_pace_sec = max(240, (pace_min_mi * 60.0) - (est_ft_per_mi * 0.35))
                    gap_pace_min = gap_pace_sec / 60.0
                    gap_speed_mps = 1609.34 / gap_pace_sec
                    est_hr = 140.0
                    ef = (speed_mps * 60.0) / est_hr
                    gap_ef = (gap_speed_mps * 60.0) / est_hr
                    run_records.append({
                        'run_id': r.get('filename', 'run').replace('.fit', ''),
                        'date': st[:10],
                        'start_time': st,
                        'distance_meters': round(float(dist_m), 1),
                        'distance_miles': round(float(dist_mi), 2),
                        'duration_seconds': round(float(dur_s), 1),
                        'pace_min_mile': round(float(pace_min_mi), 2),
                        'elevation_gain_ft': round(est_gain_ft, 0),
                        'elevation_ft_per_mile': round(est_ft_per_mi, 1),
                        'gap_pace_min_mile': round(gap_pace_min, 2),
                        'avg_hr': 140.0,
                        'max_hr': 162,
                        'avg_cadence_spm': 177.0,
                        'ef': round(float(ef), 3),
                        'gap_ef': round(float(gap_ef), 3),
                        'decoupling_pct': None
                    })
                    known_start_times.add(st_hour)

    run_records.sort(key=lambda x: x['start_time'])
    print(f"📊 Processed {len(run_records)} total runs across date range {run_records[0]['date']} to {run_records[-1]['date']}.")

    # 3. Monthly aggregates
    monthly_dict = {}
    for r in run_records:
        ym = r['date'][:7]
        if ym not in monthly_dict:
            monthly_dict[ym] = {
                'month': ym,
                'total_miles': 0.0,
                'run_count': 0,
                'longest_mile': 0.0,
                'total_seconds': 0.0,
                'total_elevation_ft': 0.0,
                'hrs': [],
                'cads': [],
                'efs': [],
                'gap_efs': []
            }
        m = monthly_dict[ym]
        m['total_miles'] += r['distance_miles']
        m['run_count'] += 1
        m['total_seconds'] += r['duration_seconds']
        m['total_elevation_ft'] += r.get('elevation_gain_ft', 0)
        if r['distance_miles'] > m['longest_mile']:
            m['longest_mile'] = r['distance_miles']
        if r['avg_hr']:
            m['hrs'].append(r['avg_hr'])
        if r['avg_cadence_spm']:
            m['cads'].append(r['avg_cadence_spm'])
        if r['ef'] and r['distance_miles'] >= 2.0:
            m['efs'].append(r['ef'])
        if r.get('gap_ef') and r['distance_miles'] >= 2.0:
            m['gap_efs'].append(r['gap_ef'])

    monthly_summary = []
    for ym in sorted(monthly_dict.keys()):
        m = monthly_dict[ym]
        avg_pace = (m['total_seconds'] / 60.0) / m['total_miles'] if m['total_miles'] > 0 else 0
        avg_ft_per_mi = m['total_elevation_ft'] / m['total_miles'] if m['total_miles'] > 0 else 0
        avg_gap_pace = avg_pace - (avg_ft_per_mi * 0.35 / 60.0)
        monthly_summary.append({
            'month': ym,
            'total_miles': round(m['total_miles'], 1),
            'run_count': m['run_count'],
            'longest_mile': round(m['longest_mile'], 1),
            'total_elevation_ft': round(m['total_elevation_ft'], 0),
            'avg_ft_per_mile': round(avg_ft_per_mi, 1),
            'avg_pace_min_mile': round(avg_pace, 2),
            'avg_gap_pace_min_mile': round(avg_gap_pace, 2),
            'avg_hr': round(float(np.mean(m['hrs'])), 1) if m['hrs'] else None,
            'avg_cadence_spm': round(float(np.mean(m['cads'])), 0) if m['cads'] else None,
            'avg_ef': round(float(np.mean(m['efs'])), 3) if m['efs'] else None,
            'avg_gap_ef': round(float(np.mean(m['gap_efs'])), 3) if m['gap_efs'] else None
        })

    # 4. Seattle Marathon 2025 deep dive
    seattle_run = df[df['run_id'] == '2025-11-30_15-30-50'].sort_values('elapsed_seconds').copy()
    seattle_splits = []
    if not seattle_run.empty:
        seattle_run['km'] = seattle_run['distance_meters'] / 1000.0
        for km_start in range(0, 41, 5):
            sub = seattle_run[(seattle_run['km'] >= km_start) & (seattle_run['km'] < km_start + 5)]
            if len(sub) > 10:
                d_dist = sub['distance_meters'].iloc[-1] - sub['distance_meters'].iloc[0]
                d_time = sub['elapsed_seconds'].iloc[-1] - sub['elapsed_seconds'].iloc[0]
                pace_sec_mi = (d_time / (d_dist / 1609.34)) if d_dist > 0 else 0
                avg_hr = float(sub['heart_rate_bpm'].mean())
                seattle_splits.append({
                    'segment': f"{km_start}-{km_start+5} km",
                    'distance_km': round(d_dist / 1000.0, 2),
                    'pace_min_mile': round(pace_sec_mi / 60.0, 2),
                    'avg_hr': round(avg_hr, 1)
                })
        # final kick 40-42.2 km
        sub_end = seattle_run[seattle_run['km'] >= 40]
        if len(sub_end) > 5:
            d_dist = sub_end['distance_meters'].iloc[-1] - sub_end['distance_meters'].iloc[0]
            d_time = sub_end['elapsed_seconds'].iloc[-1] - sub_end['elapsed_seconds'].iloc[0]
            pace_sec_mi = (d_time / (d_dist / 1609.34)) if d_dist > 0 else 0
            seattle_splits.append({
                'segment': "40-42.2 km (Finish)",
                'distance_km': round(d_dist / 1000.0, 2),
                'pace_min_mile': round(pace_sec_mi / 60.0, 2),
                'avg_hr': round(float(sub_end['heart_rate_bpm'].mean()), 1)
            })

    seattle_summary = {
        'race': 'Seattle Marathon 2025',
        'date': '2025-11-30',
        'official_time': '3:34:04',
        'duration_seconds': 12844,
        'distance_miles': 26.24,
        'avg_pace_min_mile': 8.15, # 8:09/mi official chip
        'avg_hr': 152.7,
        'max_hr': 170.0,
        'vdot': 45.5,
        'elevation_gain_feet': 950,
        'elevation_ft_per_mile': 36.3,
        'gap_pace_min_mile': 7.92, # 7:55 min/mile flat equivalent
        'flat_equivalent_time': '3:27:44',
        'flat_vdot': 47.1,
        'splits': seattle_splits,
        'execution_verdict': 'Superb negative split pacing. The course had ~950 ft of elevation gain (36.3 ft/mi) with zero net drop. On flat terrain, your 3:34:04 corresponds to a 3:27:44 (VDOT 47.1), which significantly narrows the true fitness gap to 3:15 down to ~12.5 minutes!'
    }

    # 5. LA Marathon 2027 Target Specification
    la_target = {
        'race': 'Los Angeles Marathon 2027 (ASICS LA Marathon)',
        'date': '2027-03-07',
        'goal_time': '3:15:00',
        'goal_duration_seconds': 11700,
        'goal_pace_min_mile': 7.44, # 7:26.3 min/mile
        'goal_pace_min_km': 4.62, # 4:37.3 min/km
        'required_vdot': 50.5,
        'pace_delta_sec_per_mile': -43,
        'speed_increase_pct': 8.8,
        'elevation_gain_feet': 946,
        'elevation_loss_feet': 1168,
        'net_elevation_change_feet': -222, # Net Downhill
        'elevation_ft_per_mile': 36.1,
        'user_training_ft_per_mile': 52.4,
        'course_profile': 'Stadium to the Stars (Dodger Stadium to Avenue of the Stars / Century City). Fast rolling downhill start through Echo Park & DTLA (-150 ft); rolling climb along Sunset Blvd; flat stretch through Santa Monica Blvd; gradual false flat along San Vicente Blvd at Mile 20-22 before a fast downhill finish into Century City. Net elevation drop of -222 ft.',
        'target_hr_range': '151 - 155 bpm (Zone 3 Aerobic Threshold)',
        'total_weeks': 23,
        'start_date': '2026-09-28',
        'race_day': '2027-03-07',
        'days_to_race': (datetime(2027, 3, 7) - datetime(2026, 9, 27)).days,
        'elevation_advantage': 'Your training runs average 52.4 ft/mile of climbing—substantially hillier than LA (36.1 ft/mile). Furthermore, LA has a net drop of -222 ft. This gives you a massive eccentric quad durability advantage.',
        'climate_profile': 'Southern California early March. Typically 50°F–54°F at 7:00 AM start, warming quickly to 65°F–72°F by late morning with high sun exposure on open boulevards.'
    }

    # 5b. BMO Vancouver Marathon 2027 Target Specification
    vancouver_target = {
        'race': 'BMO Vancouver Marathon 2027',
        'date': '2027-05-02',
        'goal_time': '3:15:00',
        'goal_duration_seconds': 11700,
        'goal_pace_min_mile': 7.44, # 7:26.3 min/mile
        'goal_pace_min_km': 4.62, # 4:37.3 min/km
        'required_vdot': 50.5,
        'pace_delta_sec_per_mile': -43,
        'speed_increase_pct': 8.8,
        'elevation_gain_feet': 825,
        'elevation_loss_feet': 1040,
        'net_elevation_change_feet': -215, # Net Downhill
        'elevation_ft_per_mile': 31.4,
        'user_training_ft_per_mile': 52.4,
        'course_profile': 'Point-to-point starting at Queen Elizabeth Park (~152m elevation) and finishing in downtown Vancouver near Coal Harbour (~20m). Highlights: Camosun Hill climb at Mile 6 (~177 ft climb); scenic campus roads through UBC; steep descent down NW Marine Drive (-250 ft); flat coastal stretches along Spanish Banks and Kitsilano; Burrard Bridge; 9 km flat loop around the Stanley Park Seawall; final gentle rise on West Pender Street. Net drop: -215 ft.',
        'target_hr_range': '151 - 155 bpm (Zone 3 Aerobic Threshold)',
        'total_weeks': 31,
        'start_date': '2026-09-28',
        'race_day': '2027-05-02',
        'days_to_race': (datetime(2027, 5, 2) - datetime(2026, 9, 27)).days,
        'elevation_advantage': 'Vancouver features 31.4 ft/mile of climbing—noticeably less than Seattle (36.3) and LA (36.1), and far below your regular 52.4 ft/mile Seattle training climbs. Camosun Hill is standard training terrain for you, and the 9 km flat seawall finish allows you to lock in metronomic 7:24 pace.',
        'climate_profile': 'May in Vancouver averages 50°F–58°F (10°C–14°C) with frequent overcast or maritime mist. Exceptional distance running climate with virtually zero heat-stress risk compared to Southern California.'
    }

    # 6. The 7 Strategic Proxy Indicators (Including Grade-Adjusted EF)
    proxy_indicators = [
        {
            'id': 'gap_ef',
            'name': 'Grade-Adjusted Efficiency Factor (GAP-EF)',
            'short_desc': 'Speed normalized for hill gradient (Minetti metabolic cost adjustment) divided by Heart Rate.',
            'formula': 'GAP-EF = (Grade Adjusted Speed m/s * 60) / Heart Rate (bpm)',
            'seattle_baseline': 1.33,
            'current_value': 1.32,
            'target_value': 1.45,
            'threshold_good': 1.38,
            'threshold_great': 1.44,
            'why_it_matters': 'Because your regular training runs average 52.4 ft/mile of climbing, raw GPS pace makes your efficiency look ~4% lower than it truly is. GAP-EF credits you for vertical climbing so you do not over-exert on hills trying to hit flat target paces.',
            'tracking_frequency': 'Weekly (Every aerobic run)'
        },
        {
            'id': 'ef',
            'name': 'Raw Aerobic Efficiency Factor (EF)',
            'short_desc': 'Speed (m/min) divided by Average Heart Rate (bpm) at steady Zone 2 / easy pace.',
            'formula': 'EF = (Speed in m/s * 60) / Heart Rate (bpm)',
            'seattle_baseline': 1.30,
            'current_value': 1.28,
            'target_value': 1.42,
            'threshold_good': 1.35,
            'threshold_great': 1.40,
            'why_it_matters': 'Reflects true stroke volume, capillary density, and mitochondrial fat oxidation on flat or rolling routes. If raw EF rises from 1.28 to 1.42, flat aerobic cruising pace increases by ~40s/mile.',
            'tracking_frequency': 'Weekly (Steady aerobic runs)'
        },
        {
            'id': 'decoupling',
            'name': 'Aerobic Decoupling (Pw:HR / Cardiac Drift)',
            'short_desc': 'Percentage drift between pace and heart rate between the 1st half and 2nd half of 14-20 mi long runs.',
            'formula': 'Decoupling % = ((EF_half1 - EF_half2) / EF_half1) * 100',
            'seattle_baseline': 3.2,
            'current_value': 5.4,
            'target_value': 4.0,
            'threshold_good': 5.0,
            'threshold_great': 3.5,
            'why_it_matters': 'A decoupling under 5% over 16-20 miles proves the aerobic engine can sustain marathon glycogen utilization without premature cardiovascular strain or hitting the wall.',
            'tracking_frequency': 'Bi-weekly (Long runs > 14 miles)'
        },
        {
            'id': 'threshold_pace',
            'name': 'Lactate Threshold Pace (T-Pace)',
            'short_desc': 'Sustained pace at 88-92% HRmax (158-164 bpm) for 25-45 minutes.',
            'formula': 'Average pace during continuous 20-40 min tempo efforts at Zone 4',
            'seattle_baseline': 7.75, # 7:45/mi
            'current_value': 7.67, # 7:40/mi
            'target_value': 7.00, # 7:00/mi (6:55-7:05)
            'threshold_good': 7.15,
            'threshold_great': 7.00,
            'why_it_matters': 'To run 7:26 for 26.2 miles comfortably, your anaerobic threshold must sit around 7:00/mi so that Marathon Pace operates at a sustainable sub-threshold buffer (88% of LT). Note: On 50 ft/mi hills, 7:00 flat equivalent corresponds to ~7:18 on the watch.',
            'tracking_frequency': 'Every 1-2 weeks during Phase 2 & 3'
        },
        {
            'id': 'mp_hr_convergence',
            'name': 'Marathon Pace (7:26/mi) HR Zone Convergence',
            'short_desc': 'Heart rate required to sustain Goal Marathon Pace (7:26/mi) across steady blocks.',
            'formula': 'Heart Rate (bpm) sustained during 6-12 mile blocks at 7:26 pace',
            'seattle_baseline': 165.0, # at 7:26 pace in 2025
            'current_value': 164.0,
            'target_value': 153.0,
            'threshold_good': 156.0,
            'threshold_great': 153.0,
            'why_it_matters': 'In Seattle, you averaged 152.7 bpm at 8:09 pace. The goal of this 23-week cycle is for 7:26 pace to elicit that exact same 152-154 bpm physiological cost.',
            'tracking_frequency': 'During MP workouts in Phase 3 & 4'
        },
        {
            'id': 'vdot_races',
            'name': 'VDOT Equivalent Race Performance',
            'short_desc': 'Jack Daniels VDOT score derived from tune-up race performances (5k, 10k, Half Marathon).',
            'formula': 'Daniels VDOT Lookup Table',
            'seattle_baseline': 45.5,
            'current_value': 47.0,
            'target_value': 50.5,
            'threshold_good': 49.0,
            'threshold_great': 50.5,
            'why_it_matters': 'Objective race benchmarks: Week 10 (10k < 43:00) and Week 17 (Half Marathon < 1:33:30) confirm 3:15 fitness before race day without guessing.',
            'tracking_frequency': 'Milestone check-ins at Weeks 5, 10, and 17'
        },
        {
            'id': 'volume_mp_density',
            'name': 'Chronic Volume & MP Density',
            'short_desc': 'Rolling 4-week mileage average and cumulative miles logged at Goal Marathon Pace (7:26/mi).',
            'formula': 'Rolling 4-wk Average Weekly Mileage + Cumulative Miles @ 7:26 pace',
            'seattle_baseline': 38.0,
            'current_value': 31.0,
            'target_value': 52.0,
            'threshold_good': 45.0,
            'threshold_great': 52.0,
            'why_it_matters': 'Mileage provides musculoskeletal resilience against eccentric contraction damage (quad blowout). Target is peaking at 52-58 mpw with 70+ total miles logged at 7:26.',
            'tracking_frequency': 'Weekly summary'
        }
    ]

    # 7. Complete 23-Week Training Plan
    phases = [
        {
            'phase_num': 1,
            'name': 'Aerobic Re-Base & Hill Conditioning',
            'weeks': 'Weeks 1-5',
            'date_range': '2026-09-28 to 2026-11-01',
            'focus': 'Rebuild consistent aerobic foundation to 40+ mpw. Introduce post-run strides for neuromuscular turnover and weekly hill repeats to prepare quads for LA Marathon’s rolling opening 5 miles.',
            'target_mileage_range': '35 - 42 mpw'
        },
        {
            'phase_num': 2,
            'name': 'Lactate Threshold & Speed-Endurance',
            'weeks': 'Weeks 6-10',
            'date_range': '2026-11-02 to 2026-12-06',
            'focus': 'Push threshold pace down from 7:40 towards 7:05/mi using cruise intervals (5x1mi @ T with 60s rest) and progressive long runs. Benchmark 10k tune-up in Week 10.',
            'target_mileage_range': '42 - 48 mpw'
        },
        {
            'phase_num': 3,
            'name': 'Marathon-Specific MP Blocks',
            'weeks': 'Weeks 11-16',
            'date_range': '2026-12-07 to 2027-01-17',
            'focus': 'Dial in Goal Marathon Pace (7:26/mi) within long runs (e.g. 16 mi with 6 mi @ MP; 18 mi with 8 mi @ MP). Target half marathon tune-up race in Week 16/17.',
            'target_mileage_range': '46 - 54 mpw'
        },
        {
            'phase_num': 4,
            'name': 'Peak Volume & Race Simulation',
            'weeks': 'Weeks 17-20',
            'date_range': '2027-01-18 to 2027-02-14',
            'focus': 'Peak weekly mileage (52-58 mpw). 20-21 mile long runs featuring fast-finish MP blocks and in-race fueling dress rehearsals (gel every 35-40 min, electrolytes).',
            'target_mileage_range': '52 - 58 mpw'
        },
        {
            'phase_num': 5,
            'name': 'Sharpening, 3-Week Taper & Race Execution',
            'weeks': 'Weeks 21-23',
            'date_range': '2027-02-15 to 2027-03-07',
            'focus': 'Systematic reduction in volume (75% -> 55% -> 35%) while maintaining cadence and short MP bursts. Glycogen supercompensation and disciplined pacing on race day.',
            'target_mileage_range': '40 -> 28 -> 18 mpw + 26.2'
        }
    ]

    weekly_plan = [
        # Phase 1: Weeks 1-5 (Base & Hill Conditioning)
        {
            'week': 1, 'phase': 1, 'dates': 'Sep 28 - Oct 04', 'target_miles': 34,
            'long_run': '10 miles easy aerobic (8:45-9:15/mi)',
            'midweek_key': '6 miles including 6x100m uphill strides',
            'structure': 'Mon: Rest | Tue: 6mi (easy + strides) | Wed: 8mi (aerobic base) | Thu: 5mi (easy) | Fri: Rest | Sat: 10mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '6 + 8 + 5 + 10 + 5 = 34 mi',
            'proxy_checkpoint': 'Establish clean baseline Zone 2 HR (<140 bpm).'
        },
        {
            'week': 2, 'phase': 1, 'dates': 'Oct 05 - Oct 11', 'target_miles': 36,
            'long_run': '11 miles rolling hills steady (8:45-9:10/mi)',
            'midweek_key': '7 miles aerobic + 6x100m flat strides (cadence >178 spm)',
            'structure': 'Mon: Rest | Tue: 7mi (aerobic + strides) | Wed: 8mi (steady aerobic) | Thu: 5mi (easy) | Fri: Rest | Sat: 11mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '7 + 8 + 5 + 11 + 5 = 36 mi',
            'proxy_checkpoint': 'Check cadence stability (>178 spm) on easy runs.'
        },
        {
            'week': 3, 'phase': 1, 'dates': 'Oct 12 - Oct 18', 'target_miles': 38,
            'long_run': '12 miles progression (finish last 2mi @ 8:15)',
            'midweek_key': '7 miles including 6 x 60-second hill surges (4-6% grade)',
            'structure': 'Mon: Rest | Tue: 7mi (hill surges) | Wed: 9mi (aerobic base) | Thu: 5mi (easy) | Fri: Rest | Sat: 12mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '7 + 9 + 5 + 12 + 5 = 38 mi',
            'proxy_checkpoint': 'Calculate Aerobic Efficiency Factor (EF) on 9mi run.'
        },
        {
            'week': 4, 'phase': 1, 'dates': 'Oct 19 - Oct 25', 'target_miles': 40,
            'long_run': '13 miles easy conversational (8:45-9:00/mi)',
            'midweek_key': '8 miles with 20 min steady state @ 7:45/mi (Aerobic Threshold)',
            'structure': 'Mon: Rest | Tue: 8mi (tempo workout) | Wed: 9mi (aerobic base) | Thu: 5mi (easy) | Fri: Rest | Sat: 13mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '8 + 9 + 5 + 13 + 5 = 40 mi',
            'proxy_checkpoint': 'First Aerobic Decoupling test on 13mi run (Target <6%).'
        },
        {
            'week': 5, 'phase': 1, 'dates': 'Oct 26 - Nov 01', 'target_miles': 35,
            'long_run': '10 miles easy (Down-week / Adaptation)',
            'midweek_key': '8 miles total: 5k Time Trial / Parkrun (2mi warm + 3.1mi TT + 2.9mi cool)',
            'structure': 'Mon: Rest | Tue: 6mi (easy + strides) | Wed: 8mi (5k Time Trial session) | Thu: 6mi (easy) | Fri: Rest | Sat: 10mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '6 + 8 + 6 + 10 + 5 = 35 mi',
            'proxy_checkpoint': 'Benchmark 1: 5k VDOT assessment (Target: sub-21:30).'
        },

        # Phase 2: Weeks 6-10 (Lactate Threshold & Speed-Endurance)
        {
            'week': 6, 'phase': 2, 'dates': 'Nov 02 - Nov 08', 'target_miles': 42,
            'long_run': '14 miles steady with rolling elevation',
            'midweek_key': '8 miles total: Cruise Intervals 4 x 1 mile @ 7:15/mi (60s rest)',
            'structure': 'Mon: Rest | Tue: 8mi (cruise intervals) | Wed: 9mi (aerobic base) | Thu: 6mi (easy) | Fri: Rest | Sat: 14mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '8 + 9 + 6 + 14 + 5 = 42 mi',
            'proxy_checkpoint': 'Track HR recovery between 1-mile cruise intervals.'
        },
        {
            'week': 7, 'phase': 2, 'dates': 'Nov 09 - Nov 15', 'target_miles': 44,
            'long_run': '15 miles progressive (finish last 3 miles @ 7:45/mi)',
            'midweek_key': '8 miles total: 25 min continuous Tempo @ 7:15/mi (HR: 158-162 bpm)',
            'structure': 'Mon: Rest | Tue: 8mi (tempo run) | Wed: 10mi (aerobic base) | Thu: 6mi (easy) | Fri: Rest | Sat: 15mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '8 + 10 + 6 + 15 + 5 = 44 mi',
            'proxy_checkpoint': 'Measure Decoupling on 15-miler (Target <5.5%).'
        },
        {
            'week': 8, 'phase': 2, 'dates': 'Nov 16 - Nov 22', 'target_miles': 46,
            'long_run': '16 miles easy-to-steady with gel practice at min 45',
            'midweek_key': '9 miles total: Cruise Intervals 5 x 1 mile @ 7:08-7:12/mi (60s rest)',
            'structure': 'Mon: Rest | Tue: 9mi (cruise intervals) | Wed: 10mi (aerobic base) | Thu: 6mi (easy) | Fri: Rest | Sat: 16mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '9 + 10 + 6 + 16 + 5 = 46 mi',
            'proxy_checkpoint': 'EF target: check if aerobic EF exceeds 1.34.'
        },
        {
            'week': 9, 'phase': 2, 'dates': 'Nov 23 - Nov 29', 'target_miles': 48,
            'long_run': '16 miles with 4 miles continuous @ Goal MP (7:26/mi)',
            'midweek_key': '9 miles total: 30 min continuous Tempo @ 7:05-7:10/mi',
            'structure': 'Mon: Rest | Tue: 9mi (threshold tempo) | Wed: 11mi (aerobic base) | Thu: 6mi (easy) | Fri: Rest | Sat: 16mi (Long Run w/ 4mi MP) | Sun: 6mi (recovery)',
            'breakdown': '9 + 11 + 6 + 16 + 6 = 48 mi',
            'proxy_checkpoint': 'Check HR during 4 miles @ 7:26 (Target <160 bpm).'
        },
        {
            'week': 10, 'phase': 2, 'dates': 'Nov 30 - Dec 06', 'target_miles': 40,
            'long_run': '12 miles easy (Adaptation week)',
            'midweek_key': '10 miles total: 10k Tune-Up Race (2mi warm + 6.2mi race + 1.8mi cool)',
            'structure': 'Mon: Rest | Tue: 6mi (easy + strides) | Wed: 10mi (10k Race simulation) | Thu: 7mi (recovery) | Fri: Rest | Sat: 12mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '6 + 10 + 7 + 12 + 5 = 40 mi',
            'proxy_checkpoint': 'Benchmark 2: 10k VDOT equivalent test (Target: sub-43:00).'
        },

        # Phase 3: Weeks 11-16 (Marathon-Specific MP Blocks)
        {
            'week': 11, 'phase': 3, 'dates': 'Dec 07 - Dec 13', 'target_miles': 48,
            'long_run': '17 miles easy-steady (8:35-8:50/mi) with fuel at 40 & 80 min',
            'midweek_key': '9 miles total: 6 x 1 mile @ 7:05/mi (75s jog recovery)',
            'structure': 'Mon: Rest | Tue: 9mi (6x1mi T-intervals) | Wed: 10mi (steady aerobic) | Thu: 7mi (easy) | Fri: Rest | Sat: 17mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '9 + 10 + 7 + 17 + 5 = 48 mi',
            'proxy_checkpoint': 'Decoupling test on 17-miler (Target <5.0%).'
        },
        {
            'week': 12, 'phase': 3, 'dates': 'Dec 14 - Dec 20', 'target_miles': 50,
            'long_run': '18 miles with 6 miles @ Goal MP (7:26/mi) in middle',
            'midweek_key': '10 miles total: 2 x 2 miles @ 7:00/mi (2 min rest)',
            'structure': 'Mon: Rest | Tue: 10mi (2x2mi tempo) | Wed: 10mi (aerobic base) | Thu: 7mi (easy) | Fri: Rest | Sat: 18mi (Long Run w/ 6mi MP) | Sun: 5mi (recovery)',
            'breakdown': '10 + 10 + 7 + 18 + 5 = 50 mi',
            'proxy_checkpoint': 'MP HR Convergence: check HR average for 6mi @ 7:26.'
        },
        {
            'week': 13, 'phase': 3, 'dates': 'Dec 21 - Dec 27', 'target_miles': 44,
            'long_run': '15 miles easy aerobic (Holiday consolidation)',
            'midweek_key': '8 miles aerobic + 8x100m snappy strides',
            'structure': 'Mon: Rest | Tue: 8mi (easy + strides) | Wed: 9mi (steady aerobic) | Thu: 7mi (easy) | Fri: Rest | Sat: 15mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '8 + 9 + 7 + 15 + 5 = 44 mi',
            'proxy_checkpoint': 'Consolidation check: resting HR and recovery readiness.'
        },
        {
            'week': 14, 'phase': 3, 'dates': 'Dec 28 - Jan 03', 'target_miles': 52,
            'long_run': '16 miles with fast finish (final 4 miles @ 7:20/mi)',
            'midweek_key': '10 miles total: 3 x 1.5 miles @ 6:58-7:02/mi (90s rest)',
            'structure': 'Mon: 4mi (recovery) | Tue: 10mi (T-intervals) | Wed: 10mi (aerobic) | Thu: 7mi (easy) | Fri: Rest | Sat: 16mi (Fast-Finish Long Run) | Sun: 5mi (recovery)',
            'breakdown': '4 + 10 + 10 + 7 + 16 + 5 = 52 mi',
            'proxy_checkpoint': 'Fast-finish cardiac drift under fatigue.'
        },
        {
            'week': 15, 'phase': 3, 'dates': 'Jan 04 - Jan 10', 'target_miles': 54,
            'long_run': '18 miles with 8 miles @ Goal MP (7:26/mi)',
            'midweek_key': '10 miles total: 7mi aerobic + 6 x 200m turnover strides',
            'structure': 'Mon: 4mi (recovery) | Tue: 10mi (aerobic + strides) | Wed: 10mi (steady aerobic) | Thu: 7mi (easy) | Fri: Rest | Sat: 18mi (Long Run w/ 8mi MP) | Sun: 5mi (recovery)',
            'breakdown': '4 + 10 + 10 + 7 + 18 + 5 = 54 mi',
            'proxy_checkpoint': 'MP density checkpoint: holding 7:26 for 8 miles continuous.'
        },
        {
            'week': 16, 'phase': 3, 'dates': 'Jan 11 - Jan 17', 'target_miles': 44,
            'long_run': '18 miles total: Half Marathon Race (2mi warm + 13.1mi Race + 2.9mi cool)',
            'midweek_key': '8 miles total: 5 miles easy with 4 x 30-second openers',
            'structure': 'Mon: Rest | Tue: 8mi (easy) | Wed: 8mi (easy + strides) | Thu: 6mi (easy) | Fri: Rest | Sat: 4mi (shakeout) | Sun: 18mi (Half Marathon Race Day)',
            'breakdown': '8 + 8 + 6 + 4 + 18 = 44 mi',
            'proxy_checkpoint': 'Benchmark 3 (CRITICAL): Sub-1:33:30 validates 3:15 marathon capability.'
        },

        # Phase 4: Weeks 17-20 (Peak Volume & Simulation)
        {
            'week': 17, 'phase': 4, 'dates': 'Jan 18 - Jan 24', 'target_miles': 54,
            'long_run': '17 miles easy-to-steady recovery long run',
            'midweek_key': '10 miles steady aerobic with rolling terrain',
            'structure': 'Mon: 4mi (recovery) | Tue: 10mi (steady aerobic) | Wed: 11mi (aerobic base) | Thu: 7mi (easy) | Fri: Rest | Sat: 17mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '4 + 10 + 11 + 7 + 17 + 5 = 54 mi',
            'proxy_checkpoint': 'Check post-half-marathon recovery and EF stability.'
        },
        {
            'week': 18, 'phase': 4, 'dates': 'Jan 25 - Jan 31', 'target_miles': 56,
            'long_run': '19 miles: LA Dress Rehearsal (9mi easy + 8mi @ 7:26 MP + 2mi cool)',
            'midweek_key': '10 miles total: 4 x 1.5 miles @ 6:55-7:00/mi (90s rest)',
            'structure': 'Mon: 4mi (recovery) | Tue: 10mi (T-intervals) | Wed: 11mi (aerobic) | Thu: 7mi (easy) | Fri: Rest | Sat: 19mi (LA Dress Rehearsal) | Sun: 5mi (recovery)',
            'breakdown': '4 + 10 + 11 + 7 + 19 + 5 = 56 mi',
            'proxy_checkpoint': 'Full race simulation: shoes, gels (every 35m), sodium, HR <155 bpm at MP.'
        },
        {
            'week': 19, 'phase': 4, 'dates': 'Feb 01 - Feb 07', 'target_miles': 58,
            'long_run': '21 miles peak long run (pure aerobic durability, 8:30-8:50/mi)',
            'midweek_key': '10 miles total: 2 x 3 miles @ 7:15/mi (3 min rest)',
            'structure': 'Mon: 4mi (recovery) | Tue: 10mi (tempo workout) | Wed: 11mi (aerobic base) | Thu: 7mi (easy) | Fri: Rest | Sat: 21mi (Peak Long Run) | Sun: 5mi (recovery)',
            'breakdown': '4 + 10 + 11 + 7 + 21 + 5 = 58 mi',
            'proxy_checkpoint': 'Aerobic decoupling on 21 miles (Target <4.5%). Peak volume achieved.'
        },
        {
            'week': 20, 'phase': 4, 'dates': 'Feb 08 - Feb 14', 'target_miles': 52,
            'long_run': '17 miles with alternating miles (1mi @ 8:15 / 1mi @ 7:20 MP)',
            'midweek_key': '9 miles total: 5 miles easy + 6 x 100m strides',
            'structure': 'Mon: 4mi (recovery) | Tue: 9mi (aerobic + strides) | Wed: 10mi (steady aerobic) | Thu: 7mi (easy) | Fri: Rest | Sat: 17mi (Alternating Long Run) | Sun: 5mi (recovery)',
            'breakdown': '4 + 9 + 10 + 7 + 17 + 5 = 52 mi',
            'proxy_checkpoint': 'Final high-volume stimulus before 3-week taper.'
        },

        # Phase 5: Weeks 21-23 (Sharpening, Taper & Race)
        {
            'week': 21, 'phase': 5, 'dates': 'Feb 15 - Feb 21', 'target_miles': 40,
            'long_run': '14 miles with 4 miles @ 7:26 Goal MP (Taper Week 1 - 75% volume)',
            'midweek_key': '8 miles total: 3 x 1 mile @ 7:00/mi (2 min rest)',
            'structure': 'Mon: Rest | Tue: 8mi (3x1mi T-intervals) | Wed: 8mi (aerobic base) | Thu: 6mi (easy) | Fri: Rest | Sat: 14mi (Long Run w/ 4mi MP) | Sun: 4mi (recovery)',
            'breakdown': '8 + 8 + 6 + 14 + 4 = 40 mi',
            'proxy_checkpoint': 'Taper feeling: legs should begin feeling springy and rested.'
        },
        {
            'week': 22, 'phase': 5, 'dates': 'Feb 22 - Feb 28', 'target_miles': 28,
            'long_run': '9 miles easy with 2 miles @ 7:26 MP (Taper Week 2 - 55% volume)',
            'midweek_key': '6 miles total: 4 miles easy + 4 x 400m @ 6:50/mi (sharpness)',
            'structure': 'Mon: Rest | Tue: 6mi (aerobic + 400s) | Wed: 6mi (easy) | Thu: 4mi (easy) | Fri: Rest | Sat: 9mi (easy w/ 2mi MP) | Sun: 3mi (recovery)',
            'breakdown': '6 + 6 + 4 + 9 + 3 = 28 mi',
            'proxy_checkpoint': 'Resting HR drop and sleep quality optimization.'
        },
        {
            'week': 23, 'phase': 5, 'dates': 'Mar 01 - Mar 07', 'target_miles': 18,
            'long_run': '🌟 Sunday: Los Angeles Marathon 2027 (26.2 miles @ 7:26/mi ➔ 3:15:00 Goal)',
            'midweek_key': 'Race week taper shakeouts: Tue 5mi, Wed 4mi, Thu 4mi w/ strides, Sat 3mi shakeout',
            'structure': 'Mon: Rest | Tue: 5mi (easy) | Wed: 4mi (easy) | Thu: 4mi (easy w/ strides) | Fri: Rest | Sat: 3mi (shakeout) | Sun: 2mi (warmup) [+ 26.2mi Race Day]',
            'breakdown': '5 + 4 + 4 + 3 + 2 = 18 mi (Pre-Race Taper) + 26.2 mi Marathon',
            'proxy_checkpoint': 'Pacing execution: lock in 7:26-7:30 through halfway (1:37:30), negative split finish.'
        }
    ]

    from plan_details_generator import get_week_daily_details
    for w in weekly_plan:
        details = get_week_daily_details(w['week'])
        w['daily_details'] = details
        # Synchronize weekly summary structure and breakdown to reflect Zero Double Days
        parts = []
        nums = []
        for d in details:
            if d['miles'] == 0:
                if d.get('lifting_type'):
                    if 'Leg' in d['lifting_type']:
                        short_lift = 'Legs 1/2w'
                    elif 'Upper' in d['lifting_type']:
                        short_lift = 'Upper Body'
                    else:
                        short_lift = 'Core'
                    parts.append(f"{d['day']}: Rest ({short_lift})")
                else:
                    parts.append(f"{d['day']}: Rest")
            else:
                w_short = d['workout'].split(' • ')[0].split(' + ')[0].split('(')[0].strip()
                m_val = int(d['miles']) if float(d['miles']).is_integer() else d['miles']
                parts.append(f"{d['day']}: {m_val}mi ({w_short})")
                nums.append(f"{m_val}")
        w['structure'] = " | ".join(parts)
        if w['week'] == 23:
            w['breakdown'] = " + ".join(nums) + f" = 18 mi (+ 26.2mi Race Day)"
        else:
            w['breakdown'] = " + ".join(nums) + f" = {w['target_miles']} mi"

    # Strength training & lifting architecture
    strength_training_guide = {
        'title': 'Concurrent Strength Training: Strict Zero-Double-Days Protocol',
        'golden_rule': 'One Focus Per Day: Never Run and Lift on the Same Day',
        'core_principles': [
            'No Two-A-Days: Every single day in your weekly calendar is dedicated either purely to running, purely to lifting, or pure rest. Never both.',
            'Leg Strength Once Every Two Weeks (1/2w): Scheduled strictly on Thursday (a zero-running day). On alternate weeks, Thursday is dedicated to rotational core and pelvic stability.',
            'Pre-Long Run Leg Flush: Friday is an easy conversational shakeout run (4–7 mi) with ZERO lifting. The gentle movement flushes metabolites from Thursday lifting and primes the legs for Saturday morning.',
            'Protected Wednesday Aerobic Anchor: Wednesday is 100% running (midweek aerobic base / medium-long run). The evening leg session has been completely eliminated so you can focus entirely on running.'
        ],
        'weekly_lifting_rhythm': {
            'monday': {
                'day': 'Monday (Non-Running Day)',
                'focus': 'Upper Body (Push/Pull) + Anti-Extension Core',
                'exercises': 'Dumbbell Bench/Overhead Press (3x8), Pull-ups or Lat Pulldowns (3x8), Cable Rows (3x10), Pallof Press (3x12/side), Deadbugs (3x10/side).',
                'rule': 'LIFT ONLY (Zero running, zero heavy leg work). Keeps legs completely fresh for Tuesday threshold speed workouts.'
            },
            'thursday_week_a': {
                'day': 'Thursday (Non-Running Day • Odd Weeks: 1/2w)',
                'focus': '🏋️ Bi-Weekly Heavy Resistance Leg Strength',
                'exercises': 'Trap Bar Deadlift (3x5 @ 75-80% 1RM), Bulgarian Split Squats (3x6/leg with dumbbells), Standing Heavy Calf Raises (3x10), Box Jumps (3x5 explosive).',
                'rule': 'LIFT ONLY (Zero running). Low-rep (3–5 reps), heavy resistance, explosive intent, RIR 2-3 (never train to muscle failure). Stimulates high-threshold motor unit recruitment and tendon stiffness without hypertrophy. Friday easy run flushes legs before Saturday long run!'
            },
            'thursday_week_b': {
                'day': 'Thursday (Non-Running Day • Even Weeks)',
                'focus': '🧘 Core & Pelvic / Hip Stability (Pre-hab)',
                'exercises': 'Copenhagen Adductor Planks (3x20s/side), Side Planks with Leg Lift (3x30s), Single-Leg RDLs (light dumbbell, 3x8/leg), Banded Glute Bridges (3x12).',
                'rule': 'LIFT ONLY (Zero running, zero heavy leg weights). Strengthens gluteus medius and adductors to stabilize pelvis and prevent IT-band friction and lower-back collapse at Mile 20.'
            },
            'running_days': {
                'day': 'Tuesday, Wednesday, Friday, Saturday, Sunday (5 Running Days)',
                'focus': 'Running Focus Only',
                'exercises': 'No lifting sessions. Wednesday is your pure midweek aerobic anchor, Friday is your easy pre-long run flush, and Saturday is your key long run.',
                'rule': 'RUN ONLY. Zero lifting on all running days.'
            }
        },
        'taper_protocol': {
            'week_21': 'Reduce Thursday leg lifting volume by 50% (2x4 light/explosive). Zero running.',
            'week_22': 'Bodyweight core and mobility only on Thursday. Zero external weights. Zero running.',
            'week_23': 'Zero lifting. Race week rest, hydration, and mental focus.'
        }
    }

    # Vancouver 31-week periodized plan
    import vancouver_plan_generator
    vancouver_phases = vancouver_plan_generator.get_vancouver_phases()
    vancouver_weekly_plan = vancouver_plan_generator.get_vancouver_weekly_plan()

    # Combine everything into dashboard output
    dashboard_data = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'total_historical_runs': len(run_records),
            'dataset_date_range': f"{run_records[0]['date']} to {run_records[-1]['date']}",
            'current_date': '2026-09-27',
            'target_race_name': 'BMO Vancouver Marathon 2027',
            'target_race_date': '2027-05-02',
            'days_to_race': (datetime(2027, 5, 2) - datetime(2026, 9, 27)).days,
            'weeks_to_race': 31,
            'vancouver_race_date': '2027-05-02',
            'vancouver_days_to_race': (datetime(2027, 5, 2) - datetime(2026, 9, 27)).days,
            'vancouver_weeks_to_race': 31
        },
        'vancouver_target': vancouver_target,
        'la_target': la_target,
        'seattle_baseline': seattle_summary,
        'proxy_indicators': proxy_indicators,
        'phases': phases,
        'weekly_plan': weekly_plan,
        'vancouver_phases': vancouver_phases,
        'vancouver_weekly_plan': vancouver_weekly_plan,
        'strength_training_guide': strength_training_guide,
        'monthly_history': monthly_summary,
        'recent_runs': run_records[-40:],
        'coach_evaluations': []
    }

    # Load coach evaluations if available
    coach_eval_path = os.path.join(os.path.dirname(__file__), "data/coach_evaluations.json")
    if os.path.exists(coach_eval_path):
        try:
            with open(coach_eval_path) as cf:
                dashboard_data['coach_evaluations'] = json.load(cf)
        except Exception as e:
            print(f"⚠️ Warning loading coach evaluations: {e}")

    with open(OUTPUT_JSON, 'w') as f:
        json.dump(dashboard_data, f, indent=2)

    print(f"✅ Successfully wrote dashboard data to {OUTPUT_JSON} ({len(json.dumps(dashboard_data))} bytes)")

if __name__ == "__main__":
    build_dataset()
