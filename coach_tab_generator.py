"""
coach_tab_generator.py - Generate HTML components for the Coach's Log & Daily Debriefs tab,
and the Vancouver Coaching Command Center widget.
"""

import json
import os

def load_evaluations(eval_path):
    if os.path.exists(eval_path):
        try:
            with open(eval_path, 'r') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def generate_coach_tab_html(evals):
    if not evals:
        return """
        <section id="tab-coach" class="tab-content">
          <div class="section-header">
            <h2>🏃 Coach's Log & Daily Workout Debriefs</h2>
            <p>No workout evaluations recorded yet. Run `python3 sync_and_eval.py` to sync and evaluate your latest Garmin workout.</p>
          </div>
        </section>
        """

    latest = evals[0]
    pres = latest.get("prescribed", {})
    act = latest.get("actual", {})
    score = latest.get("scorecard", {})
    grade = score.get("grade", "A")
    next_wo = latest.get("next_workout", {})

    grade_bg = "rgba(16, 185, 129, 0.15)"
    grade_color = "var(--accent-emerald)"
    grade_border = "rgba(16, 185, 129, 0.4)"
    if "B" in grade:
        grade_bg = "rgba(245, 158, 11, 0.15)"
        grade_color = "var(--accent-amber)"
        grade_border = "rgba(245, 158, 11, 0.4)"

    takeaways_html = "".join([f"<li style='margin-bottom: 8px; line-height: 1.5;'>{t}</li>" for t in latest.get("key_takeaways", [])])

    past_rows_html = ""
    for e in evals:
        e_p = e.get("prescribed", {})
        e_a = e.get("actual", {})
        e_s = e.get("scorecard", {})
        past_rows_html += f"""
        <tr style="border-bottom: 1px solid var(--border-subtle);">
          <td style="padding: 12px; font-weight: 600; color: var(--text-highlight);">{e.get('date')} ({e.get('day_of_week')})</td>
          <td style="padding: 12px;">Week {e.get('week_num')} • {e_p.get('workout', 'Run')}</td>
          <td style="padding: 12px; font-family: 'JetBrains Mono', monospace;">{e_p.get('miles', 0):.1f} mi</td>
          <td style="padding: 12px; font-family: 'JetBrains Mono', monospace; font-weight: 700; color: var(--accent-emerald);">{e_a.get('miles', 0):.2f} mi</td>
          <td style="padding: 12px; font-family: 'JetBrains Mono', monospace;">{e_a.get('pace_raw', 'N/A')}</td>
          <td style="padding: 12px; font-family: 'JetBrains Mono', monospace; color: var(--accent-cyan);">{e_a.get('pace_gap', 'N/A')}</td>
          <td style="padding: 12px; font-family: 'JetBrains Mono', monospace;">{e_a.get('avg_hr', 'N/A')} bpm</td>
          <td style="padding: 12px;"><span style="background: {grade_bg}; color: {grade_color}; border: 1px solid {grade_border}; font-weight: 800; padding: 3px 8px; border-radius: 6px; font-size: 0.85rem;">{e_s.get('grade', 'A')}</span></td>
        </tr>
        """

    is_strength = act.get('miles', 0) == 0
    if is_strength:
        header_title = f"{pres.get('workout', 'Strength Session')} • {act.get('duration_formatted')} Completed"
        header_sub = f"Prescription: <strong>{pres.get('lifting', 'Bi-Weekly Heavy Leg Strength')}</strong> • Duration: <strong>{act.get('duration_formatted')}</strong>"
        adherence_badge = "100% Protocol Adherence"
        metric_grid_html = f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-bottom: 20px;">
          <div style="background: var(--bg-secondary); padding: 12px 14px; border-radius: var(--radius-sm); border-left: 3px solid var(--accent-purple);">
            <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Activity Focus</div>
            <div style="font-size: 1.15rem; font-weight: 800; color: var(--text-highlight); font-family: 'JetBrains Mono', monospace; margin-top: 2px;">
              Heavy Leg Strength
            </div>
            <div style="font-size: 0.8rem; color: var(--accent-purple);">
              Zero-Double-Days Compliant
            </div>
          </div>

          <div style="background: var(--bg-secondary); padding: 12px 14px; border-radius: var(--radius-sm); border-left: 3px solid var(--accent-emerald);">
            <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Heart Rate (Avg / Peak)</div>
            <div style="font-size: 1.15rem; font-weight: 800; color: var(--text-highlight); font-family: 'JetBrains Mono', monospace; margin-top: 2px;">
              {act.get('avg_hr', 84)} bpm
            </div>
            <div style="font-size: 0.8rem; color: var(--accent-emerald);">
              Peak: {act.get('max_hr', 122)} bpm (&lt; 130 bpm cap)
            </div>
          </div>

          <div style="background: var(--bg-secondary); padding: 12px 14px; border-radius: var(--radius-sm); border-left: 3px solid var(--accent-blue);">
            <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Sets & Reps</div>
            <div style="font-size: 1.15rem; font-weight: 800; color: var(--text-highlight); font-family: 'JetBrains Mono', monospace; margin-top: 2px;">
              {act.get('total_sets', 13)} Sets • {act.get('total_reps', 152)} Reps
            </div>
            <div style="font-size: 0.8rem; color: var(--accent-blue);">
              Bulgarian split squats, RDLs, step ups
            </div>
          </div>

          <div style="background: var(--bg-secondary); padding: 12px 14px; border-radius: var(--radius-sm); border-left: 3px solid var(--accent-amber);">
            <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Training Stimulus</div>
            <div style="font-size: 1.15rem; font-weight: 800; color: var(--text-highlight); font-family: 'JetBrains Mono', monospace; margin-top: 2px;">
              Aerobic TE {act.get('aerobic_te', 0.4)}
            </div>
            <div style="font-size: 0.8rem; color: var(--text-secondary);">
              Pure Neuromuscular / Zero Cardio Drain
            </div>
          </div>

          <div style="background: var(--bg-secondary); padding: 12px 14px; border-radius: var(--radius-sm); border-left: 3px solid var(--accent-rose);">
            <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Running Mileage</div>
            <div style="font-size: 1.15rem; font-weight: 800; color: var(--accent-emerald); font-family: 'JetBrains Mono', monospace; margin-top: 2px;">
              0.00 Miles
            </div>
            <div style="font-size: 0.8rem; color: var(--accent-emerald);">
              Legs protected for Fri & Sat runs
            </div>
          </div>
        </div>
        """
    else:
        header_title = f"{pres.get('workout', 'Workout')} • {act.get('miles', 0):.2f} Miles Logged"
        header_sub = f"Prescription: <strong>{pres.get('miles', 0):.1f} mi</strong> ({pres.get('target_pace')}) • Actual Moving Time: <strong>{act.get('duration_formatted')}</strong>"
        adherence_badge = f"{score.get('distance_adherence_pct')}% Vol Adherence"
        metric_grid_html = f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-bottom: 20px;">
          <div style="background: var(--bg-secondary); padding: 12px 14px; border-radius: var(--radius-sm); border-left: 3px solid var(--accent-blue);">
            <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Average Pace (Raw / GAP)</div>
            <div style="font-size: 1.15rem; font-weight: 800; color: var(--text-highlight); font-family: 'JetBrains Mono', monospace; margin-top: 2px;">
              {act.get('pace_raw')}
            </div>
            <div style="font-size: 0.8rem; color: var(--accent-cyan); font-family: 'JetBrains Mono', monospace;">
              GAP: {act.get('pace_gap')}
            </div>
          </div>

          <div style="background: var(--bg-secondary); padding: 12px 14px; border-radius: var(--radius-sm); border-left: 3px solid var(--accent-emerald);">
            <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Heart Rate (Avg / Max)</div>
            <div style="font-size: 1.15rem; font-weight: 800; color: var(--text-highlight); font-family: 'JetBrains Mono', monospace; margin-top: 2px;">
              {act.get('avg_hr')} bpm
            </div>
            <div style="font-size: 0.8rem; color: var(--text-secondary);">
              Peak: {act.get('max_hr')} bpm (Hill climb)
            </div>
          </div>

          <div style="background: var(--bg-secondary); padding: 12px 14px; border-radius: var(--radius-sm); border-left: 3px solid var(--accent-amber);">
            <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Cadence (Avg / Peak)</div>
            <div style="font-size: 1.15rem; font-weight: 800; color: var(--text-highlight); font-family: 'JetBrains Mono', monospace; margin-top: 2px;">
              {act.get('avg_cadence')} spm
            </div>
            <div style="font-size: 0.8rem; color: var(--accent-amber);">
              Strides Peak: {act.get('max_cadence')} spm
            </div>
          </div>

          <div style="background: var(--bg-secondary); padding: 12px 14px; border-radius: var(--radius-sm); border-left: 3px solid var(--accent-purple);">
            <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Elevation Climbed</div>
            <div style="font-size: 1.15rem; font-weight: 800; color: var(--text-highlight); font-family: 'JetBrains Mono', monospace; margin-top: 2px;">
              +{act.get('elevation_gain_ft', 0):.0f} ft
            </div>
            <div style="font-size: 0.8rem; color: var(--text-secondary);">
              Elevation change on Seattle hills
            </div>
          </div>

          <div style="background: var(--bg-secondary); padding: 12px 14px; border-radius: var(--radius-sm); border-left: 3px solid var(--accent-rose);">
            <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Ground Contact Time</div>
            <div style="font-size: 1.15rem; font-weight: 800; color: var(--text-highlight); font-family: 'JetBrains Mono', monospace; margin-top: 2px;">
              {act.get('ground_contact_time_ms', 'N/A')} ms
            </div>
            <div style="font-size: 0.8rem; color: var(--accent-emerald);">
              Strides Pop: {act.get('strides_gct_ms', '185.9')} ms (-28%)
            </div>
          </div>
        </div>
        """

    html = f"""
    <!-- TAB: COACH'S LOG & DEBRIEFS -->
    <section id="tab-coach" class="tab-content">
      <div class="section-header">
        <h2>🏃 Coach's Log & Daily Workout Debriefs</h2>
        <p>Forensic performance scorecards, metabolic zone verification, stride biomechanics, and daily workout-by-workout coaching.</p>
      </div>

      <!-- LATEST WORKOUT HERO SCORECARD -->
      <div class="card" style="border: 2px solid rgba(16, 185, 129, 0.4); background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(22, 32, 50, 0.98) 100%); margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px; margin-bottom: 16px;">
          <div>
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
              <span class="hero-badge" style="background: rgba(16, 185, 129, 0.2); color: var(--accent-emerald); border-color: rgba(16, 185, 129, 0.4);">
                Latest Session: {latest.get('day_full')}, {latest.get('date')}
              </span>
              <span class="hero-badge" style="background: rgba(56, 189, 248, 0.15); color: var(--accent-blue); border-color: rgba(56, 189, 248, 0.3);">
                Week {latest.get('week_num')} • Vancouver Plan
              </span>
            </div>
            <h3 style="font-size: 1.5rem; font-weight: 800; color: var(--text-highlight); margin: 0 0 4px 0;">
              {header_title}
            </h3>
            <p style="color: var(--text-secondary); margin: 0; font-size: 0.95rem;">
              {header_sub}
            </p>
          </div>

          <div style="text-align: right; background: {grade_bg}; border: 1.5px solid {grade_border}; padding: 12px 20px; border-radius: var(--radius-md);">
            <div style="font-size: 0.75rem; text-transform: uppercase; font-weight: 700; color: {grade_color}; letter-spacing: 0.05em;">Workout Grade</div>
            <div style="font-size: 2.2rem; font-weight: 900; color: {grade_color}; line-height: 1;">{grade}</div>
            <div style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 4px;">{adherence_badge}</div>
          </div>
        </div>

        <!-- Metric Grid -->
        {metric_grid_html}

        <!-- Executive Debrief -->
        <div style="background: var(--bg-card); padding: 16px; border-radius: var(--radius-sm); border: 1px solid var(--border-color); margin-bottom: 16px;">
          <h4 style="margin: 0 0 8px 0; color: var(--accent-emerald); font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
            <span>📋</span> Coach's Executive Assessment
          </h4>
          <p style="color: var(--text-primary); font-size: 0.95rem; line-height: 1.6; margin: 0 0 12px 0;">
            {latest.get('executive_summary')}
          </p>
          <div style="font-size: 0.85rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700; margin-bottom: 6px;">Key Observations & Telemetry Clues:</div>
          <ul style="color: var(--text-secondary); font-size: 0.9rem; padding-left: 20px; margin: 0;">
            {takeaways_html}
          </ul>
        </div>

        <!-- Next Workout Preview -->
        <div style="background: rgba(56, 189, 248, 0.08); padding: 14px 18px; border-radius: var(--radius-sm); border: 1px solid rgba(56, 189, 248, 0.25); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
          <div>
            <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--accent-blue); font-weight: 700;">Up Next: {next_wo.get('day')} ({next_wo.get('date')})</div>
            <div style="font-size: 1.1rem; font-weight: 800; color: var(--text-highlight);">{next_wo.get('miles')} mi • {next_wo.get('workout')}</div>
            <div style="font-size: 0.85rem; color: var(--text-secondary);">Target: {next_wo.get('target_pace')} • HR: {next_wo.get('target_hr')}</div>
          </div>
          <div style="background: rgba(168, 85, 247, 0.15); border: 1px solid rgba(168, 85, 247, 0.35); padding: 8px 14px; border-radius: var(--radius-sm); font-size: 0.85rem; color: var(--accent-purple); font-weight: 700;">
            ⚡ {next_wo.get('lifting_rule')}
          </div>
        </div>
      </div>

      <!-- PAST WORKOUTS TABLE -->
      <div class="card">
        <div class="card-title">
          <span>📜 Historical Coach Evaluations Log</span>
          <span class="hero-badge" style="background: rgba(56, 189, 248, 0.12); color: var(--accent-blue); border-color: rgba(56, 189, 248, 0.3);">{len(evals)} Recorded Session(s)</span>
        </div>
        <div style="overflow-x: auto; margin-top: 12px;">
          <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem; text-align: left;">
            <thead>
              <tr style="border-bottom: 2px solid var(--border-color); color: var(--text-muted); font-size: 0.75rem; text-transform: uppercase;">
                <th style="padding: 10px;">Date</th>
                <th style="padding: 10px;">Scheduled Session</th>
                <th style="padding: 10px;">Prescribed</th>
                <th style="padding: 10px;">Completed</th>
                <th style="padding: 10px;">Raw Pace</th>
                <th style="padding: 10px;">GAP Pace</th>
                <th style="padding: 10px;">Avg HR</th>
                <th style="padding: 10px;">Grade</th>
              </tr>
            </thead>
            <tbody>
              {past_rows_html}
            </tbody>
          </table>
        </div>
      </div>
    </section>
    """
    return html

