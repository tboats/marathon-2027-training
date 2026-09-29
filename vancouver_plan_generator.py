"""
vancouver_plan_generator.py - Comprehensive 31-week periodized training plan
and daily workout details for the BMO Vancouver Marathon 2027 (May 2, 2027).
Target: 3:15:00 (7:26 min/mile / 4:37 min/km)
"""

import os
import sys

from plan_details_generator import apply_lifting_schedule

def get_vancouver_phases():
    return [
        {
            'phase_num': 1,
            'name': 'Aerobic Foundation & Hill Durability',
            'weeks': 'Weeks 1-6',
            'date_range': '2026-09-28 to 2026-11-08',
            'focus': 'Establish consistent aerobic volume (32–40 mpw). Build quad resilience on Seattle rolling terrain to prepare for Vancouver\'s Camosun Hill (Mile 6). Conclude with Benchmark 1 (5k Time Trial).',
            'target_mileage_range': '32 - 40 mpw'
        },
        {
            'phase_num': 2,
            'name': 'Aerobic Base Expansion & Turnover',
            'weeks': 'Weeks 7-12',
            'date_range': '2026-11-09 to 2026-12-20',
            'focus': 'Expand volume safely to 48 mpw. Integrate weekly strides and steady progressive long runs (14–16 mi). Build robust mitochondrial density and lipid oxidation capacity.',
            'target_mileage_range': '42 - 48 mpw'
        },
        {
            'phase_num': 3,
            'name': 'Lactate Threshold & Cruise Intervals',
            'weeks': 'Weeks 13-18',
            'date_range': '2026-12-21 to 2027-01-31',
            'focus': 'Push threshold pace from 7:40 down toward 7:05/mi via 1-mile cruise intervals and tempo runs. Benchmark 2: 10k Tune-Up Race in Week 16 (< 43:00).',
            'target_mileage_range': '42 - 52 mpw'
        },
        {
            'phase_num': 4,
            'name': 'Marathon-Specific MP & Half Marathon Test',
            'weeks': 'Weeks 19-24',
            'date_range': '2027-02-01 to 2027-03-14',
            'focus': 'Embed sustained 6–8 mile blocks at Goal Marathon Pace (7:26/mi). Benchmark 3: Half Marathon Tune-Up Race in Week 22 (sub-1:33:30 target).',
            'target_mileage_range': '48 - 54 mpw'
        },
        {
            'phase_num': 5,
            'name': 'Peak Volume & Vancouver Course Simulation',
            'weeks': 'Weeks 25-28',
            'date_range': '2027-03-15 to 2027-04-11',
            'focus': 'Peak mileage (54–58 mpw). 19–21 mile long runs simulating Camosun climb (early surge), Marine Drive descent (quad control), and flat Seawall metronome pacing.',
            'target_mileage_range': '52 - 58 mpw'
        },
        {
            'phase_num': 6,
            'name': 'Sharpening, 3-Week Taper & Vancouver Race',
            'weeks': 'Weeks 29-31',
            'date_range': '2027-04-12 to 2027-05-02',
            'focus': 'Systematic taper (75% -> 55% -> 35% volume). Full glycogen restoration, fresh legs, and race execution on Sunday, May 2, 2027 for a sub-3:15 finish.',
            'target_mileage_range': '40 -> 28 -> 18 mpw + 26.2'
        }
    ]

