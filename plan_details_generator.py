"""
plan_details_generator.py - Comprehensive day-by-day workout details for all 23 weeks
of the LA Marathon 2027 sub-3:15 training plan.
"""

def get_week_daily_details(week_num):
    """
    Returns a list of 7 daily workout dictionaries (Monday through Sunday) for the given week.
    Each item contains:
      - day: str (e.g. 'Mon')
      - day_full: str (e.g. 'Monday')
      - miles: float/int
      - workout: str (e.g. 'Easy Aerobic + Uphill Strides')
      - pace: str (e.g. '8:45 - 9:15 / mi')
      - hr_zone: str (e.g. 'Zone 2: 135 - 142 bpm')
      - purpose: str
      - description: str
    """
    plans = {
        # PHASE 1: WEEKS 1-5 (Base & Hill Conditioning)
        1: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 0,
                'workout': 'Rest & Recovery',
                'pace': 'Rest / Mobility',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Full muscular restoration and glycogen replenishment.',
                'description': 'Rest day. 15 mins foam rolling (calves, hamstrings, glutes) and light stretching. Hydrate well.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 6,
                'workout': 'Easy Aerobic + Uphill Strides',
                'pace': '8:45 – 9:15 / mi (strides fast & relaxed)',
                'hr_zone': 'Zone 2 (135 – 142 bpm)',
                'purpose': 'Neuromuscular recruitment and running economy without lactic accumulation.',
                'description': '5.5 miles easy aerobic base running on rolling roads. Finish with 6 x 100m uphill strides (4–6% grade) focusing on tall posture, knee lift, and relaxed shoulders. Walk down slowly for recovery.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 8,
                'workout': 'Midweek Aerobic Base (Medium Long Run)',
                'pace': '8:40 – 9:05 / mi',
                'hr_zone': 'Zone 2 (136 – 144 bpm)',
                'purpose': 'Capillary bed density, mitochondrial growth, and steady aerobic stamina.',
                'description': 'Continuous steady aerobic run. Settle into smooth, rhythmic breathing (3:3 cadence). Avoid pushing uphill; let heart rate dictate pace on Seattle climbs.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 5,
                'workout': 'Easy Recovery Run',
                'pace': '9:00 – 9:30 / mi',
                'hr_zone': 'Zone 1 / Low Zone 2 (< 138 bpm)',
                'purpose': 'Active flushing of metabolic byproducts without mechanical stress.',
                'description': 'Gentle conversational recovery run. Keep stride compact, cadence quick (176–180 spm), and effort relaxed.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Rest & Pre-Long Run Freshening',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Topping up glycogen stores and resting legs before the Saturday anchor long run.',
                'description': 'Full rest. Eat nutrient-rich complex carbohydrates, drink electrolytes, and aim for 8+ hours of sleep.'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 10,
                'workout': 'Long Run (Aerobic Durability Anchor)',
                'pace': '8:45 – 9:15 / mi',
                'hr_zone': 'Zone 2 (138 – 146 bpm)',
                'purpose': 'Fat oxidation efficiency, muscular stamina, and aerobic baseline expansion.',
                'description': 'Progressive steady long run on rolling terrain. First 5 miles conversational (9:00–9:15/mi); naturally settle into 8:45–8:55/mi over the second half. Take water or electrolytes at mile 5.'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 5,
                'workout': 'Aerobic Density Recovery Run',
                'pace': '9:15 – 9:45 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Stimulates endurance adaptations by running gently on legs carrying cumulative fatigue.',
                'description': 'Very easy, conversational Sunday shakeout. Flatter route preferred. Focus on light foot strikes and diaphragmatic breathing.'
            }
        ],

        2: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 0,
                'workout': 'Rest & Recovery',
                'pace': 'Rest / Mobility',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Muscular repair and central nervous system decompression.',
                'description': 'Full rest day. Foam roll lower legs and do 10 minutes of hip mobility exercises.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 7,
                'workout': 'Aerobic Base + Flat Strides',
                'pace': '8:45 – 9:10 / mi (strides @ mile pace)',
                'hr_zone': 'Zone 2 (135 – 142 bpm)',
                'purpose': 'Reinforcing high cadence (> 178 spm) and hip extension under aerobic comfort.',
                'description': '6.5 miles steady Zone 2 aerobic cruising. Conclude with 6 x 100m flat accelerations on grass or track with full walking recoveries.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 8,
                'workout': 'Steady Aerobic Run',
                'pace': '8:35 – 9:00 / mi',
                'hr_zone': 'Zone 2 (138 – 145 bpm)',
                'purpose': 'Midweek volume anchor and cardiac stroke volume maintenance.',
                'description': 'Consistent aerobic run. Focus on smooth effort through rolling terrain without surging on the climbs.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 5,
                'workout': 'Easy Recovery Run',
                'pace': '9:00 – 9:30 / mi',
                'hr_zone': 'Zone 1/2 (< 138 bpm)',
                'purpose': 'Low-impact blood flow stimulation.',
                'description': 'Easy conversational jog. Focus on relaxed breathing and keeping effort strictly conversational.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Rest & Pre-Long Run Nutrition',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Preparation for Saturday distance extension.',
                'description': 'Full rest. Hydrate with electrolyte tablets throughout the day.'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 11,
                'workout': 'Rolling Hills Long Run',
                'pace': '8:45 – 9:10 / mi',
                'hr_zone': 'Zone 2 (140 – 148 bpm)',
                'purpose': 'Eccentric quad resilience and hill-climbing power for the Los Angeles course.',
                'description': '11 miles over undulating terrain. Run by heart rate on climbs (< 152 bpm); allow yourself to coast smoothly on gentle descents with compact turnover.'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 5,
                'workout': 'Recovery Shakeout',
                'pace': '9:15 – 9:45 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Fatigue adaptation and safe mileage accumulation.',
                'description': 'Gentle shakeout run. Keeps muscles loose after Saturday\'s rolling 11-miler.'
            }
        ],

        3: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 0,
                'workout': 'Rest & Recovery',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Systemic recovery.',
                'description': 'Rest day. Light mobility and calf/hamstring stretching.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 7,
                'workout': 'Hill Surges Workout',
                'pace': '1.5mi warm @ 9:00, surges @ 5k effort, 2.5mi cool',
                'hr_zone': 'Surges: Zone 4 (160 – 166 bpm)',
                'purpose': 'VO2max power, rapid motor unit recruitment, and hill running economy.',
                'description': '1.5 miles easy warmup. Then 6 x 60-second powerful surges up a 4–6% grade hill at hard 5k effort, jogging down slowly (90s recovery). Finish with 2.5 miles easy cooldown.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 9,
                'workout': 'Aerobic Base (Medium Long Run)',
                'pace': '8:40 – 9:05 / mi',
                'hr_zone': 'Zone 2 (136 – 144 bpm)',
                'purpose': 'Aerobic durability and mitochondrial volume expansion.',
                'description': '9 continuous steady aerobic miles. Track Aerobic Efficiency Factor (EF) on this run to gauge baseline efficiency.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 5,
                'workout': 'Easy Recovery Run',
                'pace': '9:00 – 9:30 / mi',
                'hr_zone': 'Zone 1 (< 138 bpm)',
                'purpose': 'Active recovery between Tuesday quality and Saturday long run.',
                'description': 'Relaxed, easy 5 miles. Keep heart rate low and legs light.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Rest & Nutrition',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Carbohydrate loading and hydration.',
                'description': 'Full rest. Prepare gear and hydration for Saturday.'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 12,
                'workout': 'Progression Long Run',
                'pace': 'First 10mi @ 8:50 – 9:10 / mi; last 2mi @ 8:15 / mi',
                'hr_zone': 'Zone 2 (140 – 146 bpm) ramping to Zone 3 (152 bpm)',
                'purpose': 'Teaches neuromuscular system to shift gears and run faster on depleted legs.',
                'description': '12 miles total. Cruise easily for the first 10 miles. At mile 10, consciously drop pace to 8:15/mi for the final 2 miles while maintaining tall posture.'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 5,
                'workout': 'Recovery Shakeout',
                'pace': '9:15 – 9:45 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Clearing residual lactate and completing the 38-mile week.',
                'description': 'Slow recovery miles. Flattest route available.'
            }
        ],

        4: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 0,
                'workout': 'Rest & Recovery',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Absorption of Week 3 volume.',
                'description': 'Rest day. Foam rolling and hip flexor stretches.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 8,
                'workout': 'Aerobic Threshold Steady-State Tempo',
                'pace': '2mi warm @ 9:00 + 20 min @ 7:45/mi + 2mi cool',
                'hr_zone': 'Tempo block: 154 – 158 bpm (Zone 3/4 border)',
                'purpose': 'Elevating aerobic floor and expanding sub-threshold metabolic efficiency.',
                'description': '2 miles easy warmup. Settle into 20 continuous minutes at steady 7:45/mile (approximately 2.6 miles). Finish with 2+ miles easy cooldown.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 9,
                'workout': 'Midweek Aerobic Base',
                'pace': '8:35 – 9:00 / mi',
                'hr_zone': 'Zone 2 (136 – 144 bpm)',
                'purpose': 'Aerobic capacity building.',
                'description': 'Steady Zone 2 running. Focus on even breathing and cadence.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 5,
                'workout': 'Easy Recovery Run',
                'pace': '9:00 – 9:30 / mi',
                'hr_zone': 'Zone 1 (< 138 bpm)',
                'purpose': 'Active recovery.',
                'description': 'Gentle recovery miles. Zero strain.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Rest & Pre-Long Run Nutrition',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Glycogen loading.',
                'description': 'Full rest. Hydrate well.'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 13,
                'workout': 'Half-Marathon Distance Long Run',
                'pace': '8:45 – 9:00 / mi steady',
                'hr_zone': 'Zone 2 (138 – 146 bpm)',
                'purpose': 'First official Aerobic Decoupling test (Target < 6%) and in-run fueling test.',
                'description': '13.1 miles steady aerobic running. Practice taking a gel at minute 45 with 4–6 oz of water. Check first half vs second half heart rate decoupling.'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 5,
                'workout': 'Recovery Shakeout',
                'pace': '9:15 – 9:45 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Completing the 40-mile milestone.',
                'description': 'Relaxed conversational jog.'
            }
        ],

        5: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 0,
                'workout': 'Rest & Recovery',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Down-week adaptation and freshness before 5k benchmark.',
                'description': 'Rest day. Sleep, foam roll, and mentally prep for Wednesday\'s 5k test.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 6,
                'workout': 'Easy Run + Strides (Opener)',
                'pace': '8:50 – 9:15 / mi + 4x100m strides',
                'hr_zone': 'Zone 2 (< 140 bpm)',
                'purpose': 'Neuromuscular priming without fatigue.',
                'description': '5.5 miles easy. 4 crisp 100m strides at 5k pace to activate fast-twitch fibers.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 8,
                'workout': '🌟 BENCHMARK 1: 5k Time Trial / Parkrun',
                'pace': '2mi warm + 3.1mi TT @ max sustainable pace + 2.9mi cool',
                'hr_zone': 'TT: Zone 5 (166 – 174 bpm)',
                'purpose': 'First physiological check: sub-21:30 validates current VDOT ≥ 47.5.',
                'description': '2 miles easy warmup with dynamic drills. Run a flat 5,000m (or Parkrun) at maximum sustainable effort (Goal: sub-21:30 / 6:55/mi). Finish with 2.9 miles very easy cooldown.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 6,
                'workout': 'Post-Race Recovery Aerobic',
                'pace': '9:10 – 9:35 / mi',
                'hr_zone': 'Zone 1 (< 136 bpm)',
                'purpose': 'Flushing muscle soreness from Wednesday\'s 5k all-out effort.',
                'description': 'Super gentle aerobic run. Zero pace goals; just relaxed blood flow.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Rest',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Down-week consolidation.',
                'description': 'Full rest.'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 10,
                'workout': 'Easy Long Run (Down-Week Cutback)',
                'pace': '8:50 – 9:15 / mi',
                'hr_zone': 'Zone 2 (136 – 144 bpm)',
                'purpose': 'Consolidating Phase 1 adaptations before entering Phase 2 threshold build.',
                'description': '10 miles easy and relaxed. Enjoyable conversational pace.'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 5,
                'workout': 'Recovery Shakeout',
                'pace': '9:15 – 9:45 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Completing Phase 1 at 35 miles.',
                'description': 'Gentle Sunday recovery. Phase 1 Base & Hills complete!'
            }
        ],

        # PHASE 2: WEEKS 6-10 (Lactate Threshold & Speed-Endurance)
        6: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 0,
                'workout': 'Rest & Recovery',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Restoration before Phase 2 threshold intensity begins.',
                'description': 'Full rest day. Foam rolling and calf massage.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 8,
                'workout': 'Cruise Intervals: 4 x 1 Mile',
                'pace': '2mi warm + 4 x 1mi @ 7:15/mi (60s rest) + 2mi cool',
                'hr_zone': 'Work intervals: Zone 4 (158 – 164 bpm)',
                'purpose': 'Lactate clearance velocity and threshold expansion.',
                'description': '2 miles easy warmup. 4 x 1 mile at 7:15/mi with exactly 60 seconds jogging recovery between reps. Heart rate should rise to 158–162 bpm by end of each rep. 2 miles easy cooldown.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 9,
                'workout': 'Aerobic Base Run',
                'pace': '8:35 – 9:00 / mi',
                'hr_zone': 'Zone 2 (138 – 145 bpm)',
                'purpose': 'Aerobic volume to absorb Tuesday threshold stimulus.',
                'description': '9 miles steady Zone 2. Let legs settle into a smooth rhythm.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 6,
                'workout': 'Easy Recovery Run',
                'pace': '9:00 – 9:30 / mi',
                'hr_zone': 'Zone 1 (< 138 bpm)',
                'purpose': 'Active flushing.',
                'description': '6 easy conversational miles. Keep cadence crisp.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Rest',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Hydration and glycogen rest.',
                'description': 'Full rest before weekend long run.'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 14,
                'workout': 'Steady Long Run with Rolling Elevation',
                'pace': '8:40 – 9:05 / mi',
                'hr_zone': 'Zone 2 (140 – 148 bpm)',
                'purpose': 'Long distance aerobic efficiency and Seattle hill adaptation.',
                'description': '14 miles continuous over rolling terrain. Practice taking a gel at mile 6 and mile 11 with water.'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 5,
                'workout': 'Recovery Run',
                'pace': '9:15 – 9:45 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Completing 42 miles.',
                'description': 'Easy recovery jog on flat route.'
            }
        ],

        7: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 0,
                'workout': 'Rest & Recovery',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Recovery.',
                'description': 'Rest day.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 8,
                'workout': 'Continuous Threshold Tempo: 25 Minutes',
                'pace': '2mi warm + 25 min @ 7:15/mi (~3.5mi) + 2.5mi cool',
                'hr_zone': 'Tempo: Zone 4 (158 – 162 bpm)',
                'purpose': 'Sustained lactate buffering capacity and mental toughness at threshold.',
                'description': '2 miles easy warmup. 25 continuous minutes locked into 7:15/mile on flat or track. Focus on relaxed jaw, low shoulders, and steady breathing. 2.5 miles easy cooldown.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 10,
                'workout': 'Midweek Long Run (Double-Digit Midweek)',
                'pace': '8:35 – 9:00 / mi',
                'hr_zone': 'Zone 2 (138 – 146 bpm)',
                'purpose': 'High aerobic volume stimulus during the work week.',
                'description': '10 miles steady aerobic cruising. This midweek double-digit run is the secret weapon for marathon endurance.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 6,
                'workout': 'Easy Recovery Run',
                'pace': '9:00 – 9:30 / mi',
                'hr_zone': 'Zone 1 (< 138 bpm)',
                'purpose': 'Active recovery.',
                'description': 'Relaxed conversational jog.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Rest',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Pre-long run rest.',
                'description': 'Full rest. Hydrate well.'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 15,
                'workout': 'Progressive Long Run',
                'pace': 'First 12mi @ 8:45/mi; final 3mi progressive down to 7:45/mi',
                'hr_zone': 'Zone 2 ramping to Zone 3/4 (140 to 156 bpm)',
                'purpose': 'Fast-finish durability and late-stage glycogen depletion resistance.',
                'description': '15 miles. Settle into 8:45/mi through mile 12. For miles 13, 14, and 15, drop pace to 8:15, 8:00, and 7:45/mi. Measure Decoupling (target < 5.5%).'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 5,
                'workout': 'Recovery Run',
                'pace': '9:15 – 9:45 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Completing 44-mile week.',
                'description': 'Easy recovery miles.'
            }
        ],

        8: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 0,
                'workout': 'Rest & Recovery',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Recovery.',
                'description': 'Rest day.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 9,
                'workout': 'Cruise Intervals: 5 x 1 Mile',
                'pace': '2mi warm + 5 x 1mi @ 7:08 – 7:12/mi (60s rest) + 2mi cool',
                'hr_zone': 'Work intervals: Zone 4 (159 – 165 bpm)',
                'purpose': 'Progressing threshold velocity closer to 7:00 pace.',
                'description': '2 miles easy warmup. 5 x 1 mile at 7:08–7:12/mi with 60 seconds jogging recovery. Controlled power on each rep. 2 miles easy cooldown.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 10,
                'workout': 'Midweek Aerobic Base',
                'pace': '8:30 – 8:55 / mi',
                'hr_zone': 'Zone 2 (138 – 145 bpm)',
                'purpose': 'Aerobic capacity.',
                'description': '10 miles steady Zone 2. Check if GAP-EF exceeds 1.34.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 6,
                'workout': 'Easy Recovery Run',
                'pace': '9:00 – 9:30 / mi',
                'hr_zone': 'Zone 1 (< 138 bpm)',
                'purpose': 'Active flushing.',
                'description': '6 easy recovery miles.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Rest',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Rest and fueling.',
                'description': 'Full rest before 16-miler.'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 16,
                'workout': 'Long Run with Formal Fueling Protocol',
                'pace': '8:40 – 9:00 / mi',
                'hr_zone': 'Zone 2 (140 – 148 bpm)',
                'purpose': 'Gut training: consuming carbohydrates every 45 minutes.',
                'description': '16 miles steady aerobic. Take an energy gel at minute 45 and minute 90 with 5 oz of water each time. Teaches stomach to absorb fuel at heart rate 145 bpm.'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 5,
                'workout': 'Recovery Run',
                'pace': '9:15 – 9:45 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Completing 46-mile week.',
                'description': 'Gentle shakeout.'
            }
        ],

        9: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 0,
                'workout': 'Rest & Recovery',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Recovery.',
                'description': 'Rest day.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 9,
                'workout': 'Sustained Threshold Tempo: 30 Minutes',
                'pace': '2mi warm + 30 min continuous @ 7:05 – 7:10/mi (~4.2mi) + 2.8mi cool',
                'hr_zone': 'Tempo: Zone 4 (160 – 165 bpm)',
                'purpose': 'Peak threshold stamina: 30 min continuous at target T-pace.',
                'description': '2 miles easy warmup. Lock into 7:05–7:10/mi for 30 uninterrupted minutes on flat terrain. 2.8 miles easy cooldown.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 11,
                'workout': 'Midweek Long Run',
                'pace': '8:35 – 9:00 / mi',
                'hr_zone': 'Zone 2 (138 – 146 bpm)',
                'purpose': 'Aerobic endurance.',
                'description': '11 miles continuous aerobic base running.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 6,
                'workout': 'Easy Recovery Run',
                'pace': '9:00 – 9:30 / mi',
                'hr_zone': 'Zone 1 (< 138 bpm)',
                'purpose': 'Active recovery.',
                'description': '6 gentle recovery miles.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Rest',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Pre-long run rest.',
                'description': 'Full rest day.'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 16,
                'workout': 'Long Run with 4 Miles @ Goal Marathon Pace (7:26)',
                'pace': '10mi easy @ 8:45/mi + 4mi continuous @ 7:26 MP + 2mi cool',
                'hr_zone': 'MP block: Zone 3 (Target < 160 bpm)',
                'purpose': 'First major test of holding 7:26 pace after 10 miles of pre-fatigue.',
                'description': '10 miles easy conversational (8:45/mi). At mile 10, shift directly into 7:26/mile for 4 continuous miles. Observe cardiac drift during the MP block. 2 miles easy cooldown.'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 6,
                'workout': 'Recovery Run',
                'pace': '9:15 – 9:45 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Completing 48-mile week.',
                'description': '6 easy recovery miles on soft ground.'
            }
        ],

        10: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 0,
                'workout': 'Rest & Recovery',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Freshening up for 10k tune-up race.',
                'description': 'Rest day. Light mobility.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 6,
                'workout': 'Easy Run + 4x100m Strides',
                'pace': '8:50 – 9:15 / mi',
                'hr_zone': 'Zone 2 (< 140 bpm)',
                'purpose': 'Pre-race shakeout and neuromuscular priming.',
                'description': '5.5 miles easy. 4 light strides at 10k pace.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 10,
                'workout': '🌟 BENCHMARK 2: 10k Tune-Up Race',
                'pace': '2mi warm + 6.2mi Race @ max effort + 1.8mi cool',
                'hr_zone': 'Race: Zone 4/5 (165 – 172 bpm)',
                'purpose': 'Validates VDOT 49.0: Target sub-43:00 (6:55/mi average).',
                'description': '2 miles easy warmup with dynamic drills. Run a flat 10k road race or time trial at maximum even-split effort (Goal: < 43:00 / 6:55/mi). 1.8 miles easy cooldown.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 7,
                'workout': 'Post-Race Recovery Aerobic',
                'pace': '9:15 – 9:40 / mi',
                'hr_zone': 'Zone 1 (< 136 bpm)',
                'purpose': 'Flushing fatigue from 10k race effort.',
                'description': '7 slow, gentle recovery miles.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Rest',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Consolidation.',
                'description': 'Full rest.'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 12,
                'workout': 'Easy Long Run (Adaptation Week)',
                'pace': '8:45 – 9:15 / mi',
                'hr_zone': 'Zone 2 (138 – 144 bpm)',
                'purpose': 'Cutback long run to let Phase 2 threshold adaptations consolidate.',
                'description': '12 miles comfortable conversational pace.'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 5,
                'workout': 'Recovery Shakeout',
                'pace': '9:15 – 9:45 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Completing Phase 2 at 40 miles.',
                'description': '5 easy recovery miles. Phase 2 Threshold Expansion complete!'
            }
        ],

        # PHASE 3: WEEKS 11-16 (Marathon-Specific MP Blocks)
        11: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 0,
                'workout': 'Rest & Recovery',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Recovery before entering Phase 3 specific MP blocks.',
                'description': 'Rest day. Foam rolling and calf stretching.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 9,
                'workout': 'Threshold Cruise: 6 x 1 Mile',
                'pace': '2mi warm + 6 x 1mi @ 7:05/mi (75s jog) + 1mi cool',
                'hr_zone': 'Work intervals: Zone 4 (160 – 165 bpm)',
                'purpose': 'Peak threshold interval volume: 6 miles total at sub-3:15 threshold pace.',
                'description': '2 miles easy warmup. 6 x 1 mile at 7:05/mile with 75 seconds jogging recovery. Keep every rep within 2 seconds of 7:05. 1 mile easy cooldown.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 10,
                'workout': 'Midweek Aerobic Base',
                'pace': '8:30 – 8:55 / mi',
                'hr_zone': 'Zone 2 (138 – 145 bpm)',
                'purpose': 'Aerobic stamina.',
                'description': '10 miles steady Zone 2.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 7,
                'workout': 'Easy Aerobic Run',
                'pace': '8:55 – 9:25 / mi',
                'hr_zone': 'Zone 1/2 (< 138 bpm)',
                'purpose': 'Active recovery.',
                'description': '7 easy miles.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Rest',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Fueling before 17-miler.',
                'description': 'Full rest day.'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 17,
                'workout': 'Steady Long Run with Double Fueling Check',
                'pace': '8:35 – 8:55 / mi',
                'hr_zone': 'Zone 2 (140 – 148 bpm)',
                'purpose': 'Aerobic over-distance engine building; decoupling target < 5.0%.',
                'description': '17 miles steady aerobic. Take energy gel at minute 40 and minute 80 with water. Practice relaxed breathing and high cadence on rolling hills.'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 5,
                'workout': 'Recovery Shakeout',
                'pace': '9:15 – 9:45 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Completing 48 miles.',
                'description': '5 gentle recovery miles.'
            }
        ],

        12: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 0,
                'workout': 'Rest & Recovery',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Recovery.',
                'description': 'Rest day.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 10,
                'workout': 'Extended Threshold: 2 x 2 Miles',
                'pace': '2mi warm + 2 x 2mi @ 7:00/mi (2 min rest) + 2mi cool',
                'hr_zone': 'Intervals: Zone 4 (160 – 166 bpm)',
                'purpose': 'Extended threshold volume: teaching body to hold 7:00 pace for 14 continuous minutes per rep.',
                'description': '2 miles easy warmup. Rep 1: 2 miles @ 7:00/mi. Jog 2 minutes. Rep 2: 2 miles @ 7:00/mi. 2 miles easy cooldown.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 10,
                'workout': 'Midweek Aerobic Base',
                'pace': '8:30 – 8:55 / mi',
                'hr_zone': 'Zone 2 (138 – 145 bpm)',
                'purpose': 'Aerobic volume.',
                'description': '10 miles steady Zone 2.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 7,
                'workout': 'Easy Aerobic Run',
                'pace': '9:00 – 9:25 / mi',
                'hr_zone': 'Zone 1 (< 138 bpm)',
                'purpose': 'Active recovery.',
                'description': '7 easy miles.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Rest',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Pre-long run fueling.',
                'description': 'Full rest day.'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 18,
                'workout': 'Long Run with 6 Miles @ Goal Marathon Pace (7:26)',
                'pace': '9mi easy @ 8:40/mi + 6mi continuous @ 7:26 MP + 3mi cool',
                'hr_zone': 'MP block: Zone 3 (151 – 155 bpm)',
                'purpose': 'Heart Rate Convergence Check: verify that 7:26 pace stays in Zone 3 (~153 bpm) even at mile 15!',
                'description': '9 miles easy aerobic (8:40/mi). Shift directly to 7:26 Goal Marathon Pace for miles 10 through 15. Observe heart rate—if HR stays under 156 bpm, fitness is right on schedule. 3 miles easy cooldown.'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 5,
                'workout': 'Recovery Shakeout',
                'pace': '9:15 – 9:45 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Crossing the 50 MPW milestone.',
                'description': '5 gentle recovery miles. 50-mile week in the books!'
            }
        ],

        13: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 0,
                'workout': 'Rest & Recovery',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Holiday consolidation and muscular repair.',
                'description': 'Rest day. Foam rolling and sleep.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 8,
                'workout': 'Easy Aerobic + 8x100m Snappy Strides',
                'pace': '8:45 – 9:10 / mi + strides',
                'hr_zone': 'Zone 2 (< 140 bpm)',
                'purpose': 'Leg turnover and running mechanics without central fatigue.',
                'description': '7.5 miles easy aerobic running. Finish with 8 crisp 100m flat strides focusing on light, elastic ground contact.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 9,
                'workout': 'Steady Aerobic Run',
                'pace': '8:35 – 9:00 / mi',
                'hr_zone': 'Zone 2 (138 – 145 bpm)',
                'purpose': 'Aerobic maintenance during holiday week.',
                'description': '9 miles comfortable steady running.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 7,
                'workout': 'Easy Run',
                'pace': '9:00 – 9:25 / mi',
                'hr_zone': 'Zone 1 (< 138 bpm)',
                'purpose': 'Active recovery.',
                'description': '7 easy miles.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Rest',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Rest.',
                'description': 'Full rest day.'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 15,
                'workout': 'Easy Aerobic Long Run',
                'pace': '8:45 – 9:10 / mi',
                'hr_zone': 'Zone 2 (138 – 145 bpm)',
                'purpose': 'Consolidating endurance adaptations with low neurological stress.',
                'description': '15 miles comfortable aerobic cruising.'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 5,
                'workout': 'Recovery Shakeout',
                'pace': '9:15 – 9:45 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Completing 44-mile week.',
                'description': '5 gentle miles.'
            }
        ],

        14: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 4,
                'workout': 'Gentle Aerobic Shakeout (First 6-Day Week)',
                'pace': '9:15 – 9:45 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Introduces 6 days/week running frequency to safely expand volume to 52 mpw.',
                'description': '4 very easy recovery miles. Flattest route possible. Just light movement.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 10,
                'workout': 'Long Threshold Intervals: 3 x 1.5 Miles',
                'pace': '2mi warm + 3 x 1.5mi @ 6:58 – 7:02/mi (90s rest) + 3.5mi cool',
                'hr_zone': 'Intervals: Zone 4 (161 – 166 bpm)',
                'purpose': 'Sub-7:00 threshold speed reserve: 4.5 cumulative miles at 7:00 pace.',
                'description': '2 miles easy warmup. 3 x 1.5 miles at 6:58–7:02/mi with 90 seconds jogging recovery. Controlled breathing and rhythm. 3.5 miles easy cooldown.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 10,
                'workout': 'Midweek Aerobic Base',
                'pace': '8:30 – 8:55 / mi',
                'hr_zone': 'Zone 2 (138 – 145 bpm)',
                'purpose': 'Aerobic volume.',
                'description': '10 miles steady Zone 2.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 7,
                'workout': 'Easy Aerobic Run',
                'pace': '9:00 – 9:25 / mi',
                'hr_zone': 'Zone 1 (< 138 bpm)',
                'purpose': 'Active recovery.',
                'description': '7 easy conversational miles.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Rest',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Crucial rest before fast-finish long run.',
                'description': 'Full rest day. Hydration and early sleep.'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 16,
                'workout': 'Fast-Finish Long Run',
                'pace': '12mi easy @ 8:45/mi + final 4mi progressive acceleration down to 7:20/mi',
                'hr_zone': 'Zone 2 ramping to Zone 3/4 (140 to 158 bpm)',
                'purpose': 'Teaches mind and legs to recruit fast-twitch fibers under heavy fatigue.',
                'description': '12 miles easy conversational running. For the final 4 miles, cut down pace each mile: 7:40, 7:30, 7:25, and 7:20/mi into the finish.'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 5,
                'workout': 'Recovery Shakeout',
                'pace': '9:15 – 9:45 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Completing 52 miles.',
                'description': '5 gentle recovery miles.'
            }
        ],

        15: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 4,
                'workout': 'Recovery Shakeout',
                'pace': '9:15 – 9:45 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Active flushing.',
                'description': '4 easy recovery miles.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 10,
                'workout': 'Aerobic Base + 6 x 200m Turnover Strides',
                'pace': '8:35 – 9:00 / mi + 200m strides @ 42–44s',
                'hr_zone': 'Zone 2 (138 – 144 bpm)',
                'purpose': 'Speed reserve and neuromuscular snap without lactic fatigue.',
                'description': '9 miles steady aerobic running. Finish with 6 x 200m strides on flat or track at smooth mile race pace (42–44 seconds per 200m) with 200m slow walking/jogging recovery.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 10,
                'workout': 'Steady Aerobic Run',
                'pace': '8:30 – 8:55 / mi',
                'hr_zone': 'Zone 2 (138 – 145 bpm)',
                'purpose': 'Aerobic stamina.',
                'description': '10 miles steady Zone 2.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 7,
                'workout': 'Easy Run',
                'pace': '9:00 – 9:25 / mi',
                'hr_zone': 'Zone 1 (< 138 bpm)',
                'purpose': 'Active recovery.',
                'description': '7 easy miles.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Rest',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Pre-long run fueling.',
                'description': 'Full rest day.'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 18,
                'workout': 'Long Run with 8 Miles @ Goal Marathon Pace (7:26)',
                'pace': '8mi easy @ 8:40/mi + 8mi continuous @ 7:26 MP + 2mi cool',
                'hr_zone': 'MP block: Zone 3 (151 – 155 bpm)',
                'purpose': 'Major marathon simulation: holding 7:26 pace for over an hour in the middle of an 18-miler.',
                'description': '8 miles easy (8:40/mi). Shift smoothly into 7:26/mile for 8 continuous miles (miles 9 through 16). Take an energy gel at mile 8 and mile 13. 2 miles easy cooldown.'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 5,
                'workout': 'Recovery Shakeout',
                'pace': '9:15 – 9:45 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Completing 54-mile week.',
                'description': '5 gentle recovery miles.'
            }
        ],

        16: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 0,
                'workout': 'Rest & Recovery',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Freshening up for critical Half Marathon benchmark.',
                'description': 'Rest day.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 8,
                'workout': 'Easy Aerobic Run',
                'pace': '8:50 – 9:15 / mi',
                'hr_zone': 'Zone 2 (< 140 bpm)',
                'purpose': 'Aerobic maintenance without fatigue.',
                'description': '8 easy miles.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 8,
                'workout': 'Easy Run + 4x100m Strides',
                'pace': '8:50 – 9:15 / mi',
                'hr_zone': 'Zone 2 (< 140 bpm)',
                'purpose': 'Neuromuscular priming.',
                'description': '7.5 miles easy + 4 strides.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 6,
                'workout': 'Easy Shakeout + Race Pace Openers',
                'pace': '9:00/mi with 4 x 30s openers @ 7:00/mi',
                'hr_zone': 'Zone 1/2 (< 140 bpm)',
                'purpose': 'Waking up neuromuscular coordination for race day.',
                'description': '5.5 miles very easy with 4 x 30-second surges at target half marathon race pace.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Rest & Carbo-Loading',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Glycogen loading and hydration.',
                'description': 'Full rest. Eat high-carb meals, hydrate with electrolytes.'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 4,
                'workout': 'Pre-Race Shakeout Jog',
                'pace': '9:00 – 9:30 / mi + 3 light strides',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Loosening up legs.',
                'description': '4 easy miles. Prepare racing singlet, bib, and shoes.'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 18,
                'workout': '🌟 BENCHMARK 3 (CRITICAL): Half Marathon Race',
                'pace': '2mi warm + 13.1mi Race @ 7:05 – 7:08/mi + 2.9mi cool',
                'hr_zone': 'Race: Zone 4 (162 – 170 bpm)',
                'purpose': 'The Definitive 3:15 Predictor: Sub-1:33:30 validates Daniels VDOT 50.5!',
                'description': '2 miles easy warmup with dynamic stretching. Race 13.1 miles at target 7:05–7:08 pace (Goal: sub-1:33:30). Take a gel at mile 7. Finish with 2.9 miles very easy cooldown. Total: 18 miles.'
            }
        ],

        # PHASE 4: WEEKS 17-20 (Peak Volume & Simulation)
        17: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 4,
                'workout': 'Gentle Post-Race Shakeout',
                'pace': '9:20 – 9:50 / mi',
                'hr_zone': 'Zone 1 (< 133 bpm)',
                'purpose': 'Post-half marathon muscle repair and blood flow.',
                'description': '4 slow, gentle recovery miles.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 10,
                'workout': 'Steady Aerobic on Rolling Hills',
                'pace': '8:40 – 9:05 / mi',
                'hr_zone': 'Zone 2 (138 – 145 bpm)',
                'purpose': 'Aerobic volume rebuild.',
                'description': '10 miles comfortable rolling hills.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 11,
                'workout': 'Midweek Long Run',
                'pace': '8:35 – 9:00 / mi',
                'hr_zone': 'Zone 2 (138 – 146 bpm)',
                'purpose': 'Volume anchor.',
                'description': '11 miles steady Zone 2.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 7,
                'workout': 'Easy Recovery Run',
                'pace': '9:00 – 9:30 / mi',
                'hr_zone': 'Zone 1 (< 138 bpm)',
                'purpose': 'Active recovery.',
                'description': '7 easy miles.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Rest',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Rest.',
                'description': 'Full rest day.'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 17,
                'workout': 'Steady Aerobic Long Run',
                'pace': '8:40 – 9:05 / mi',
                'hr_zone': 'Zone 2 (140 – 148 bpm)',
                'purpose': 'Aerobic consolidation and fat oxidation.',
                'description': '17 miles steady aerobic cruising. Fueling every 40 minutes.'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 5,
                'workout': 'Recovery Shakeout',
                'pace': '9:15 – 9:45 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Completing 54-mile week.',
                'description': '5 gentle recovery miles.'
            }
        ],

        18: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 4,
                'workout': 'Recovery Shakeout',
                'pace': '9:20 – 9:50 / mi',
                'hr_zone': 'Zone 1 (< 133 bpm)',
                'purpose': 'Active recovery.',
                'description': '4 easy miles.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 10,
                'workout': 'Threshold Cruise Intervals: 4 x 1.5 Miles',
                'pace': '2mi warm + 4 x 1.5mi @ 6:55 – 7:00/mi (90s rest) + 2mi cool',
                'hr_zone': 'Intervals: Zone 4 (161 – 166 bpm)',
                'purpose': 'Sub-7:00 threshold mastery: 6 cumulative miles under 7:00 pace.',
                'description': '2 miles easy warmup. 4 x 1.5 miles at 6:55–7:00/mi with 90 seconds jogging recovery. 2 miles easy cooldown.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 11,
                'workout': 'Midweek Aerobic Base',
                'pace': '8:30 – 8:55 / mi',
                'hr_zone': 'Zone 2 (138 – 145 bpm)',
                'purpose': 'High aerobic density.',
                'description': '11 miles steady Zone 2.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 7,
                'workout': 'Easy Aerobic Run',
                'pace': '9:00 – 9:25 / mi',
                'hr_zone': 'Zone 1 (< 138 bpm)',
                'purpose': 'Active recovery.',
                'description': '7 easy miles.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Rest',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Preparation for full LA Marathon Dress Rehearsal.',
                'description': 'Full rest day. Pre-hydrate and eat race-style dinner.'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 19,
                'workout': '🌟 FULL LA MARATHON DRESS REHEARSAL',
                'pace': '9mi easy @ 8:35/mi + 8mi continuous @ 7:26 Goal MP + 2mi cool',
                'hr_zone': 'MP block: Zone 3 (< 155 bpm)',
                'purpose': 'The ultimate rehearsal: exact race shoes, race breakfast, gel every 35m, sodium check.',
                'description': 'Wake up at race hour. Eat exact race breakfast (e.g. oatmeal + banana). Wear target marathon racing shoes. Run 9 miles easy (8:35/mi). Then lock into 7:26 Goal Marathon Pace for 8 continuous miles (miles 10 through 17). Take gel at 35m, 70m, and 105m. Finish with 2 miles cooldown. Target HR at 7:26: < 155 bpm!'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 5,
                'workout': 'Recovery Shakeout',
                'pace': '9:15 – 9:45 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Completing 56 miles.',
                'description': '5 gentle recovery miles.'
            }
        ],

        19: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 4,
                'workout': 'Recovery Shakeout',
                'pace': '9:20 – 9:50 / mi',
                'hr_zone': 'Zone 1 (< 133 bpm)',
                'purpose': 'Active recovery.',
                'description': '4 easy miles.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 10,
                'workout': 'Extended Threshold Tempo: 2 x 3 Miles',
                'pace': '2mi warm + 2 x 3mi @ 7:15/mi (3 min rest) + 2mi cool',
                'hr_zone': 'Tempo blocks: Zone 4 (160 – 165 bpm)',
                'purpose': 'Stamina under peak-cycle chronic volume fatigue.',
                'description': '2 miles easy warmup. Rep 1: 3 miles at 7:15/mi. Jog 3 minutes. Rep 2: 3 miles at 7:15/mi. 2 miles easy cooldown.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 11,
                'workout': 'Midweek Long Run',
                'pace': '8:35 – 9:00 / mi',
                'hr_zone': 'Zone 2 (138 – 146 bpm)',
                'purpose': 'Volume.',
                'description': '11 miles steady Zone 2.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 7,
                'workout': 'Easy Aerobic Run',
                'pace': '9:00 – 9:25 / mi',
                'hr_zone': 'Zone 1 (< 138 bpm)',
                'purpose': 'Active recovery.',
                'description': '7 easy miles.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Rest',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Rest before the longest run of the training block.',
                'description': 'Full rest day. Hydrate thoroughly.'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 21,
                'workout': '🌟 PEAK LONG RUN (THE 21-MILER)',
                'pace': '8:35 – 9:00 / mi steady conversational',
                'hr_zone': 'Zone 2 (140 – 148 bpm)',
                'purpose': 'Maximum glycogen depletion adaptation, psychological barrier broken; decoupling target < 4.5%.',
                'description': 'The longest run of the entire cycle. Settle into smooth, disciplined aerobic cruising (8:35–9:00/mi). Consume an energy gel every 40 minutes (min 40, 80, 120, 150) with water. Proves you can cover 21 miles with zero bonking.'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 5,
                'workout': 'Recovery Shakeout',
                'pace': '9:20 – 9:50 / mi',
                'hr_zone': 'Zone 1 (< 133 bpm)',
                'purpose': 'Peak volume achieved: 58-mile week in the books!',
                'description': '5 very easy recovery miles. Celebrate hitting peak training volume!'
            }
        ],

        20: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 4,
                'workout': 'Recovery Shakeout',
                'pace': '9:20 – 9:50 / mi',
                'hr_zone': 'Zone 1 (< 133 bpm)',
                'purpose': 'Active recovery.',
                'description': '4 easy miles.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 9,
                'workout': 'Aerobic Base + 6x100m Strides',
                'pace': '8:40 – 9:05 / mi + strides',
                'hr_zone': 'Zone 2 (< 140 bpm)',
                'purpose': 'Neuromuscular maintenance.',
                'description': '8.5 miles easy. 6 fast, relaxed 100m strides.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 10,
                'workout': 'Steady Aerobic Run',
                'pace': '8:30 – 8:55 / mi',
                'hr_zone': 'Zone 2 (138 – 145 bpm)',
                'purpose': 'Aerobic endurance.',
                'description': '10 miles steady Zone 2.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 7,
                'workout': 'Easy Run',
                'pace': '9:00 – 9:25 / mi',
                'hr_zone': 'Zone 1 (< 138 bpm)',
                'purpose': 'Active recovery.',
                'description': '7 easy miles.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Rest',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Rest before final high-volume stimulus.',
                'description': 'Full rest day.'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 17,
                'workout': 'Alternating Long Run: 1mi Easy / 1mi MP',
                'pace': '8 miles of alternating (1mi @ 8:15 / 1mi @ 7:20 MP) + warm/cool',
                'hr_zone': 'Alternating Zone 2 and Zone 3 (140 to 154 bpm)',
                'purpose': 'Lactate clearance dynamics and pace variability under volume fatigue.',
                'description': '4.5 miles warmup @ 8:40/mi. Then alternate 8 miles: 1 mile @ 8:15 / 1 mile @ 7:20 MP (4 cycles). 4.5 miles easy cooldown. Final high-volume stimulus before 3-week taper!'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 5,
                'workout': 'Recovery Shakeout',
                'pace': '9:15 – 9:45 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Completing 52 miles. Phase 4 Peak Volume complete!',
                'description': '5 gentle recovery miles.'
            }
        ],

        # PHASE 5: WEEKS 21-23 (Sharpening, Taper & Race Day)
        21: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 0,
                'workout': 'Rest & Recovery (Taper Begins)',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Systemic recovery begins. Muscle fibers start repairing and storing supercompensated glycogen.',
                'description': 'Full rest day. Muscle tissue remodeling begins. Hydrate well.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 8,
                'workout': 'Taper Sharpener: 3 x 1 Mile',
                'pace': '2mi warm + 3 x 1mi @ 7:00/mi (2 min rest) + 3mi cool',
                'hr_zone': 'Intervals: Zone 4 (160 – 165 bpm)',
                'purpose': 'Maintaining neuromuscular speed while volume drops by 25%.',
                'description': '2 miles easy warmup. 3 x 1 mile at 7:00/mile with 2 full minutes walking/jogging recovery. Crisp, light, effortless. 3 miles easy cooldown.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 8,
                'workout': 'Aerobic Base Run',
                'pace': '8:40 – 9:05 / mi',
                'hr_zone': 'Zone 2 (< 140 bpm)',
                'purpose': 'Aerobic cruising with reduced volume.',
                'description': '8 miles easy conversational.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 6,
                'workout': 'Easy Run',
                'pace': '9:00 – 9:25 / mi',
                'hr_zone': 'Zone 1 (< 138 bpm)',
                'purpose': 'Active recovery.',
                'description': '6 easy recovery miles.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Rest',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Rest.',
                'description': 'Full rest day.'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 14,
                'workout': 'Taper Long Run with 4 Miles @ Goal MP (7:26)',
                'pace': '8mi easy @ 8:40/mi + 4mi @ 7:26 MP + 2mi cool',
                'hr_zone': 'MP block: Zone 3 (151 – 154 bpm)',
                'purpose': 'Locking into 7:26 marathon pace; should feel dramatically easier than in week 12!',
                'description': '8 miles easy. At mile 8, shift into 7:26/mile for 4 miles. Note how light and relaxed your legs feel. 2 miles easy cooldown.'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 4,
                'workout': 'Recovery Shakeout',
                'pace': '9:15 – 9:45 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Completing Taper Week 1 at 40 miles.',
                'description': '4 easy miles.'
            }
        ],

        22: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 0,
                'workout': 'Rest & Recovery',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Taper Week 2 (55% volume).',
                'description': 'Rest day. Prioritize 8+ hours of sleep.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 6,
                'workout': 'Speed Maintenance: 4 x 400m',
                'pace': '2mi warm + 4 x 400m @ 6:50/mi (~1:42) w/ 200m jog + 2.5mi cool',
                'hr_zone': 'Work reps: Zone 4/5 (Fast turnover, zero fatigue)',
                'purpose': 'High leg turnover and springiness with negligible fatigue.',
                'description': '2 miles easy warmup. 4 x 400m at 6:50/mile (~102 seconds) with 200m slow jog. Pure neuromuscular snap. 2.5 miles easy cooldown.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 6,
                'workout': 'Easy Aerobic Run',
                'pace': '8:45 – 9:15 / mi',
                'hr_zone': 'Zone 2 (< 138 bpm)',
                'purpose': 'Easy movement.',
                'description': '6 comfortable easy miles.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 4,
                'workout': 'Easy Shakeout',
                'pace': '9:00 – 9:30 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Active recovery.',
                'description': '4 very easy miles.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Rest',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Rest.',
                'description': 'Full rest day.'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 9,
                'workout': 'Short Long Run with 2 Miles @ Goal MP',
                'pace': '6mi easy @ 8:45/mi + 2mi @ 7:26 MP + 1mi cool',
                'hr_zone': 'Zone 2 / Zone 3',
                'purpose': 'Final rehearsal of 7:26 pace rhythm before race week.',
                'description': '6 miles easy. 2 miles at 7:26 Goal Marathon Pace. 1 mile cooldown. Legs should feel coiled, rested, and springy.'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 3,
                'workout': 'Recovery Shakeout',
                'pace': '9:20 – 9:50 / mi',
                'hr_zone': 'Zone 1 (< 133 bpm)',
                'purpose': 'Completing Taper Week 2 at 28 miles.',
                'description': '3 very easy recovery miles.'
            }
        ],

        23: [
            {
                'day': 'Mon', 'day_full': 'Monday', 'miles': 0,
                'workout': 'Rest & Race Week Hydration Protocol',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Beginning final carbo-loading and electrolyte saturation.',
                'description': 'Full rest. Start sipping water with electrolytes. Avoid heavy fiber.'
            },
            {
                'day': 'Tue', 'day_full': 'Tuesday', 'miles': 5,
                'workout': 'Easy Aerobic Shakeout',
                'pace': '8:50 – 9:20 / mi',
                'hr_zone': 'Zone 2 (< 138 bpm)',
                'purpose': 'Keeps blood flowing and muscles loose.',
                'description': '5 very easy miles. Completely relaxed breathing.'
            },
            {
                'day': 'Wed', 'day_full': 'Wednesday', 'miles': 4,
                'workout': 'Easy Jog',
                'pace': '9:00 – 9:30 / mi',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Easy movement.',
                'description': '4 easy miles.'
            },
            {
                'day': 'Thu', 'day_full': 'Thursday', 'miles': 4,
                'workout': 'Easy Run + 4 x 20-Second Strides',
                'pace': '9:00 / mi + 4 light strides',
                'hr_zone': 'Zone 1/2 (< 138 bpm)',
                'purpose': 'Wakes up fast-twitch neuromuscular coordination.',
                'description': '3.5 miles very easy + 4 x 20-second strides at marathon pace with full walking recovery.'
            },
            {
                'day': 'Fri', 'day_full': 'Friday', 'miles': 0,
                'workout': 'Travel to LA & Rest',
                'pace': 'Rest',
                'hr_zone': 'Rest (< 100 bpm)',
                'purpose': 'Travel, expo, and resting legs.',
                'description': 'Travel to Los Angeles. Pick up race bib at expo quickly; stay off your feet as much as possible! High carbohydrate intake (8–10g carbs / kg body weight).'
            },
            {
                'day': 'Sat', 'day_full': 'Saturday', 'miles': 3,
                'workout': 'Pre-Race Shakeout Jog in Los Angeles',
                'pace': '9:15 – 9:45 / mi + 3 light strides',
                'hr_zone': 'Zone 1 (< 135 bpm)',
                'purpose': 'Flushing travel stiffness and checking race morning gear.',
                'description': '3 very easy miles around your hotel in LA. 3 light strides. Pin bib to singlet, lay out shoes and gels. Early lights out by 9:30 PM.'
            },
            {
                'day': 'Sun', 'day_full': 'Sunday', 'miles': 28.2,
                'workout': '🌟 LOS ANGELES MARATHON 2027 (RACE DAY)',
                'pace': '2mi warm shakeout + 26.2mi @ 7:26 / mi ➔ 3:15:00 GOAL',
                'hr_zone': 'Miles 1-5: 148-152 bpm | Miles 6-19: 152-155 bpm | Miles 20-26.2: 156-164 bpm',
                'purpose': 'EXECUTING SUB-3:15:00 MARATHON MASTERY!',
                'description': 'Race Morning: Wake up 3.5h before start. Eat familiar high-carb breakfast. 2-mile light warmup shakeout at Dodger Stadium.\\n'
                             'Miles 1–5: Down Sunset Blvd (-150 ft). RESIST THE CROWD! Lock in 7:30–7:35/mi to protect your quads.\\n'
                             'Miles 6–19: Hollywood to Beverly Hills. Settle into 7:24–7:26/mi cruise control. Gel every 35 mins with water.\\n'
                             'Miles 20–22: San Vicente false flat climb. Run by HR (< 160 bpm), accept 7:30–7:35/mi without panic.\\n'
                             'Miles 23–26.2: Final descent into Century City. Unleash your Seattle hill power! Drop pace to 7:15–7:20/mi across Avenue of the Stars to cross the line in 3:14:xx!'
            }
        ]
    }
    raw_days = plans.get(week_num, [])
    return apply_lifting_schedule(week_num, raw_days)