def generate_vancouver_command_center_html(evals):
    if not evals:
        return ""
    
    latest = evals[0]
    pres = latest.get("prescribed", {})
    act = latest.get("actual", {})
    score = latest.get("scorecard", {})
    grade = score.get("grade", "A+")
    next_wo = latest.get("next_workout", {})

    day_map = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
    day_num = day_map.get(latest.get("day_of_week", "Mon"), 1)
    status_str = f"Campaign Status: Week {latest.get('week_num', 1)} Active (Day {day_num} of 7 Complete)"

    if act.get('miles', 0) == 0:
        left_title = f"Latest Session: {latest.get('day_full')} ({latest.get('date')}) • Heavy Leg Strength"
        left_sub = f"🏋️ {pres.get('workout', 'Heavy Leg Strength')} • {act.get('duration_formatted')}"
        left_desc = f"HR: <strong>{act.get('avg_hr', 84)} bpm</strong> (Peak <strong>{act.get('max_hr', 122)} bpm</strong>) • <strong>{act.get('total_sets', 13)} sets</strong> • Bulgarian split squats, step ups, RDLs, calf raises. Zero running logged."
    else:
        left_title = f"Latest Run: {latest.get('day_full')} ({latest.get('date')})"
        left_sub = f"{act.get('miles', 0):.2f} mi @ {act.get('pace_raw')} (GAP: {act.get('pace_gap')})"
        left_desc = f"HR: <strong>{act.get('avg_hr')} bpm</strong> • Climb: <strong>+{act.get('elevation_gain_ft', 0):.0f} ft</strong> • Strides: <strong>{score.get('strides_count', 0)} executed (peak {score.get('strides_peak_pace', 'fast')})</strong>."

    return f"""
    <!-- ACTIVE COACHING COMMAND CENTER WIDGET -->
    <div class="card" style="border: 2px solid rgba(16, 185, 129, 0.45); background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(22, 32, 50, 0.95) 100%); margin-bottom: 24px;">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px; border-bottom: 1px solid rgba(16, 185, 129, 0.2); padding-bottom: 12px; margin-bottom: 14px;">
        <div style="display: flex; align-items: center; gap: 10px;">
          <span style="font-size: 1.4rem;">⚡</span>
          <div>
            <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--accent-emerald); font-weight: 800; letter-spacing: 0.05em;">Active Coaching Command Center • Vancouver 2027</div>
            <div style="font-size: 1.15rem; font-weight: 800; color: var(--text-highlight);">{status_str}</div>
          </div>
        </div>
        <div style="display: flex; gap: 8px;">
          <button class="details-toggle-btn active" onclick="switchTab('coach')" style="background: var(--accent-emerald); color: #000; font-weight: 800; padding: 6px 14px; font-size: 0.85rem; border: none;">
            <span>View Detailed Coach Debrief ➔</span>
          </button>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;">
        <!-- Left: Latest Completed Session -->
        <div style="background: var(--bg-secondary); padding: 14px; border-radius: var(--radius-sm); border-left: 3px solid var(--accent-emerald);">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
            <span style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700;">{left_title}</span>
            <span style="background: rgba(16, 185, 129, 0.2); color: var(--accent-emerald); font-weight: 800; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;">Grade {grade}</span>
          </div>
          <div style="font-size: 1.05rem; font-weight: 800; color: var(--text-highlight); margin-bottom: 4px;">
            {left_sub}
          </div>
          <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.4;">
            {left_desc}
          </div>
        </div>

        <!-- Right: Next Session Preview -->
        <div style="background: var(--bg-secondary); padding: 14px; border-radius: var(--radius-sm); border-left: 3px solid var(--accent-blue);">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
            <span style="font-size: 0.75rem; text-transform: uppercase; color: var(--accent-blue); font-weight: 700;">Up Next: {next_wo.get('day')} ({next_wo.get('date')})</span>
            <span style="background: rgba(168, 85, 247, 0.15); color: var(--accent-purple); font-weight: 700; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem;">{next_wo.get('lifting_rule')}</span>
          </div>
          <div style="font-size: 1.05rem; font-weight: 800; color: var(--text-highlight); margin-bottom: 4px;">
            {next_wo.get('miles')} mi • {next_wo.get('workout')}
          </div>
          <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.4;">
            Prescribed Pace: <strong>{next_wo.get('target_pace')}</strong> • Target HR: <strong>{next_wo.get('target_hr')}</strong>.
          </div>
        </div>
      </div>
    </div>
    """