def get_vancouver_weekly_plan():
    """
    Returns the complete 31-week plan for Vancouver Marathon 2027.
    Every week's daily running miles mathematically sum to target_miles.
    """
    raw_weeks = [
        # Phase 1: Weeks 1-6 (Foundation & Hills)
        {
            'week': 1, 'phase': 1, 'dates': 'Sep 28 - Oct 04', 'target_miles': 32,
            'long_run': '9 miles easy aerobic (8:50-9:20/mi)',
            'midweek_key': '6 miles including 6 x 100m uphill strides',
            'structure': 'Mon: Rest | Tue: 6mi (easy + strides) | Wed: 7mi (aerobic base) | Thu: 5mi (easy) | Fri: Rest | Sat: 9mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '6 + 7 + 5 + 9 + 5 = 32 mi',
            'proxy_checkpoint': 'Establish clean Zone 2 baseline HR (< 140 bpm).'
        },
        {
            'week': 2, 'phase': 1, 'dates': 'Oct 05 - Oct 11', 'target_miles': 34,
            'long_run': '10 miles rolling hills steady (8:45-9:15/mi)',
            'midweek_key': '6 miles aerobic + 6 x 100m flat strides (>178 spm)',
            'structure': 'Mon: Rest | Tue: 6mi (aerobic + strides) | Wed: 8mi (steady aerobic) | Thu: 5mi (easy) | Fri: Rest | Sat: 10mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '6 + 8 + 5 + 10 + 5 = 34 mi',
            'proxy_checkpoint': 'Cadence check: steady 178+ spm on easy miles.'
        },
        {
            'week': 3, 'phase': 1, 'dates': 'Oct 12 - Oct 18', 'target_miles': 36,
            'long_run': '11 miles progression (finish last 2mi @ 8:20/mi)',
            'midweek_key': '7 miles including 6 x 60-second hill surges (4-6% grade)',
            'structure': 'Mon: Rest | Tue: 7mi (hill surges) | Wed: 8mi (aerobic base) | Thu: 5mi (easy) | Fri: Rest | Sat: 11mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '7 + 8 + 5 + 11 + 5 = 36 mi',
            'proxy_checkpoint': 'Aerobic Efficiency Factor (EF) on 8mi run.'
        },
        {
            'week': 4, 'phase': 1, 'dates': 'Oct 19 - Oct 25', 'target_miles': 38,
            'long_run': '12 miles easy conversational (8:45-9:05/mi)',
            'midweek_key': '7 miles with 20 min steady state @ 7:45/mi (AeT)',
            'structure': 'Mon: Rest | Tue: 7mi (steady tempo) | Wed: 9mi (aerobic base) | Thu: 5mi (easy) | Fri: Rest | Sat: 12mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '7 + 9 + 5 + 12 + 5 = 38 mi',
            'proxy_checkpoint': 'First Aerobic Decoupling test on 12-miler (< 6%).'
        },
        {
            'week': 5, 'phase': 1, 'dates': 'Oct 26 - Nov 01', 'target_miles': 32,
            'long_run': '10 miles easy (Down-week / Adaptation)',
            'midweek_key': '7 miles aerobic + 6 x 100m snappy strides',
            'structure': 'Mon: Rest | Tue: 5mi (easy + strides) | Wed: 7mi (aerobic) | Thu: 5mi (easy) | Fri: Rest | Sat: 10mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '5 + 7 + 5 + 10 + 5 = 32 mi',
            'proxy_checkpoint': 'Resting HR and musculoskeletal recovery check.'
        },
        {
            'week': 6, 'phase': 1, 'dates': 'Nov 02 - Nov 08', 'target_miles': 40,
            'long_run': '13 miles easy-steady rolling hills',
            'midweek_key': '8 miles total: 5k Time Trial (2mi warm + 3.1mi TT + 2.9mi cool)',
            'structure': 'Mon: Rest | Tue: 8mi (5k Time Trial session) | Wed: 9mi (aerobic base) | Thu: 5mi (easy) | Fri: Rest | Sat: 13mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '8 + 9 + 5 + 13 + 5 = 40 mi',
            'proxy_checkpoint': 'Benchmark 1: 5k Time Trial (Target: sub-21:30, VDOT 47.5).'
        },

        # Phase 2: Weeks 7-12 (Aerobic Base Expansion)
        {
            'week': 7, 'phase': 2, 'dates': 'Nov 09 - Nov 15', 'target_miles': 42,
            'long_run': '14 miles steady with rolling elevation',
            'midweek_key': '8 miles total: Cruise Intervals 4 x 1 mile @ 7:15/mi (60s rest)',
            'structure': 'Mon: Rest | Tue: 8mi (cruise intervals) | Wed: 9mi (aerobic base) | Thu: 6mi (easy) | Fri: Rest | Sat: 14mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '8 + 9 + 6 + 14 + 5 = 42 mi',
            'proxy_checkpoint': 'HR recovery rate between 1-mile cruise intervals.'
        },
        {
            'week': 8, 'phase': 2, 'dates': 'Nov 16 - Nov 22', 'target_miles': 44,
            'long_run': '15 miles progressive (finish last 3mi @ 7:50/mi)',
            'midweek_key': '8 miles total: 25 min continuous Tempo @ 7:15/mi (158-162 bpm)',
            'structure': 'Mon: Rest | Tue: 8mi (tempo run) | Wed: 10mi (aerobic base) | Thu: 6mi (easy) | Fri: Rest | Sat: 15mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '8 + 10 + 6 + 15 + 5 = 44 mi',
            'proxy_checkpoint': 'Measure decoupling on 15 miles (Target < 5.5%).'
        },
        {
            'week': 9, 'phase': 2, 'dates': 'Nov 23 - Nov 29', 'target_miles': 42,
            'long_run': '14 miles easy aerobic (Thanksgiving consolidation)',
            'midweek_key': '8 miles aerobic + 8 x 100m flat strides',
            'structure': 'Mon: Rest | Tue: 8mi (aerobic + strides) | Wed: 9mi (steady aerobic) | Thu: 6mi (easy) | Fri: Rest | Sat: 14mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '8 + 9 + 6 + 14 + 5 = 42 mi',
            'proxy_checkpoint': 'Post-run recovery readiness and joint integrity.'
        },
        {
            'week': 10, 'phase': 2, 'dates': 'Nov 30 - Dec 06', 'target_miles': 46,
            'long_run': '16 miles easy-steady with gel practice at min 45',
            'midweek_key': '9 miles total: Cruise Intervals 5 x 1 mile @ 7:10/mi (60s rest)',
            'structure': 'Mon: Rest | Tue: 9mi (cruise intervals) | Wed: 10mi (aerobic base) | Thu: 6mi (easy) | Fri: Rest | Sat: 16mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '9 + 10 + 6 + 16 + 5 = 46 mi',
            'proxy_checkpoint': 'Target: verify raw aerobic EF exceeds 1.34.'
        },
        {
            'week': 11, 'phase': 2, 'dates': 'Dec 07 - Dec 13', 'target_miles': 48,
            'long_run': '16 miles with 4 miles continuous @ Goal MP (7:26/mi)',
            'midweek_key': '9 miles total: 30 min continuous Tempo @ 7:08-7:12/mi',
            'structure': 'Mon: Rest | Tue: 9mi (threshold tempo) | Wed: 11mi (aerobic base) | Thu: 6mi (easy) | Fri: Rest | Sat: 16mi (Long Run w/ 4mi MP) | Sun: 6mi (recovery)',
            'breakdown': '9 + 11 + 6 + 16 + 6 = 48 mi',
            'proxy_checkpoint': 'Check HR during 4 miles @ 7:26 (Target < 160 bpm).'
        },
        {
            'week': 12, 'phase': 2, 'dates': 'Dec 14 - Dec 20', 'target_miles': 44,
            'long_run': '15 miles easy (Pre-Holiday consolidation)',
            'midweek_key': '8 miles aerobic + 6 x 150m gentle accelerations',
            'structure': 'Mon: Rest | Tue: 8mi (easy + strides) | Wed: 9mi (aerobic base) | Thu: 7mi (easy) | Fri: Rest | Sat: 15mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '8 + 9 + 7 + 15 + 5 = 44 mi',
            'proxy_checkpoint': 'Adaptation review: baseline readiness ahead of winter block.'
        },

        # Phase 3: Weeks 13-18 (Lactate Threshold & Speed-Endurance)
        {
            'week': 13, 'phase': 3, 'dates': 'Dec 21 - Dec 27', 'target_miles': 42,
            'long_run': '14 miles easy aerobic (Holiday week)',
            'midweek_key': '8 miles total: 3 x 1.5 miles @ 7:10/mi (90s rest)',
            'structure': 'Mon: Rest | Tue: 8mi (tempo intervals) | Wed: 9mi (aerobic base) | Thu: 6mi (easy) | Fri: Rest | Sat: 14mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '8 + 9 + 6 + 14 + 5 = 42 mi',
            'proxy_checkpoint': 'Consolidation check: maintaining rhythm through holidays.'
        },
        {
            'week': 14, 'phase': 3, 'dates': 'Dec 28 - Jan 03', 'target_miles': 46,
            'long_run': '16 miles steady aerobic (8:35-8:50/mi)',
            'midweek_key': '9 miles total: 6 x 1 mile @ 7:05/mi (75s jog recovery)',
            'structure': 'Mon: Rest | Tue: 9mi (6x1mi T-intervals) | Wed: 10mi (aerobic) | Thu: 6mi (easy) | Fri: Rest | Sat: 16mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '9 + 10 + 6 + 16 + 5 = 46 mi',
            'proxy_checkpoint': 'T-Pace stability: holding 7:05 pace under 163 bpm.'
        },
        {
            'week': 15, 'phase': 3, 'dates': 'Jan 04 - Jan 10', 'target_miles': 48,
            'long_run': '17 miles with 5 miles @ Goal MP (7:26/mi)',
            'midweek_key': '9 miles total: 2 x 2 miles @ 7:00/mi (2 min rest)',
            'structure': 'Mon: Rest | Tue: 9mi (2x2mi tempo) | Wed: 10mi (aerobic base) | Thu: 7mi (easy) | Fri: Rest | Sat: 17mi (Long Run w/ 5mi MP) | Sun: 5mi (recovery)',
            'breakdown': '9 + 10 + 7 + 17 + 5 = 48 mi',
            'proxy_checkpoint': 'Decoupling test on 17-miler (Target < 5.0%).'
        },
        {
            'week': 16, 'phase': 3, 'dates': 'Jan 11 - Jan 17', 'target_miles': 44,
            'long_run': '15 miles total: 10k Tune-Up Race (2.5mi warm + 6.2mi race + 6.3mi long cool)',
            'midweek_key': '6 miles easy with 4 x 30-second strides',
            'structure': 'Mon: Rest | Tue: 6mi (easy + strides) | Wed: 9mi (aerobic) | Thu: 6mi (easy) | Fri: Rest | Sat: 8mi (easy) | Sun: 15mi (10k Tune-up Race Day)',
            'breakdown': '6 + 9 + 6 + 8 + 15 = 44 mi',
            'proxy_checkpoint': 'Benchmark 2: 10k Race sub-43:00 (VDOT 49.0 confirmed!).'
        },
        {
            'week': 17, 'phase': 3, 'dates': 'Jan 18 - Jan 24', 'target_miles': 50,
            'long_run': '18 miles steady with rolling elevation (fuel at 40 & 80 min)',
            'midweek_key': '10 miles total: 3 x 2 miles @ 7:05/mi (2 min rest)',
            'structure': 'Mon: Rest | Tue: 10mi (3x2mi tempo) | Wed: 10mi (aerobic) | Thu: 7mi (easy) | Fri: Rest | Sat: 18mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '10 + 10 + 7 + 18 + 5 = 50 mi',
            'proxy_checkpoint': 'Post-10k aerobic efficiency and cardiac stability.'
        },
        {
            'week': 18, 'phase': 3, 'dates': 'Jan 25 - Jan 31', 'target_miles': 52,
            'long_run': '16 miles with fast finish (final 4 miles @ 7:20/mi)',
            'midweek_key': '10 miles total: 4 x 1.5 miles @ 6:58-7:02/mi (90s rest)',
            'structure': 'Mon: 4mi (recovery) | Tue: 10mi (T-intervals) | Wed: 10mi (aerobic) | Thu: 7mi (easy) | Fri: Rest | Sat: 16mi (Fast-Finish Long Run) | Sun: 5mi (recovery)',
            'breakdown': '4 + 10 + 10 + 7 + 16 + 5 = 52 mi',
            'proxy_checkpoint': 'Fast-finish cardiac drift under cumulative fatigue.'
        },

        # Phase 4: Weeks 19-24 (Marathon-Specific MP Blocks & Half Marathon)
        {
            'week': 19, 'phase': 4, 'dates': 'Feb 01 - Feb 07', 'target_miles': 54,
            'long_run': '17 miles with 6 miles @ Goal MP (7:26/mi)',
            'midweek_key': '10 miles total: 8mi aerobic + 6 x 200m turnover strides',
            'structure': 'Mon: 4mi (recovery) | Tue: 10mi (aerobic + strides) | Wed: 11mi (aerobic base) | Thu: 7mi (easy) | Fri: Rest | Sat: 17mi (Long Run w/ 6mi MP) | Sun: 5mi (recovery)',
            'breakdown': '4 + 10 + 11 + 7 + 17 + 5 = 54 mi',
            'proxy_checkpoint': 'MP HR Convergence: verify HR < 156 bpm during 6mi @ 7:26.'
        },
        {
            'week': 20, 'phase': 4, 'dates': 'Feb 08 - Feb 14', 'target_miles': 48,
            'long_run': '15 miles easy (Down-week before Half Marathon peak)',
            'midweek_key': '8 miles total: 4 x 1 mile @ 6:55-7:00/mi (75s rest)',
            'structure': 'Mon: 4mi (recovery) | Tue: 8mi (sharp intervals) | Wed: 10mi (aerobic) | Thu: 6mi (easy) | Fri: Rest | Sat: 15mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '4 + 8 + 10 + 6 + 15 + 5 = 48 mi',
            'proxy_checkpoint': 'Muscular freshness check before Half Marathon test.'
        },
        {
            'week': 21, 'phase': 4, 'dates': 'Feb 15 - Feb 21', 'target_miles': 52,
            'long_run': '16 miles steady aerobic with 3 miles @ 7:20/mi finish',
            'midweek_key': '10 miles total: 2 x 3 miles @ 7:10/mi (3 min rest)',
            'structure': 'Mon: 4mi (recovery) | Tue: 10mi (tempo workout) | Wed: 10mi (aerobic) | Thu: 7mi (easy) | Fri: Rest | Sat: 16mi (Progressive Long Run) | Sun: 5mi (recovery)',
            'breakdown': '4 + 10 + 10 + 7 + 16 + 5 = 52 mi',
            'proxy_checkpoint': 'Half Marathon race pacing rehearsal (7:05-7:08/mi pace feel).'
        },
        {
            'week': 22, 'phase': 4, 'dates': 'Feb 22 - Feb 28', 'target_miles': 44,
            'long_run': '18 miles total: Half Marathon Tune-Up Race (2mi warm + 13.1mi Race + 2.9mi cool)',
            'midweek_key': '8 miles total: 5 miles easy with 4 x 30s openers',
            'structure': 'Mon: Rest | Tue: 8mi (easy) | Wed: 8mi (easy + strides) | Thu: 6mi (easy) | Fri: Rest | Sat: 4mi (shakeout) | Sun: 18mi (Half Marathon Race Day)',
            'breakdown': '8 + 8 + 6 + 4 + 18 = 44 mi',
            'proxy_checkpoint': 'Benchmark 3 (CRITICAL): Sub-1:33:30 confirms sub-3:15 VDOT (50.5).'
        },
        {
            'week': 23, 'phase': 4, 'dates': 'Mar 01 - Mar 07', 'target_miles': 50,
            'long_run': '15 miles easy-to-steady recovery long run',
            'midweek_key': '9 miles steady aerobic with rolling terrain',
            'structure': 'Mon: 4mi (recovery) | Tue: 9mi (aerobic) | Wed: 10mi (aerobic base) | Thu: 7mi (easy) | Fri: Rest | Sat: 15mi (Long Run) | Sun: 5mi (recovery)',
            'breakdown': '4 + 9 + 10 + 7 + 15 + 5 = 50 mi',
            'proxy_checkpoint': 'Post-half marathon recovery and muscle enzyme clearance.'
        },
        {
            'week': 24, 'phase': 4, 'dates': 'Mar 08 - Mar 14', 'target_miles': 54,
            'long_run': '17 miles with 7 miles @ Goal MP (7:26/mi)',
            'midweek_key': '10 miles total: 4 x 1.5 miles @ 6:55-7:00/mi (90s rest)',
            'structure': 'Mon: 4mi (recovery) | Tue: 10mi (T-intervals) | Wed: 11mi (aerobic base) | Thu: 7mi (easy) | Fri: Rest | Sat: 17mi (Long Run w/ 7mi MP) | Sun: 5mi (recovery)',
            'breakdown': '4 + 10 + 11 + 7 + 17 + 5 = 54 mi',
            'proxy_checkpoint': 'Transition into Peak Block: holding 7:26 for 7 continuous miles.'
        },

        # Phase 5: Weeks 25-28 (Peak Volume & Vancouver Simulation)
        {
            'week': 25, 'phase': 5, 'dates': 'Mar 15 - Mar 21', 'target_miles': 56,
            'long_run': '19 miles: Vancouver Dress Rehearsal (9mi easy + 8mi @ 7:26 MP + 2mi cool)',
            'midweek_key': '10 miles total: 5 x 1 mile @ 6:58/mi (60s rest)',
            'structure': 'Mon: 4mi (recovery) | Tue: 10mi (T-intervals) | Wed: 11mi (aerobic) | Thu: 7mi (easy) | Fri: Rest | Sat: 19mi (Vancouver Dress Rehearsal) | Sun: 5mi (recovery)',
            'breakdown': '4 + 10 + 11 + 7 + 19 + 5 = 56 mi',
            'proxy_checkpoint': 'Full race simulation: shoes, gels (every 35 min), sodium, HR < 155 bpm at MP.'
        },
        {
            'week': 26, 'phase': 5, 'dates': 'Mar 22 - Mar 28', 'target_miles': 52,
            'long_run': '17 miles with alternating miles (1mi @ 8:15 / 1mi @ 7:20 MP)',
            'midweek_key': '9 miles total: 5 miles easy + 6 x 100m strides',
            'structure': 'Mon: 4mi (recovery) | Tue: 9mi (aerobic + strides) | Wed: 10mi (steady aerobic) | Thu: 7mi (easy) | Fri: Rest | Sat: 17mi (Alternating Long Run) | Sun: 5mi (recovery)',
            'breakdown': '4 + 9 + 10 + 7 + 17 + 5 = 52 mi',
            'proxy_checkpoint': 'Lactate clearance under alternating pace surges.'
        },
        {
            'week': 27, 'phase': 5, 'dates': 'Mar 29 - Apr 04', 'target_miles': 58,
            'long_run': '21 miles Peak Vancouver Simulation (Early steep climb + fast descent + flat finish)',
            'midweek_key': '10 miles total: 2 x 3 miles @ 7:15/mi (3 min rest)',
            'structure': 'Mon: 4mi (recovery) | Tue: 10mi (tempo workout) | Wed: 11mi (aerobic base) | Thu: 7mi (easy) | Fri: Rest | Sat: 21mi (Peak Simulation Long Run) | Sun: 5mi (recovery)',
            'breakdown': '4 + 10 + 11 + 7 + 21 + 5 = 58 mi',
            'proxy_checkpoint': 'Aerobic decoupling on 21 miles (Target < 4.5%). Peak volume achieved!'
        },
        {
            'week': 28, 'phase': 5, 'dates': 'Apr 05 - Apr 11', 'target_miles': 50,
            'long_run': '15 miles steady with 4 miles @ 7:26 MP in middle',
            'midweek_key': '9 miles total: 4 x 1 mile @ 7:00/mi (75s rest)',
            'structure': 'Mon: 4mi (recovery) | Tue: 9mi (cruise intervals) | Wed: 10mi (aerobic) | Thu: 7mi (easy) | Fri: Rest | Sat: 15mi (Steady w/ 4mi MP) | Sun: 5mi (recovery)',
            'breakdown': '4 + 9 + 10 + 7 + 15 + 5 = 50 mi',
            'proxy_checkpoint': 'Final high-volume stimulus before entering the 3-week taper.'
        },

        # Phase 6: Weeks 29-31 (Sharpening, Taper & Vancouver Race)
        {
            'week': 29, 'phase': 6, 'dates': 'Apr 12 - Apr 18', 'target_miles': 40,
            'long_run': '14 miles with 4 miles @ 7:26 Goal MP (Taper Week 1 - 75% volume)',
            'midweek_key': '8 miles total: 3 x 1 mile @ 7:00/mi (2 min rest)',
            'structure': 'Mon: Rest | Tue: 8mi (3x1mi T-intervals) | Wed: 8mi (aerobic base) | Thu: 6mi (easy) | Fri: Rest | Sat: 14mi (Long Run w/ 4mi MP) | Sun: 4mi (recovery)',
            'breakdown': '8 + 8 + 6 + 14 + 4 = 40 mi',
            'proxy_checkpoint': 'Taper feeling: legs should begin feeling springy and rested.'
        },
        {
            'week': 30, 'phase': 6, 'dates': 'Apr 19 - Apr 25', 'target_miles': 28,
            'long_run': '9 miles easy with 2 miles @ 7:26 MP (Taper Week 2 - 55% volume)',
            'midweek_key': '6 miles total: 4 miles easy + 4 x 400m @ 6:50/mi (sharpness)',
            'structure': 'Mon: Rest | Tue: 6mi (aerobic + 400s) | Wed: 6mi (easy) | Thu: 4mi (easy) | Fri: Rest | Sat: 9mi (easy w/ 2mi MP) | Sun: 3mi (recovery)',
            'breakdown': '6 + 6 + 4 + 9 + 3 = 28 mi',
            'proxy_checkpoint': 'Resting HR drop and sleep quality optimization.'
        },
        {
            'week': 31, 'phase': 6, 'dates': 'Apr 26 - May 02', 'target_miles': 18,
            'long_run': '🌟 Sunday: BMO Vancouver Marathon 2027 (26.2 miles @ 7:26/mi ➔ 3:15:00 Goal)',
            'midweek_key': 'Race week taper shakeouts: Tue 5mi, Wed 4mi, Thu 4mi w/ strides, Sat 3mi shakeout',
            'structure': 'Mon: Rest | Tue: 5mi (easy) | Wed: 4mi (easy) | Thu: 4mi (easy w/ strides) | Fri: Rest | Sat: 3mi (shakeout) | Sun: 2mi (warmup) [+ 26.2mi Race Day]',
            'breakdown': '5 + 4 + 4 + 3 + 2 = 18 mi (Pre-Race Taper) + 26.2 mi Marathon',
            'proxy_checkpoint': 'Pacing execution: respect Camosun Hill, cruise Spanish Banks & Kitsilano, metronome Seawall, kick to 3:14:xx finish.'
        }
    ]

    for w in raw_weeks:
        details = get_vancouver_daily_details(w['week'], w)
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
        if w['week'] == 31:
            w['breakdown'] = " + ".join(nums) + f" = 18 mi (+ 26.2mi Race Day)"
        else:
            w['breakdown'] = " + ".join(nums) + f" = {w['target_miles']} mi"

    return raw_weeks