def apply_lifting_schedule(week_num, days, total_weeks=23):
    """
    Enriches the 7 daily workouts with concurrent strength training strictly enforcing
    ZERO TWO-A-DAYS (never run and lift on the same day):
    - Monday (Non-running day): Upper Body (Push/Pull) + Anti-Extension Core (NO RUNNING)
    - Tuesday: Quality Run / Intervals / Threshold (RUN ONLY - NO LIFTING)
    - Wednesday: Midweek Aerobic Base / Medium Long Run (RUN ONLY - NO LIFTING)
    - Thursday (Non-running day):
        * Odd Weeks (1/2w): 🏋️ Bi-Weekly Heavy Leg Strength (NO RUNNING)
        * Even Weeks: 🧘 Core & Pelvic Hip Stability (NO RUNNING)
        * Taper W1: 🏋️ Taper Leg Strength (50% volume, high velocity)
        * Taper W2: 🧘 Light Core & Mobility (no weights)
        * Race Week: Pure rest & mobility
    - Friday: Easy Pre-Long Run Shakeout (RUN ONLY - NO LIFTING)
    - Saturday: Anchor Long Run (RUN ONLY - NO LIFTING)
    - Sunday: Aerobic Recovery Shakeout (RUN ONLY - NO LIFTING)
    """
    import copy
    enriched = copy.deepcopy(days)
    d_map = {d['day']: d for d in enriched}
    day_thu = d_map.get('Thu')
    day_fri = d_map.get('Fri')
    day_mon = d_map.get('Mon')
    day_wed = d_map.get('Wed')
    day_sat = d_map.get('Sat')
    day_sun = d_map.get('Sun')

    # 1. Shift Thursday run miles to Friday so Thursday is 100% non-running
    if day_thu and day_fri and day_thu['miles'] > 0 and day_fri['miles'] == 0:
        day_fri['miles'] = day_thu['miles']
        day_fri['workout'] = 'Easy Pre-Long Run Shakeout'
        day_fri['pace'] = day_thu.get('pace', '9:00 – 9:30 / mi')
        day_fri['hr_zone'] = 'Zone 1 / Low Zone 2 (< 138 bpm)'
        day_fri['purpose'] = 'Gentle active recovery flush of legs following Thursday strength session, priming for Saturday long run.'
        day_fri['description'] = 'Relaxed conversational recovery run on flat terrain. Promotes capillary circulation, flushes metabolites from Thursday lifting, and primes legs for tomorrow anchor. ZERO lifting.'
        day_thu['miles'] = 0
        day_thu['pace'] = 'Rest / Strength'
        day_thu['hr_zone'] = 'Rest / Gym (< 130 bpm)'
        day_thu['purpose'] = 'Targeted neuromuscular recruitment and eccentric resilience without running impact.'

    # 2. If Monday had miles > 0 (high-volume weeks), shift those miles so Monday is 100% non-running
    if day_mon and day_mon['miles'] > 0:
        extra = day_mon['miles']
        day_mon['miles'] = 0
        day_mon['pace'] = 'Rest / Strength'
        day_mon['hr_zone'] = 'Rest / Gym (< 130 bpm)'
        day_mon['purpose'] = 'Upper body muscular endurance and core stability without leg fatigue.'
        if day_sat and extra >= 2:
            day_sat['miles'] += 2
            extra -= 2
        if day_wed and extra >= 1:
            day_wed['miles'] += 1
            extra -= 1
        if day_sun and extra >= 1:
            day_sun['miles'] += extra
            extra = 0
        elif day_fri and extra > 0:
            day_fri['miles'] += extra
            extra = 0

    taper_w1 = total_weeks - 2
    taper_w2 = total_weeks - 1
    race_week = total_weeks

    for d in enriched:
        day_name = d.get('day')

        # MONDAY: Lift Only (Upper Body & Core)
        if day_name == 'Mon':
            if week_num < race_week:
                d['lifting_type'] = 'Upper Body & Core Strength (No Running)'
                d['lifting_exercises'] = 'Dumbbell Bench/Overhead Press (3x8), Pull-ups or Lat Pulldowns (3x8), Cable Rows (3x10), Pallof Press (3x12/side), Deadbugs (3x10/side). No heavy leg loading.'
                d['workout'] = 'Rest from Running • Upper Body & Core Strength'
                d['description'] = 'Non-running day: Upper Body Push/Pull + Core stability. Keep effort controlled (RIR 2-3). 15 min foam rolling. Keeps legs fresh for Tuesday quality run. Zero running.'
            else:
                d['lifting_type'] = None
                d['lifting_exercises'] = 'Race week rest and mobility only.'
                d['workout'] = 'Rest from Running • Race Week Rest & Mobility'
                d['description'] = 'Full rest day. Light stretching, hydration, and carbo-loading. Zero lifting.'

        # THURSDAY: Lift Only (Legs 1/2w on Odd Weeks, Core on Even Weeks)
        elif day_name == 'Thu':
            if week_num < taper_w1 and (week_num % 2 == 1):
                d['lifting_type'] = '🏋️ Bi-Weekly Heavy Leg Strength (No Running)'
                d['lifting_exercises'] = 'Trap Bar Deadlift (3x5 @ 75-80%), Bulgarian Split Squats (3x6/leg with dumbbells), Standing Heavy Calf Raises (3x10), Box Jumps (3x5 explosive). Leave 2-3 RIR (never to failure!).'
                d['workout'] = 'Rest from Running • 🏋️ Bi-Weekly Heavy Leg Strength'
                d['description'] = 'Non-running day: Bi-Weekly Heavy Resistance Leg Strength. Low reps (3-5), heavy weight, explosive intent. Trap Bar Deadlifts, Bulgarian Split Squats, Heavy Calf Raises, Box Jumps. Zero running today ensures complete energy for neuromuscular recruitment without fatigue. Friday is an easy recovery run to flush legs before Saturday.'
            elif week_num < taper_w1 and (week_num % 2 == 0):
                d['lifting_type'] = '🧘 Core & Pelvic Hip Stability (No Running)'
                d['lifting_exercises'] = 'Copenhagen Adductor Planks (3x20s/side), Side Planks with Leg Lift (3x30s), Single-Leg RDLs (light dumbbell, 3x8/leg), Banded Glute Bridges (3x12). Zero heavy eccentric leg loading.'
                d['workout'] = 'Rest from Running • 🧘 Core & Pelvic Hip Stability'
                d['description'] = 'Non-running day: Hip stability, glute activation, and rotational core. Strengthens adductors and gluteus medius to stabilize pelvis and protect IT bands during high marathon mileage without heavy leg fatigue.'
            elif week_num == taper_w1:
                d['lifting_type'] = '🏋️ Taper Leg Strength (50% Volume)'
                d['lifting_exercises'] = 'Trap Bar Deadlift (2x4 light/moderate), Bodyweight Split Squats (2x5), Standing Calf Raises (2x8). High movement velocity, low fatigue.'
                d['workout'] = 'Rest from Running • 🏋️ Taper Leg Strength (50% Volume)'
                d['description'] = 'Non-running day: 50% cutback in lifting volume. Maintains neuromuscular snap while allowing deep muscle recovery.'
            elif week_num == taper_w2:
                d['lifting_type'] = '🧘 Light Core & Mobility'
                d['lifting_exercises'] = 'Deadbugs, bird-dogs, thoracic mobility, gentle hip openers. No weights.'
                d['workout'] = 'Rest from Running • 🧘 Light Core & Mobility'
                d['description'] = 'Non-running day: Light core activation and mobility only. Zero weights.'
            else:
                d['lifting_type'] = None
                d['lifting_exercises'] = 'Race week rest and mobility only.'
                d['workout'] = 'Rest from Running • Pre-Race Rest & Mobility'
                d['description'] = 'Full rest day. Light stretching, hydration, and carbo-loading. Zero lifting.'

        # WEDNESDAY: Run Only (Zero Lifting)
        elif day_name == 'Wed':
            d['lifting_type'] = None
            d['lifting_exercises'] = None
            d['workout'] = d['workout'].split(' + ')[0].split(' • ')[0]
            if 'PM STRENGTH' in d['description']:
                d['description'] = d['description'].split('PM STRENGTH')[0].strip()

        # TUE, FRI, SAT, SUN: Run Only (Zero Lifting)
        elif day_name in ('Tue', 'Fri', 'Sat', 'Sun'):
            d['lifting_type'] = None
            d['lifting_exercises'] = None
            if day_name == 'Fri' and 'Rest from Running' in d['workout']:
                d['workout'] = 'Easy Pre-Long Run Shakeout'

    return enriched