def get_vancouver_daily_details(week_num, week_dict):
    """
    Generates the 7 daily workouts for Vancouver week_num and enriches with strength training.
    """
    structure_str = week_dict['structure']
    # Example format: Mon: Rest | Tue: 6mi (easy + strides) | Wed: 7mi (aerobic base) | Thu: 5mi (easy) | Fri: Rest | Sat: 9mi (Long Run) | Sun: 5mi (recovery)
    day_parts = [p.strip() for p in structure_str.split('|')]
    
    day_map = {
        'Mon': 'Monday', 'Tue': 'Tuesday', 'Wed': 'Wednesday', 'Thu': 'Thursday',
        'Fri': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday'
    }

    days = []
    for part in day_parts:
        if ':' not in part:
            continue
        d_abbr, d_desc = part.split(':', 1)
        d_abbr = d_abbr.strip()
        d_desc = d_desc.strip()
        
        miles = 0
        workout_name = d_desc
        pace_str = "8:45 – 9:15 / mi"
        hr_zone_str = "Zone 2 (135 – 144 bpm)"
        purpose_str = "Aerobic endurance adaptation."
        desc_str = d_desc

        if 'Rest' in d_desc:
            miles = 0
            workout_name = "Rest & Recovery"
            pace_str = "Rest / Mobility"
            hr_zone_str = "Rest (< 100 bpm)"
            purpose_str = "Cellular repair and musculoskeletal remodeling."
            desc_str = "Non-running day. Foam roll calves, hamstrings, and IT bands. Hydrate with electrolytes."
        elif 'mi' in d_desc:
            try:
                m_part = d_desc.split('mi')[0].strip()
                # could be "6" or "5.5"
                miles = float(m_part)
                workout_name = d_desc.split('(', 1)[1].replace(')', '').strip().title() if '(' in d_desc else d_desc
            except:
                miles = 0

        # Refine specific days
        if d_abbr == 'Tue':
            if 'Time Trial' in d_desc or 'TT' in d_desc:
                pace_str = "Goal 5k Pace: 6:50 – 6:55 / mi"
                hr_zone_str = "Zone 5 (> 168 bpm)"
                purpose_str = "Maximal aerobic capacity (VO2max) and threshold benchmark test."
                desc_str = "2 miles warm-up, 5k (3.1 miles) all-out time trial effort, 2.9 miles cool-down. Benchmark 1 fitness test."
            elif 'Interval' in d_desc or 'tempo' in d_desc.lower() or 'cruise' in d_desc.lower() or 'T-intervals' in d_desc:
                pace_str = "Intervals: 7:00 – 7:10 / mi | Recovery: 9:00 / mi"
                hr_zone_str = "Zone 4 Threshold (158 – 164 bpm)"
                purpose_str = "Lactate threshold velocity expansion and clearance rate."
                desc_str = f"Quality catalyst session: {d_desc}. Maintain relaxed shoulders and snappy cadence (180 spm)."
            elif 'strides' in d_desc.lower() or 'surges' in d_desc.lower():
                pace_str = "8:35 – 9:05 / mi (strides @ mile pace)"
                hr_zone_str = "Zone 2 base w/ Zone 4-5 surges"
                purpose_str = "Neuromuscular turnover and hill mechanics."
                desc_str = f"Aerobic run concluding with {d_desc}. Focus on high knee drive and upright posture."
            else:
                pace_str = "8:35 – 9:00 / mi"
                hr_zone_str = "Zone 2 (136 – 144 bpm)"
                purpose_str = "Aerobic base and running efficiency."
                desc_str = f"Steady aerobic run: {d_desc}."

        elif d_abbr == 'Wed':
            pace_str = "8:30 – 8:55 / mi"
            hr_zone_str = "Zone 2 Aerobic Base (136 – 145 bpm)"
            purpose_str = "Mitochondrial density, capillary bed expansion, and fatigue resistance."
            desc_str = f"Midweek double-digit aerobic anchor: {d_desc}. Crucial stamina builder for Vancouver's undulating profile."

        elif d_abbr == 'Thu':
            pace_str = "9:00 – 9:30 / mi"
            hr_zone_str = "Zone 1 / Low Zone 2 (< 138 bpm)"
            purpose_str = "Metabolic byproduct flushing and active recovery."
            desc_str = f"Gentle recovery jog: {d_desc}. Keep stride light, cadence relaxed, and effort conversational."

        elif d_abbr == 'Sat':
            if week_num == 31:
                pace_str = "9:30 / mi shakeout"
                hr_zone_str = "Zone 1 (< 130 bpm)"
                purpose_str = "Pre-race nervous system activation."
                desc_str = "3 miles very light shakeout with 4 x 20-second strides in Vancouver. Rest and carbo-load."
            elif 'Dress Rehearsal' in d_desc or 'MP' in d_desc:
                pace_str = "Easy: 8:40 / mi | MP Blocks: 7:26 / mi"
                hr_zone_str = "Zone 2 base progressing to Zone 3 (151–155 bpm) at MP"
                purpose_str = "Marathon pace economy and in-race fueling dress rehearsal."
                desc_str = f"Marathon Anchor: {d_desc}. Take gel every 35–40 minutes with water. Practice wearing race kit."
            elif 'Simulation' in d_desc:
                pace_str = "8:30 – 8:50 / mi (surge climbs @ 8:15, cruise flats @ 7:45)"
                hr_zone_str = "Zone 2-3 (140 – 152 bpm)"
                purpose_str = "Vancouver course terrain simulation (Camosun climb + Marine Drive descent + Seawall flat)."
                desc_str = f"Peak simulation: {d_desc}. Practice climbing on effort rather than forcing GPS pace, followed by relaxed quad-friendly descending."
            else:
                pace_str = "8:40 – 9:15 / mi"
                hr_zone_str = "Zone 2 (138 – 146 bpm)"
                purpose_str = "Long aerobic endurance and fat oxidation."
                desc_str = f"Weekly long run anchor: {d_desc}. Maintain steady effort on Seattle rolling hills."

        elif d_abbr == 'Sun':
            if week_num == 31:
                miles = 28.2 # 2mi warmup + 26.2mi race
                workout_name = "🌟 BMO Vancouver Marathon 2027"
                pace_str = "7:26 / mi (3:15:00 Goal)"
                hr_zone_str = "Zone 3 Aerobic Threshold (151 – 156 bpm)"
                desc_str = ('Race Morning: Wake up 3.5h before start. Light 2mi warmup shakeout at Queen Elizabeth Park (elevation 152m).\\n'
                            'Km 0–8 (Miles 1–5): Gentle descent out of QE Park into Dunbar. Settle into disciplined 7:28–7:30/mi rhythm.\\n'
                            'Km 9–10 (Mile 6): Camosun Street Hill climb (~177 ft vertical rise). SURRENDER PACE, HOLD EFFORT! Run by HR (< 158 bpm, ~8:10/mi). Your Seattle training makes this routine.\\n'
                            'Km 10–16 (Miles 6.5–10): Pacific Spirit Park & UBC campus. Regroup into 7:24–7:26/mi cruise.\\n'
                            'Km 16–18 (Miles 10–11.5): Big descent down NW Marine Drive (-250 ft drop to sea level). Lean forward, light feet (cadence >180 spm), protect your quads!\\n'
                            'Km 18–31 (Miles 11.5–19.5): Spanish Banks, Point Grey & Kitsilano. The metronome miles: lock into 7:24–7:26/mi. Gel every 35 mins with water.\\n'
                            'Km 31–32 (Miles 19.5–20): Burrard Bridge climb. Drive knees over the crest into West End.\\n'
                            'Km 32–40 (Miles 20–25): Stanley Park Seawall flat loop. 9 km of flat ocean-side running. Hold your 7:24/mi line; mental grit wins the race here.\\n'
                            'Km 40–42.2 (Miles 25–26.2): Exit seawall onto West Pender Street rise. Empty the tank at 7:15/mi into the downtown Vancouver finish line for 3:14:xx!')
                purpose_str = "Race day execution: The culmination of 31 weeks of disciplined training!"
            elif 'Half Marathon' in d_desc:
                pace_str = "Goal Half Marathon Pace: 7:05 – 7:08 / mi"
                hr_zone_str = "Zone 4 Threshold (160 – 166 bpm)"
                purpose_str = "Benchmark 3: Validate 3:15 marathon fitness with a sub-1:33:30 half marathon."
                desc_str = "Half Marathon Tune-Up Race. 2mi warm-up, 13.1mi race execution (< 1:33:30), 2.9mi cool-down. Confirms VDOT 50.5."
            else:
                pace_str = "9:15 – 9:45 / mi"
                hr_zone_str = "Zone 1 (< 135 bpm)"
                purpose_str = "Aerobic density and cumulative fatigue recovery."
                desc_str = f"Gentle Sunday recovery shakeout: {d_desc}. Runs gently on legs carrying Saturday fatigue."

        days.append({
            'day': d_abbr,
            'day_full': day_map.get(d_abbr, d_abbr),
            'miles': miles,
            'workout': workout_name,
            'pace': pace_str,
            'hr_zone': hr_zone_str,
            'purpose': purpose_str,
            'description': desc_str
        })

    return apply_lifting_schedule(week_num, days, total_weeks=31)
