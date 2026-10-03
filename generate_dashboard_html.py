#!/usr/bin/env python3
"""
generate_dashboard_html.py - Generate the standalone, fully interactive HTML dashboard
with embedded dashboard_data.json for zero-dependency viewing.
"""

import os
import json
import coach_tab_generator

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(REPO_DIR, "data/dashboard_data.json")
COACH_EVALS_FILE = os.path.join(REPO_DIR, "data/coach_evaluations.json")
OUTPUT_HTML = os.path.join(REPO_DIR, "index.html")

def generate():
    with open(DATA_FILE) as f:
        data_json_str = f.read()

    coach_evals = coach_tab_generator.load_evaluations(COACH_EVALS_FILE)
    coach_tab_html = coach_tab_generator.generate_coach_tab_html(coach_evals)
    vancouver_command_center_html = coach_tab_generator.generate_vancouver_command_center_html(coach_evals)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BMO Vancouver Marathon 2027: Sub-3:15 Training & Telemetry Dashboard</title>
  <!-- Chart.js for data visualization -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  
  <style>
    :root {{
      --bg-primary: #0a0f1d;
      --bg-secondary: #111827;
      --bg-card: #162032;
      --bg-card-hover: #1c2942;
      --border-color: #24324d;
      --border-subtle: #1e293b;
      
      --accent-blue: #38bdf8;
      --accent-emerald: #10b981;
      --accent-amber: #f59e0b;
      --accent-rose: #f43f5e;
      --accent-purple: #a855f7;
      --accent-cyan: #06b6d4;

      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;
      --text-highlight: #ffffff;

      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 16px;
      --radius-full: 9999px;
      --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.4);
      --shadow-md: 0 4px 20px rgba(0, 0, 0, 0.5);
      --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.6);
      --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--bg-primary);
      color: var(--text-primary);
      line-height: 1.5;
      padding-bottom: 80px;
      min-height: 100vh;
    }}

    /* Header & Hero */
    header {{
      background: linear-gradient(180deg, #131c31 0%, var(--bg-primary) 100%);
      border-bottom: 1px solid var(--border-color);
      padding: 32px 24px 24px;
    }}

    .header-container {{
      max-width: 1400px;
      margin: 0 auto;
    }}

    .hero-top {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      flex-wrap: wrap;
      gap: 20px;
      margin-bottom: 24px;
    }}

    .hero-title-area h1 {{
      font-size: 2.2rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      background: linear-gradient(135deg, #ffffff 30%, var(--accent-blue) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .hero-subtitle {{
      color: var(--text-secondary);
      font-size: 1.05rem;
      margin-top: 6px;
      display: flex;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
    }}

    .hero-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 12px;
      border-radius: var(--radius-full);
      font-size: 0.85rem;
      font-weight: 600;
      background: rgba(56, 189, 248, 0.12);
      color: var(--accent-blue);
      border: 1px solid rgba(56, 189, 248, 0.3);
    }}

    .countdown-widget {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 14px 20px;
      display: flex;
      align-items: center;
      gap: 16px;
      box-shadow: var(--shadow-sm);
    }}

    .countdown-val {{
      font-size: 1.8rem;
      font-weight: 800;
      color: var(--accent-amber);
      font-family: 'JetBrains Mono', monospace;
      line-height: 1;
    }}

    .countdown-label {{
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-secondary);
      font-weight: 600;
    }}

    /* Stat Banner Cards */
    .stat-banner {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 16px;
      margin-top: 20px;
    }}

    .stat-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: var(--transition);
      position: relative;
      overflow: hidden;
    }}

    .stat-card:hover {{
      transform: translateY(-2px);
      border-color: rgba(56, 189, 248, 0.4);
      box-shadow: var(--shadow-md);
    }}

    .stat-card::before {{
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
      background: var(--accent-blue);
    }}

    .stat-card.emerald::before {{ background: var(--accent-emerald); }}
    .stat-card.amber::before {{ background: var(--accent-amber); }}
    .stat-card.purple::before {{ background: var(--accent-purple); }}
    .stat-card.rose::before {{ background: var(--accent-rose); }}

    .stat-title {{
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-secondary);
      font-weight: 600;
      margin-bottom: 6px;
    }}

    .stat-value {{
      font-size: 1.8rem;
      font-weight: 800;
      color: var(--text-highlight);
      font-family: 'JetBrains Mono', monospace;
      line-height: 1.1;
    }}

    .stat-sub {{
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-top: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .badge-diff {{
      color: var(--accent-emerald);
      font-weight: 700;
      font-size: 0.85rem;
    }}

    /* Top-Level Race Switcher */
    /* Navigation Tabs */
    .tabs-nav-wrapper {{
      max-width: 1400px;
      margin: 24px auto 0;
      padding: 0 24px;
    }}

    .tabs-nav {{
      display: flex;
      gap: 8px;
      background: var(--bg-secondary);
      padding: 6px;
      border-radius: var(--radius-md);
      border: 1px solid var(--border-color);
      overflow-x: auto;
      scrollbar-width: none;
    }}

    .tabs-nav::-webkit-scrollbar {{
      display: none;
    }}

    .tab-btn {{
      background: transparent;
      border: none;
      color: var(--text-secondary);
      font-family: inherit;
      font-size: 0.95rem;
      font-weight: 600;
      padding: 10px 18px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      white-space: nowrap;
      transition: var(--transition);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .tab-btn:hover {{
      color: var(--text-primary);
      background: rgba(255, 255, 255, 0.05);
    }}

    .tab-btn.active {{
      background: var(--accent-blue);
      color: #0f172a;
      box-shadow: 0 2px 10px rgba(56, 189, 248, 0.3);
    }}

    /* Main Container & Sections */
    main {{
      max-width: 1400px;
      margin: 28px auto 0;
      padding: 0 24px;
    }}

    .tab-content {{
      display: none;
      animation: fadeIn 0.25s ease-out;
    }}

    .tab-content.active {{
      display: block;
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Section Headers */
    .section-header {{
      margin-bottom: 24px;
    }}

    .section-header h2 {{
      font-size: 1.5rem;
      font-weight: 700;
      color: var(--text-highlight);
      letter-spacing: -0.02em;
    }}

    .section-header p {{
      color: var(--text-secondary);
      font-size: 0.95rem;
      margin-top: 4px;
    }}

    /* Cards Grid */
    .grid-2 {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
      gap: 24px;
      margin-bottom: 28px;
    }}

    .grid-3 {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 20px;
      margin-bottom: 28px;
    }}

    .card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 24px;
      box-shadow: var(--shadow-sm);
    }}

    .card-title {{
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text-highlight);
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 16px;
    }}

    /* Proxy Indicators Section */
    .indicator-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      transition: var(--transition);
    }}

    .indicator-card:hover {{
      border-color: rgba(56, 189, 248, 0.4);
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
    }}

    .indicator-top {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 12px;
      margin-bottom: 12px;
    }}

    .indicator-name {{
      font-size: 1.1rem;
      font-weight: 700;
      color: var(--text-highlight);
    }}

    .indicator-status {{
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      padding: 3px 8px;
      border-radius: var(--radius-full);
      letter-spacing: 0.05em;
    }}

    .status-target {{
      background: rgba(16, 185, 129, 0.15);
      color: var(--accent-emerald);
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}

    .status-track {{
      background: rgba(56, 189, 248, 0.15);
      color: var(--accent-blue);
      border: 1px solid rgba(56, 189, 248, 0.3);
    }}

    .status-alert {{
      background: rgba(245, 158, 11, 0.15);
      color: var(--accent-amber);
      border: 1px solid rgba(245, 158, 11, 0.3);
    }}

    .indicator-desc {{
      font-size: 0.88rem;
      color: var(--text-secondary);
      margin-bottom: 16px;
      line-height: 1.45;
    }}

    .indicator-metrics {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 12px;
      margin-bottom: 14px;
      text-align: center;
    }}

    .metric-col:not(:last-child) {{
      border-right: 1px solid var(--border-subtle);
    }}

    .metric-label {{
      font-size: 0.72rem;
      text-transform: uppercase;
      font-weight: 600;
      color: var(--text-muted);
    }}

    .metric-num {{
      font-size: 1.15rem;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      color: var(--text-highlight);
      margin-top: 2px;
    }}

    .metric-num.target {{
      color: var(--accent-emerald);
    }}

    .metric-num.current {{
      color: var(--accent-blue);
    }}

    .indicator-why {{
      font-size: 0.82rem;
      color: var(--text-secondary);
      background: rgba(255, 255, 255, 0.02);
      border-left: 3px solid var(--accent-cyan);
      padding: 8px 12px;
      border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    }}

    /* Proxy Indicator Time Series Selector & Granularity Bar */
    .metric-toggle-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 16px;
    }}

    .metric-btn {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-secondary);
      padding: 8px 14px;
      border-radius: var(--radius-sm);
      font-size: 0.84rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: var(--transition);
    }}

    .metric-btn:hover {{
      border-color: var(--accent-blue);
      color: var(--text-primary);
    }}

    .metric-btn.active {{
      background: rgba(56, 189, 248, 0.15);
      border-color: var(--accent-blue);
      color: var(--accent-blue);
      font-weight: 700;
    }}

    .granularity-btn {{
      background: transparent;
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      padding: 5px 12px;
      border-radius: var(--radius-full);
      font-size: 0.8rem;
      font-weight: 700;
      cursor: pointer;
      transition: var(--transition);
    }}

    .granularity-btn:hover {{
      color: var(--text-primary);
      border-color: var(--text-secondary);
    }}

    .granularity-btn.active {{
      background: var(--accent-emerald);
      color: #000;
      border-color: var(--accent-emerald);
    }}

    /* Chart Containers */
    .chart-box {{
      position: relative;
      width: 100%;
      height: 320px;
    }}

    /* Training Plan Styles */
    .phase-filter-bar {{
      display: flex;
      gap: 10px;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }}

    .phase-pill {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-secondary);
      font-size: 0.85rem;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: var(--radius-full);
      cursor: pointer;
      transition: var(--transition);
    }}

    .phase-pill:hover {{
      border-color: var(--accent-blue);
      color: var(--text-primary);
    }}

    .phase-pill.active {{
      background: var(--accent-blue);
      color: #0f172a;
      border-color: var(--accent-blue);
      font-weight: 700;
    }}

    .week-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 20px;
      margin-bottom: 16px;
      transition: var(--transition);
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .week-card:hover {{
      border-color: rgba(56, 189, 248, 0.4);
      background: var(--bg-card-hover);
    }}

    .week-badge {{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: rgba(56, 189, 248, 0.1);
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: var(--radius-sm);
      padding: 8px;
    }}

    .week-num {{
      font-size: 1.1rem;
      font-weight: 800;
      color: var(--accent-blue);
      font-family: 'JetBrains Mono', monospace;
    }}

    .week-tag {{
      font-size: 0.65rem;
      text-transform: uppercase;
      font-weight: 700;
      color: var(--text-secondary);
    }}

    .week-meta {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .week-dates {{
      font-size: 0.85rem;
      color: var(--text-secondary);
      font-weight: 500;
    }}

    .week-miles {{
      font-size: 1.25rem;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      color: var(--accent-amber);
    }}

    .week-details {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    .workout-line {{
      font-size: 0.92rem;
      color: var(--text-primary);
      display: flex;
      align-items: baseline;
      gap: 8px;
    }}

    .workout-label {{
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      padding: 2px 6px;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.08);
      color: var(--accent-cyan);
      white-space: nowrap;
    }}

    .workout-label.lr {{
      background: rgba(245, 158, 11, 0.15);
      color: var(--accent-amber);
    }}

    .workout-sub {{
      font-size: 0.82rem;
      color: var(--text-muted);
    }}

    .week-checkpoint {{
      font-size: 0.82rem;
      color: var(--accent-emerald);
      background: rgba(16, 185, 129, 0.08);
      border: 1px solid rgba(16, 185, 129, 0.2);
      border-radius: var(--radius-sm);
      padding: 8px 12px;
    }}

    .week-check {{
      display: flex;
      justify-content: center;
      align-items: center;
    }}

    .week-check input[type="checkbox"] {{
      width: 20px;
      height: 20px;
      cursor: pointer;
      accent-color: var(--accent-emerald);
    }}

    .week-card-main {{
      display: grid;
      grid-template-columns: 80px 140px 1fr 200px 40px;
      align-items: center;
      gap: 20px;
      width: 100%;
    }}

    @media (max-width: 900px) {{
      .week-card-main {{
        grid-template-columns: 1fr;
        gap: 12px;
      }}
    }}

    .details-toggle-btn {{
      background: rgba(56, 189, 248, 0.1);
      border: 1px solid rgba(56, 189, 248, 0.25);
      color: var(--accent-blue);
      font-size: 0.8rem;
      font-weight: 600;
      padding: 5px 12px;
      border-radius: 6px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: var(--transition);
      margin-top: 6px;
      width: fit-content;
    }}

    .details-toggle-btn:hover {{
      background: rgba(56, 189, 248, 0.2);
      border-color: var(--accent-blue);
      color: #fff;
    }}

    .details-toggle-btn.active {{
      background: rgba(16, 185, 129, 0.18);
      border-color: var(--accent-emerald);
      color: var(--accent-emerald);
    }}

    .week-daily-breakdown {{
      width: 100%;
      background: rgba(10, 15, 29, 0.7);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 16px;
      margin-top: 4px;
      animation: fadeIn 0.2s ease-in-out;
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(-4px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    .daily-details-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.85rem;
    }}

    .daily-details-table th {{
      background: rgba(0, 0, 0, 0.35);
      color: var(--text-muted);
      font-size: 0.75rem;
      text-transform: uppercase;
      font-weight: 700;
      padding: 8px 12px;
      text-align: left;
      border-bottom: 1px solid var(--border-subtle);
    }}

    .daily-details-table td {{
      padding: 10px 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      vertical-align: top;
    }}

    .daily-details-table tr:last-child td {{
      border-bottom: none;
    }}

    .daily-details-table tr:hover {{
      background: rgba(255, 255, 255, 0.02);
    }}

    .day-badge {{
      display: inline-block;
      font-size: 0.72rem;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      text-transform: uppercase;
      font-family: 'JetBrains Mono', monospace;
    }}

    .day-badge.rest {{
      background: rgba(100, 116, 139, 0.2);
      color: var(--text-muted);
    }}

    .day-badge.run {{
      background: rgba(56, 189, 248, 0.15);
      color: var(--accent-blue);
    }}

    .day-badge.lr {{
      background: rgba(245, 158, 11, 0.15);
      color: var(--accent-amber);
    }}

    .day-badge.race {{
      background: rgba(16, 185, 129, 0.2);
      color: var(--accent-emerald);
    }}

    .daily-miles {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      color: var(--accent-amber);
      font-size: 0.95rem;
    }}

    .daily-miles.rest {{
      color: var(--text-muted);
      font-weight: normal;
    }}

    .daily-pace {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      color: var(--accent-cyan);
    }}

    .daily-hr {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      color: var(--accent-rose);
    }}

    .daily-purpose {{
      font-size: 0.8rem;
      color: var(--accent-emerald);
      margin-bottom: 3px;
    }}

    .daily-instruction {{
      font-size: 0.83rem;
      color: var(--text-secondary);
      line-height: 1.4;
    }}

    /* Tables */
    .data-table-wrapper {{
      overflow-x: auto;
      border-radius: var(--radius-md);
      border: 1px solid var(--border-color);
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.9rem;
    }}

    th {{
      background: var(--bg-secondary);
      color: var(--text-secondary);
      font-weight: 700;
      text-transform: uppercase;
      font-size: 0.75rem;
      letter-spacing: 0.05em;
      padding: 14px 16px;
      border-bottom: 1px solid var(--border-color);
    }}

    td {{
      padding: 12px 16px;
      border-bottom: 1px solid var(--border-subtle);
      color: var(--text-primary);
    }}

    tr:last-child td {{
      border-bottom: none;
    }}

    tr:hover td {{
      background: rgba(255, 255, 255, 0.02);
    }}

    /* Calculator Styles */
    .calc-container {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
      gap: 24px;
    }}

    .input-group {{
      margin-bottom: 16px;
    }}

    .input-group label {{
      display: block;
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-secondary);
      margin-bottom: 6px;
    }}

    .input-row {{
      display: flex;
      gap: 10px;
    }}

    input[type="text"], input[type="number"], select {{
      width: 100%;
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 10px 14px;
      color: var(--text-primary);
      font-family: inherit;
      font-size: 0.95rem;
      transition: var(--transition);
    }}

    input:focus, select:focus {{
      outline: none;
      border-color: var(--accent-blue);
      box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15);
    }}

    .calc-btn {{
      background: var(--accent-blue);
      color: #0f172a;
      border: none;
      padding: 12px 20px;
      border-radius: var(--radius-sm);
      font-weight: 700;
      font-size: 0.95rem;
      cursor: pointer;
      width: 100%;
      margin-top: 8px;
      transition: var(--transition);
    }}

    .calc-btn:hover {{
      background: #7dd3fc;
      transform: translateY(-1px);
    }}

    .calc-result-box {{
      background: rgba(0, 0, 0, 0.3);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 18px;
      margin-top: 20px;
    }}

    .calc-result-header {{
      font-size: 0.85rem;
      text-transform: uppercase;
      font-weight: 700;
      color: var(--text-secondary);
      margin-bottom: 8px;
    }}

    .calc-result-val {{
      font-size: 2rem;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      color: var(--accent-emerald);
      line-height: 1;
      margin-bottom: 8px;
    }}

    /* Pace Zone Pill Grid */
    .zone-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
      gap: 10px;
      margin-top: 14px;
    }}

    .zone-pill {{
      background: var(--bg-secondary);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 10px;
      text-align: center;
    }}

    .zone-name {{
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--text-muted);
    }}

    .zone-pace {{
      font-size: 1.05rem;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      color: var(--text-highlight);
      margin-top: 2px;
    }}

    /* Responsive */
    @media (max-width: 900px) {{
      .hero-title-area h1 {{ font-size: 1.8rem; }}
      .week-card {{
        grid-template-columns: 1fr;
        gap: 12px;
      }}
      .grid-2, .calc-container {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>

  <!-- HEADER -->
  <header>
    <div class="header-container">
      <!-- Top-Level Campaign Header Badge -->
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 20px;">
        <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); padding: 6px 14px; border-radius: var(--radius-full); font-size: 0.85rem; font-weight: 700; color: var(--accent-emerald);">
          <span>🌲</span> Official Campaign: BMO Vancouver Marathon 2027 • 31-Week Master Periodization
        </div>
        <div style="color: var(--text-secondary); font-size: 0.85rem;">
          Race Day: <strong>Sunday, May 2, 2027</strong> • Vancouver, BC
        </div>
      </div>

      <div class="hero-top">
        <div class="hero-title-area">
          <h1 id="raceMainTitle">
            <span>🌲</span> BMO Vancouver Marathon 2027: Sub-3:15
          </h1>
          <div class="hero-subtitle">
            <span id="raceDateText">Sunday, May 2, 2027</span>
            <span>•</span>
            <span id="raceLocationText">Vancouver, BC, Canada</span>
            <span class="hero-badge" id="racePaceBadge">Goal Pace: 7:24 – 7:26 / mi (4:36 / km)</span>
            <span class="hero-badge" id="raceElevationBadge" style="background: rgba(16, 185, 129, 0.12); color: var(--accent-emerald); border-color: rgba(16, 185, 129, 0.3);">Course: 825 ft Gain • -215 ft Net Downhill</span>
          </div>
        </div>

        <div class="countdown-widget">
          <div>
            <div class="countdown-val" id="countdownDays">212</div>
            <div class="countdown-label">Days to Race</div>
          </div>
          <div style="border-left: 1px solid var(--border-color); padding-left: 16px;">
            <div class="countdown-val" id="countdownWeeks" style="color: var(--accent-emerald);">31</div>
            <div class="countdown-label">Training Weeks</div>
          </div>
        </div>
      </div>

      <!-- Stat Banner Cards -->
      <div class="stat-banner">
        <div class="stat-card emerald">
          <div class="stat-title">Target Goal Time</div>
          <div class="stat-value">3:14:59</div>
          <div class="stat-sub"><span class="badge-diff">-19m 05s</span> from Seattle</div>
        </div>

        <div class="stat-card">
          <div class="stat-title">Target Marathon Pace</div>
          <div class="stat-value">7:25<span style="font-size: 1rem;">/mi</span></div>
          <div class="stat-sub"><span class="badge-diff">-44s/mi</span> (4:36/km, +9.0% speed)</div>
        </div>

        <div class="stat-card purple">
          <div class="stat-title">Seattle 2025 Baseline</div>
          <div class="stat-value">3:34:04</div>
          <div class="stat-sub">8:09/mi • Avg HR: 152.7 bpm</div>
        </div>

        <div class="stat-card amber">
          <div class="stat-title">Target VDOT Score</div>
          <div class="stat-value">50.6</div>
          <div class="stat-sub">Seattle Baseline: 45.5 (+5.1 pts)</div>
        </div>

        <div class="stat-card rose">
          <div class="stat-title" id="statCourseElevationTitle">Course Profile</div>
          <div class="stat-value" id="statCourseElevationVal" style="font-size: 1.4rem;">825 <span style="font-size: 0.85rem; color: var(--text-secondary);">ft gain</span></div>
          <div class="stat-sub" id="statCourseElevationSub">-215 ft Net Downhill (31.4 ft/mi)</div>
        </div>
      </div>
    </div>
  </header>

  <!-- NAVIGATION TABS -->
  <div class="tabs-nav-wrapper">
    <div class="tabs-nav">
      <button class="tab-btn active" id="navBtn_overview" onclick="switchTab('overview')">
        <span>🌲</span> Vancouver Campaign & Strategy
      </button>
      <button class="tab-btn" id="navBtn_coach" onclick="switchTab('coach')" style="border-color: rgba(16, 185, 129, 0.45); background: rgba(16, 185, 129, 0.08);">
        <span>🏃</span> Coach's Log & Daily Debriefs <span style="background: var(--accent-emerald); color: #000; font-size: 0.65rem; font-weight: 800; padding: 1px 6px; border-radius: 9999px; margin-left: 4px;">ACTIVE</span>
      </button>
      <button class="tab-btn" id="navBtn_training" onclick="switchTab('training')">
        <span>📅</span> 31-Week Training Schedule
      </button>
      <button class="tab-btn" id="navBtn_indicators" onclick="switchTab('indicators')">
        <span>🎯</span> Telemetry & Proxy Indicators
      </button>
      <button class="tab-btn" id="navBtn_seattle" onclick="switchTab('seattle')">
        <span>📊</span> Seattle 2025 Retrospective
      </button>
      <button class="tab-btn" id="navBtn_calculator" onclick="switchTab('calculator')">
        <span>🧮</span> Readiness & Fitness Calc
      </button>
      <button class="tab-btn" id="navBtn_history" onclick="switchTab('history')">
        <span>📈</span> Historical Volume & Heatmap
      </button>
    </div>
  </div>
  </div>

  <!-- MAIN CONTAINER -->
  <main>

    <!-- TAB 1: OVERVIEW & STRATEGY -->
    <section id="tab-overview" class="tab-content active">
      <div class="section-header">
        <h2>🌲 Strategic Campaign: Seattle 3:34 ➔ BMO Vancouver 3:15</h2>
        <p>A rigorous, evidence-based roadmap bridging your verified Seattle aerobic base to 3:15 capability across 31 periodized weeks (Sunday, May 2, 2027 • Vancouver, BC).</p>
      </div>

      {vancouver_command_center_html}

      <div class="grid-2">
        <div class="card">
          <div class="card-title">
            <span>The Mathematical & Physiological Leap</span>
            <span class="hero-badge">Analysis</span>
          </div>
          <p style="color: var(--text-secondary); margin-bottom: 16px; font-size: 0.95rem;">
            Your Seattle Marathon on Nov 30, 2025 was run with impeccable discipline: finishing in 3:34:04 (8:09/mile) with negative splits (final 2.2km at 7:56/mile) and an average heart rate of 152.7 bpm. You demonstrated exceptional aerobic durability with near-zero premature cardiac drift on a course with ~950 ft gain.
          </p>
          <div style="background: var(--bg-secondary); border-radius: var(--radius-sm); padding: 16px; border: 1px solid var(--border-subtle); margin-bottom: 16px;">
            <div style="font-weight: 700; color: var(--accent-emerald); margin-bottom: 6px;">The Vancouver 3:15 Challenge:</div>
            <ul style="padding-left: 20px; color: var(--text-secondary); font-size: 0.9rem; display: flex; flex-direction: column; gap: 8px;">
              <li><strong>Pace Requirement:</strong> 7:25–7:26 min/mile (4:36–4:37 min/km) sustained for 26.2 miles.</li>
              <li><strong>Speed Differential:</strong> +44 seconds per mile faster than Seattle (+9.0% velocity).</li>
              <li><strong>The Engine Shift:</strong> You already possess strong aerobic endurance and mental resilience. The required shift is lifting your <em>lactate threshold velocity</em> so that 7:25/mile feels like cruising in Zone 3 (~151–155 bpm) rather than straining in Zone 4 (~165+ bpm).</li>
              <li><strong>Volume Expansion & Runway:</strong> With <strong>31 periodized weeks</strong> (8 extra weeks compared to spring alternatives), peak volume can safely expand to <strong>52–58 mpw</strong> without rushing mileage spikes.</li>
            </ul>
          </div>
          <div style="font-size: 0.88rem; color: var(--text-muted);">
            💡 <em>"You do not rise to the level of your goal on race day; you fall to the level of your training telemetry."</em>
          </div>
        </div>

        <div class="card">
          <div class="card-title">
            <span>BMO Vancouver Marathon Course Anatomy</span>
            <span class="hero-badge" style="background: rgba(16, 185, 129, 0.15); color: var(--accent-emerald); border-color: rgba(16, 185, 129, 0.3);">Course Breakdown</span>
          </div>
          <div style="color: var(--text-secondary); font-size: 0.9rem; line-height: 1.55; display: flex; flex-direction: column; gap: 8px;">
            <div style="padding: 9px; background: var(--bg-secondary); border-left: 3px solid var(--accent-blue); border-radius: 4px;">
              <strong>Km 0–8 (Miles 1–5 - QE Park to Dunbar):</strong> Starts high at Queen Elizabeth Park (~152m elevation). Gentle initial descent. Settle into disciplined 7:28–7:30/mi pace.
            </div>
            <div style="padding: 9px; background: var(--bg-secondary); border-left: 3px solid var(--accent-rose); border-radius: 4px;">
              <strong>Km 9–10 (Mile 6 - Camosun Hill):</strong> Famous steep climb (~177 ft vertical rise in 0.6 mi). <em>Pacing Rule:</em> Surrender pace! Run by HR (&lt; 158 bpm, ~8:10/mi). Your 52 ft/mi Seattle training makes this easy.
            </div>
            <div style="padding: 9px; background: var(--bg-secondary); border-left: 3px solid var(--accent-amber); border-radius: 4px;">
              <strong>Km 10–16 (Miles 6.5–10 - UBC Campus):</strong> Rolling roads through Pacific Spirit Park and UBC. Settle back into 7:24–7:26/mi cruise control.
            </div>
            <div style="padding: 9px; background: var(--bg-secondary); border-left: 3px solid var(--accent-cyan); border-radius: 4px;">
              <strong>Km 16–18 (Miles 10–11.5 - NW Marine Drive):</strong> Fast descent dropping ~250 ft to Spanish Banks. Maintain cadence (&gt;180 spm), lean forward, protect quads.
            </div>
            <div style="padding: 9px; background: var(--bg-secondary); border-left: 3px solid var(--accent-emerald); border-radius: 4px;">
              <strong>Km 18–31 (Miles 11.5–19.5 - Spanish Banks &amp; Kitsilano):</strong> Flat coastal miles along English Bay. Metronome miles: lock into 7:24/mi. Fuel with gel every 35 mins.
            </div>
            <div style="padding: 9px; background: var(--bg-secondary); border-left: 3px solid var(--accent-purple); border-radius: 4px;">
              <strong>Km 31–40 (Miles 19.5–25 - Burrard Bridge &amp; Seawall):</strong> Burrard bridge crest followed by 9 km of flat seawall loop around Stanley Park. Mental focus wins the race.
            </div>
            <div style="padding: 9px; background: var(--bg-secondary); border-left: 3px solid var(--accent-emerald); border-radius: 4px;">
              <strong>Km 40–42.2 (Miles 25–26.2 - Downtown Finish):</strong> Exit seawall onto West Pender Street rise. Re-accelerate to 7:15/mi into the finish line for 3:14:xx!
            </div>
          </div>
        </div>
      </div>

      <!-- Elevation & Topography Advantage Banner -->
      <div class="card" style="margin-bottom: 28px; background: linear-gradient(135deg, rgba(22, 32, 50, 0.9) 0%, rgba(17, 24, 39, 0.95) 100%); border-color: rgba(16, 185, 129, 0.35);">
        <div class="card-title">
          <span>⛰️ Elevation &amp; Topography: Your Decisive Advantage</span>
          <span class="hero-badge" style="background: rgba(16, 185, 129, 0.15); color: var(--accent-emerald); border-color: rgba(16, 185, 129, 0.3);">Topography Analysis</span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-top: 14px;">
          <div style="background: var(--bg-secondary); padding: 14px; border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);">
            <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700;">Your Seattle Training Routes</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: var(--accent-amber); font-family: 'JetBrains Mono', monospace; margin: 4px 0;">52.4 <span style="font-size: 0.9rem;">ft / mi</span></div>
            <div style="font-size: 0.85rem; color: var(--text-secondary);">~1,373 ft climbing per 26.2 mi equivalent. Your regular routes are <strong>~67% hillier</strong> than Vancouver!</div>
          </div>
          <div style="background: var(--bg-secondary); padding: 14px; border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);">
            <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700;">Seattle Marathon 2025 Baseline</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: var(--accent-blue); font-family: 'JetBrains Mono', monospace; margin: 4px 0;">36.3 <span style="font-size: 0.9rem;">ft / mi</span></div>
            <div style="font-size: 0.85rem; color: var(--text-secondary);">~950 ft gain with <strong>0 net drop</strong> (loop). Grade-Adjusted Flat Equivalent was <strong>3:27:44 (7:55/mi, VDOT 47.1)</strong>!</div>
          </div>
          <div style="background: var(--bg-secondary); padding: 14px; border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);">
            <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--accent-emerald); font-weight: 700;">BMO Vancouver Marathon 2027</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: var(--accent-emerald); font-family: 'JetBrains Mono', monospace; margin: 4px 0;">31.4 <span style="font-size: 0.9rem;">ft / mi</span></div>
            <div style="font-size: 0.85rem; color: var(--text-secondary);">825 ft gain with <strong>-215 ft Net Downhill</strong>! Even friendlier profile than Seattle, with ideal 50°F–58°F maritime weather.</div>
          </div>
        </div>
        <div style="margin-top: 14px; font-size: 0.88rem; color: var(--text-secondary); background: rgba(0,0,0,0.25); padding: 10px 14px; border-radius: var(--radius-sm);">
          💡 <strong>Key Takeaway:</strong> Vancouver features less total climbing than Seattle, plus a net downhill bonus (-215 ft). Because you consistently train on 52 ft/mile Seattle hills, you have built high eccentric quad resilience and superior metabolic power. Run the hills by HR (&lt;158 bpm), and let the flats unlock 7:24 pace effortlessly.
        </div>
      </div>

      <!-- 6 Macrocycle Phases -->
      <div class="card" style="margin-bottom: 28px;">
        <div class="card-title">
          <span>The 6-Phase Periodization Architecture</span>
          <span style="font-size: 0.85rem; color: var(--text-secondary); font-weight: normal;">Sep 28, 2026 ➔ May 2, 2027 (31 Weeks)</span>
        </div>
        <div class="grid-3" id="phasesOverviewGrid">
          <!-- Populated dynamically via JS -->
        </div>
      </div>
    </section>

    {coach_tab_html}

    <!-- TAB 2: PROXY INDICATORS (TELEMETRY) -->
    <section id="tab-indicators" class="tab-content">
      <div class="section-header">
        <h2>Proxy Metrics & Telemetry Engine</h2>
        <p>You cannot run a marathon test every month. Instead, track these 6 physiological proxy indicators in your day-to-day training data to verify if you are trending toward a 3:15 finish.</p>
      </div>

      <div class="grid-3" id="indicatorsGrid">
        <!-- Rendered dynamically via JS -->
      </div>

      <!-- Interactive Proxy Metric Time Series Studio -->
      <div class="card" style="margin-bottom: 24px; border: 1px solid rgba(56, 189, 248, 0.35);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 16px;">
          <div>
            <div class="card-title" style="margin-bottom: 4px;">
              <span id="tsChartHeading">📈 Proxy Indicator Historical Time Series: Grade-Adjusted Efficiency Factor (GAP-EF)</span>
              <span class="hero-badge" id="tsMetricBadge" style="background: rgba(168, 85, 247, 0.15); color: var(--accent-purple); border-color: rgba(168, 85, 247, 0.3);">Grade-Adjusted</span>
            </div>
            <p style="font-size: 0.85rem; color: var(--text-secondary); margin: 0;" id="tsChartDescription">
              Speed normalized for Seattle hill climb gradients (ft/mile) divided by Heart Rate. Target for Sub-3:15 is &ge; 1.45.
            </p>
          </div>
          <!-- Granularity Toggle -->
          <div style="display: flex; align-items: center; gap: 8px; background: rgba(0, 0, 0, 0.35); padding: 4px 8px; border-radius: var(--radius-full); border: 1px solid var(--border-subtle);">
            <span style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700; margin-right: 4px;">Granularity:</span>
            <button class="granularity-btn active" id="granBtn_weekly" onclick="setTsGranularity('weekly')">📅 Weekly (Smoothed)</button>
            <button class="granularity-btn" id="granBtn_daily" onclick="setTsGranularity('daily')">🏃 Daily (Every Run)</button>
          </div>
        </div>

        <!-- Metric Switcher Pills -->
        <div class="metric-toggle-bar">
          <button class="metric-btn active" id="tsBtn_gap_ef" onclick="setTsMetric('gap_ef')">
            <span>⛰️</span> Grade-Adjusted EF (GAP-EF)
          </button>
          <button class="metric-btn" id="tsBtn_ef" onclick="setTsMetric('ef')">
            <span>⚡</span> Raw Aerobic EF
          </button>
          <button class="metric-btn" id="tsBtn_pace" onclick="setTsMetric('pace')">
            <span>⏱️</span> Pace vs GAP Pace
          </button>
          <button class="metric-btn" id="tsBtn_hr" onclick="setTsMetric('hr')">
            <span>❤️</span> Heart Rate & Cadence
          </button>
          <button class="metric-btn" id="tsBtn_vdot" onclick="setTsMetric('vdot')">
            <span>🎯</span> Estimated Daniels VDOT
          </button>
          <button class="metric-btn" id="tsBtn_volume" onclick="setTsMetric('volume')">
            <span>📊</span> Mileage & Rolling 4W MPW
          </button>
          <button class="metric-btn" id="tsBtn_decoupling" onclick="setTsMetric('decoupling')">
            <span>📉</span> Aerobic Decoupling (%)
          </button>
        </div>

        <div class="chart-box" style="height: 380px;">
          <canvas id="proxyTsChart"></canvas>
        </div>
      </div>

      <!-- Chart: Aerobic Efficiency Factor Progression -->
      <div class="grid-2">
        <div class="card">
          <div class="card-title">
            <span>Aerobic Efficiency Factor (EF) Trajectory</span>
            <span class="hero-badge">Speed / Heart Rate</span>
          </div>
          <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 12px;">
            Historical monthly EF (2025-2026) plotted against the required trajectory to reach <strong>1.42</strong> for a 3:15 marathon.
          </p>
          <div class="chart-box">
            <canvas id="efChart"></canvas>
          </div>
        </div>

        <div class="card">
          <div class="card-title">
            <span>Volume Density & Long Run Progression</span>
            <span class="hero-badge">Miles / Month</span>
          </div>
          <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 12px;">
            Historical monthly volume and longest runs vs. target build for peak Vancouver training (52-58 mpw).
          </p>
          <div class="chart-box">
            <canvas id="volumeChart"></canvas>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 3: PERIODIZED TRAINING PLANS -->
    <section id="tab-training" class="tab-content">
      <div class="section-header">
        <h2 id="planSectionTitle">🌲 BMO Vancouver Marathon: 31-Week Master Training Schedule</h2>
        <p id="planSectionSub">Sep 28, 2026 to May 2, 2027 • Specific daily running assignments, strength protocol, long run workouts, and proxy checkpoints.</p>
      </div>

      <!-- Strength & Lifting Integration Guide Card -->
      <div class="card" style="margin-bottom: 24px; background: linear-gradient(135deg, rgba(22, 32, 50, 0.95) 0%, rgba(17, 24, 39, 0.98) 100%); border-color: rgba(168, 85, 247, 0.35);">
        <div class="card-title">
          <span>🏋️ Concurrent Strength Training: Strict Zero-Double-Days Protocol</span>
          <span class="hero-badge" style="background: rgba(168, 85, 247, 0.15); color: var(--accent-purple); border-color: rgba(168, 85, 247, 0.3);">Never Run & Lift Same Day</span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-top: 14px;">
          <div style="background: var(--bg-secondary); padding: 14px; border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);">
            <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--accent-purple); font-weight: 700;">Core Principle: Zero Double Days</div>
            <div style="font-size: 1.1rem; font-weight: 800; color: var(--text-highlight); margin: 4px 0;">One Focus Per Day</div>
            <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.45;">
              <strong>Never lift and run on the same day.</strong> Monday is <strong>Lift Only</strong> (Upper Body & Core). Thursday is <strong>Lift Only</strong> (Legs 1/2w or Core). Wednesday is <strong>Run Only</strong> (midweek aerobic anchor, zero evening gym). Friday is <strong>Run Only</strong> (easy pre-long run flush).
            </div>
          </div>
          <div style="background: var(--bg-secondary); padding: 14px; border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);">
            <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--accent-blue); font-weight: 700;">Thursday (Odd Weeks • 1/2w)</div>
            <div style="font-size: 1.1rem; font-weight: 800; color: var(--text-highlight); margin: 4px 0;">Heavy Leg Strength (Zero Running)</div>
            <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.45;">
              <strong>Trap Bar Deadlift (3x5)</strong>, <strong>Bulgarian Split Squats (3x6/leg)</strong>, <strong>Heavy Standing Calf Raises (3x10)</strong>, <strong>Box Jumps (3x5)</strong>. Non-running day allows complete energy for neuromuscular recruitment. <strong>Leave 2–3 reps in reserve</strong> (never to failure).
            </div>
          </div>
          <div style="background: var(--bg-secondary); padding: 14px; border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);">
            <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--accent-emerald); font-weight: 700;">Thursday (Even Weeks • Alternate)</div>
            <div style="font-size: 1.1rem; font-weight: 800; color: var(--text-highlight); margin: 4px 0;">Core & Pelvic Hip Pre-Hab (Zero Running)</div>
            <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.45;">
              <strong>Copenhagen Adductor Planks (3x20s)</strong>, <strong>Side Planks w/ Leg Lift (3x30s)</strong>, <strong>Single-Leg RDLs (3x8)</strong>, <strong>Banded Glutes (3x12)</strong>. Zero heavy eccentric leg loading. Restores pelvic stability and protects IT bands without muscle soreness.
            </div>
          </div>
          <div style="background: var(--bg-secondary); padding: 14px; border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);">
            <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--accent-amber); font-weight: 700;">Monday Lift • Friday Easy Run</div>
            <div style="font-size: 1.1rem; font-weight: 800; color: var(--text-highlight); margin: 4px 0;">Upper Body Lift & Friday Flush</div>
            <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.45;">
              <strong>Monday (Lift Only)</strong>: Dumbbell Bench/Overhead Press, Pull-ups / Lat Pulldowns, Cable Rows, Pallof Press, Deadbugs. Zero running.<br>
              <strong>Friday (Run Only)</strong>: Easy conversational shakeout run (4–7 mi, zero lifting) to flush legs before Saturday's long run.
            </div>
          </div>
        </div>
      </div>

      <!-- Dynamic Filter pills -->
      <div class="phase-filter-bar" id="phaseFilterBar">
        <!-- Rendered dynamically via JS based on currentPlanRace -->
      </div>

      <div id="weeklyPlanContainer">
        <!-- Rendered dynamically via JS -->
      </div>
    </section>

    <!-- TAB 4: SEATTLE 2025 RETROSPECTIVE -->
    <section id="tab-seattle" class="tab-content">
      <div class="section-header">
        <h2>Seattle Marathon 2025: Baseline Forensic Analysis</h2>
        <p>Nov 30, 2025 • Official Time: 3:34:04 • <strong style="color: var(--accent-emerald);">Flat Equivalent: 3:27:44</strong> • 950 ft Gain (36.3 ft/mi) • Avg HR: 152.7 bpm • VDOT: 45.5 (Flat: 47.1)</p>
      </div>

      <div class="grid-2">
        <div class="card">
          <div class="card-title">
            <span>5km Segment Splits & Heart Rate</span>
            <span class="hero-badge">Empirical Data</span>
          </div>
          <div class="chart-box" style="height: 280px; margin-bottom: 20px;">
            <canvas id="seattleSplitsChart"></canvas>
          </div>
          <div class="data-table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Segment</th>
                  <th>Distance</th>
                  <th>Pace (min/mi)</th>
                  <th>Avg HR (bpm)</th>
                </tr>
              </thead>
              <tbody id="seattleSplitsTable">
                <!-- Rendered dynamically -->
              </tbody>
            </table>
          </div>
        </div>

        <div class="card">
          <div class="card-title">
            <span>Tactical Insights: What Seattle Proves</span>
            <span class="hero-badge" style="background: rgba(16, 185, 129, 0.15); color: var(--accent-emerald);">Key Learnings</span>
          </div>
          <div style="color: var(--text-secondary); font-size: 0.92rem; display: flex; flex-direction: column; gap: 14px;">
            <div style="background: var(--bg-secondary); border-left: 3px solid var(--accent-emerald); padding: 12px; border-radius: var(--radius-sm);">
              <strong style="color: var(--text-highlight);">1. Flawless Pacing Discipline:</strong>
              <p style="margin-top: 4px;">You ran Km 10-35 at virtually identical 8:08-8:15 pace with heart rate rock-solid at 151 bpm. You did not blow up or bonk.</p>
            </div>
            <div style="background: var(--bg-secondary); border-left: 3px solid var(--accent-blue); padding: 12px; border-radius: var(--radius-sm);">
              <strong style="color: var(--text-highlight);">2. Fast Finish Acceleration:</strong>
              <p style="margin-top: 4px;">In the final 2.2km, you surged to <strong>7:56/mile</strong> while pushing heart rate to 164 bpm. This proves you had reserve aerobic capacity that was untapped.</p>
            </div>
            <div style="background: var(--bg-secondary); border-left: 3px solid var(--accent-amber); padding: 12px; border-radius: var(--radius-sm);">
              <strong style="color: var(--text-highlight);">3. The Specific Upgrade for 3:15:</strong>
              <p style="margin-top: 4px;">To run 7:26, you cannot simply "try harder" on race day. You must push your lactate threshold so that 7:26 generates the exact same metabolic lactate clearance and 152 bpm cardiac load that 8:09 did in Seattle.</p>
            </div>
            <div style="background: var(--bg-secondary); border-left: 3px solid var(--accent-purple); padding: 12px; border-radius: var(--radius-sm);">
              <strong style="color: var(--text-highlight);">4. Seattle Elevation Penalty (~950 ft climbing):</strong>
              <p style="margin-top: 4px;">Seattle's hills (~36.3 ft/mi) cost ~6m 20s. Your flat-equivalent finish was <strong>3:27:44 (7:55/mi, VDOT 47.1)</strong>. The true fitness gap to 3:15 is only <strong>12m 44s</strong>, not 19 minutes!</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 5: READINESS & FITNESS CALCULATOR -->
    <section id="tab-calculator" class="tab-content">
      <div class="section-header">
        <h2>Interactive Fitness & Readiness Telemetry</h2>
        <p>Input recent workout data or tune-up race results to assess your current readiness score and target training zones.</p>
      </div>

      <div class="calc-container">
        <!-- Workout EF Calculator -->
        <div class="card">
          <div class="card-title">
            <span>Workout Aerobic Efficiency (EF)</span>
            <span class="hero-badge">Run Metric</span>
          </div>
          <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 16px;">
            Enter an easy or steady aerobic run to calculate your current Aerobic Efficiency Factor.
          </p>

          <div class="input-group">
            <label>Distance (Miles)</label>
            <input type="number" id="calcDist" value="8.0" step="0.1">
          </div>

          <div class="input-group">
            <label>Duration (Minutes : Seconds)</label>
            <div class="input-row">
              <input type="number" id="calcDurMin" value="68" placeholder="Minutes">
              <input type="number" id="calcDurSec" value="0" placeholder="Seconds">
            </div>
          </div>

          <div class="input-group">
            <label>Average Heart Rate (bpm)</label>
            <input type="number" id="calcHR" value="141">
          </div>

          <div class="input-group">
            <label>Elevation Gain (Feet) <span style="font-size: 0.75rem; color: var(--text-muted);">(Seattle hills compensation)</span></label>
            <input type="number" id="calcElev" value="400" placeholder="e.g. 400">
          </div>

          <button class="calc-btn" onclick="calculateEF()">Calculate Efficiency & Grade Adjustment</button>

          <div class="calc-result-box" id="efResultBox">
            <div class="calc-result-header">Computed Efficiency & Grade Adjustment</div>
            <div style="display: flex; justify-content: space-around; align-items: baseline; margin: 10px 0;">
              <div>
                <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Raw EF</div>
                <div class="calc-result-val" id="efResultVal" style="font-size: 1.5rem;">1.332</div>
              </div>
              <div>
                <div style="font-size: 0.75rem; color: var(--accent-purple); text-transform: uppercase;">Grade-Adjusted (GAP-EF)</div>
                <div class="calc-result-val" id="gapEfResultVal" style="font-size: 1.5rem; color: var(--accent-purple);">1.385</div>
              </div>
            </div>
            <div style="font-size: 0.85rem; color: var(--accent-cyan); font-family: 'JetBrains Mono', monospace; margin-bottom: 8px;" id="gapPaceText">
              Raw Pace: 8:30/mi ➔ Flat Equivalent GAP: 8:02/mi (+50 ft/mi)
            </div>
            <div style="font-size: 0.85rem; color: var(--text-secondary);" id="efVerdict">
              Tracking on schedule for Phase 1. Target for 3:15: ≥ 1.40.
            </div>
          </div>
        </div>

        <!-- Race Equivalent & VDOT Predictor -->
        <div class="card">
          <div class="card-title">
            <span>Race Equivalent & 3:15 Readiness</span>
            <span class="hero-badge">VDOT Predictor</span>
          </div>
          <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 16px;">
            Input a recent time trial or tune-up race to calculate VDOT score and marathon capability.
          </p>

          <div class="input-group">
            <label>Race Event</label>
            <select id="raceEvent">
              <option value="5k">5 km</option>
              <option value="10k" selected>10 km</option>
              <option value="half">Half Marathon (13.1 mi)</option>
            </select>
          </div>

          <div class="input-group">
            <label>Time (Hours : Minutes : Seconds)</label>
            <div class="input-row">
              <input type="number" id="raceHr" value="0" placeholder="Hours">
              <input type="number" id="raceMin" value="43" placeholder="Minutes">
              <input type="number" id="raceSec" value="30" placeholder="Seconds">
            </div>
          </div>

          <button class="calc-btn" onclick="calculateVDOT()">Assess Race Readiness</button>

          <div class="calc-result-box" id="vdotResultBox">
            <div class="calc-result-header">Estimated VDOT & Projected Marathon</div>
            <div class="calc-result-val" id="vdotMarathonPred">3:18:20</div>
            <div style="font-size: 0.9rem; font-weight: 600; color: var(--accent-amber); margin-bottom: 6px;" id="vdotScoreText">
              VDOT: 49.3 (Goal: 50.5)
            </div>
            <div style="font-size: 0.85rem; color: var(--text-secondary);" id="vdotVerdict">
              Readiness: ~82%. On track for 3:15 with Phase 3 & 4 MP blocks remaining!
            </div>
          </div>
        </div>
      </div>

      <!-- Training Pace Zones Reference -->
      <div class="card" style="margin-top: 24px;">
        <div class="card-title">
          <span>Personalized Training Pace Zones (VDOT 50.5 Goal vs Current VDOT 47.0)</span>
          <span class="hero-badge">Daniels Pacing</span>
        </div>
        <p style="font-size: 0.88rem; color: var(--text-secondary); margin-bottom: 16px;">
          Train at your <em>current fitness</em> for daily paces, and use <em>Goal VDOT 50.5</em> for race-specific MP blocks.
        </p>
        <div class="data-table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Training Zone</th>
                <th>Target Effort / Purpose</th>
                <th>Current Paces (VDOT 47.0)</th>
                <th>Goal Paces (VDOT 50.5 - 3:15)</th>
                <th>Target Heart Rate</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Easy / Recovery (E)</strong></td>
                <td>Cellular adaptation, mitochondria, capillary beds</td>
                <td>9:10 - 9:45 / mi</td>
                <td>8:35 - 9:15 / mi</td>
                <td>&lt; 140 bpm (Zone 2)</td>
              </tr>
              <tr>
                <td><strong>Marathon Pace (MP)</strong></td>
                <td>Specific race economy, glycogen preservation</td>
                <td>8:05 - 8:15 / mi</td>
                <td><strong>7:26 / mi</strong> (4:37/km)</td>
                <td>151 - 155 bpm (Zone 3)</td>
              </tr>
              <tr>
                <td><strong>Threshold / Tempo (T)</strong></td>
                <td>Lactate clearance, 20-40 min cruise intervals</td>
                <td>7:35 - 7:45 / mi</td>
                <td><strong>6:55 - 7:05 / mi</strong></td>
                <td>158 - 164 bpm (Zone 4)</td>
              </tr>
              <tr>
                <td><strong>Interval (I - VO2max)</strong></td>
                <td>Aerobic power, 3-5 min reps (800m-1200m)</td>
                <td>6:55 - 7:05 / mi</td>
                <td><strong>6:25 - 6:35 / mi</strong></td>
                <td>165 - 173 bpm (Zone 5)</td>
              </tr>
              <tr>
                <td><strong>Repetition (R - Speed)</strong></td>
                <td>Neuromuscular mechanics, 200m-400m strides</td>
                <td>46-48s per 200m</td>
                <td><strong>42-44s per 200m</strong></td>
                <td>Neuromuscular turnover</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- TAB 6: HISTORICAL VOLUME & LOGS -->
    <section id="tab-history" class="tab-content">
      <div class="section-header">
        <h2>Garmin Activity Logs & Historical Trends</h2>
        <p>Comprehensive record of your 389 runs from March 2025 to September 2026.</p>
      </div>

      <div class="card" style="margin-bottom: 24px;">
        <div class="card-title">
          <span>Monthly Training Progression</span>
          <span style="font-size: 0.85rem; color: var(--text-secondary); font-weight: normal;">March 2025 – Present</span>
        </div>
        <div class="data-table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Month</th>
                <th>Total Miles</th>
                <th>Elevation Gain</th>
                <th>Runs</th>
                <th>Longest Run</th>
                <th>Avg Pace</th>
                <th>Avg GAP</th>
                <th>Avg Heart Rate</th>
                <th>Cadence (spm)</th>
                <th>Raw / GAP EF</th>
              </tr>
            </thead>
            <tbody id="monthlyHistoryTable">
              <!-- Rendered dynamically -->
            </tbody>
          </table>
        </div>
      </div>

      <div class="card">
        <div class="card-title">
          <span>Recent 40 Runs</span>
          <span class="hero-badge">Garmin Sync</span>
        </div>
        <div class="data-table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Distance</th>
                <th>Duration</th>
                <th>Pace</th>
                <th>Gain (ft)</th>
                <th>ft / mi</th>
                <th>GAP Pace</th>
                <th>Avg HR</th>
                <th>Cadence</th>
                <th>Raw / GAP EF</th>
              </tr>
            </thead>
            <tbody id="recentRunsTable">
              <!-- Rendered dynamically -->
            </tbody>
          </table>
        </div>
      </div>
    </section>

  </main>

  <!-- Embedded Precomputed Data -->
  <script>
    window.PRELOADED_DASHBOARD_DATA = {data_json_str};
  </script>

  <!-- Main Dashboard Script -->
  <script>
    let dashboardData = window.PRELOADED_DASHBOARD_DATA;
    let currentRace = 'vancouver';
    let currentPlanRace = 'vancouver';
    let currentFilter = 'all';
    let allDetailsExpanded = false;

    function init() {{
      renderPhasesOverview();
      renderIndicators();
      renderPhaseFilterPills();
      renderWeeklyPlan();
      renderSeattleRetrospective();
      renderMonthlyHistory();
      renderRecentRuns();
      initCharts();
    }}

    function switchTab(tabId) {{
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
      
      const activeBtn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick') && b.getAttribute('onclick').includes(tabId));
      if (activeBtn) activeBtn.classList.add('active');
      
      const activeContent = document.getElementById('tab-' + tabId);
      if (activeContent) activeContent.classList.add('active');

      const wrapper = document.querySelector('.tabs-nav-wrapper');
      if (wrapper) {{
        window.scrollTo({{ top: wrapper.offsetTop - 12, behavior: 'smooth' }});
      }}
    }}

    function renderPhaseFilterPills() {{
      const container = document.getElementById('phaseFilterBar');
      if (!container) return;

      const phases = dashboardData.vancouver_phases || [];
      const totalWeeks = 31;

      let html = `<button class="phase-pill ${{currentFilter === 'all' ? 'active' : ''}}" onclick="filterPlan('all')">All ${{totalWeeks}} Weeks</button>`;
      
      phases.forEach(p => {{
        const isAct = currentFilter === String(p.phase_num);
        const shortName = p.name.split('&')[0].replace('Aerobic', '').trim();
        html += `<button class="phase-pill ${{isAct ? 'active' : ''}}" onclick="filterPlan(${{p.phase_num}})">Phase ${{p.phase_num}}: ${{shortName}} (${{p.weeks}})</button>`;
      }});

      html += `<button class="phase-pill" id="toggleAllDetailsBtn" onclick="toggleAllDetails()" style="margin-left: auto; background: rgba(16, 185, 129, 0.12); border-color: rgba(16, 185, 129, 0.35); color: var(--accent-emerald);">👁️ Expand All Week Details</button>`;

      container.innerHTML = html;
    }}

    function renderPhasesOverview() {{
      const container = document.getElementById('phasesOverviewGrid');
      if (!container || !dashboardData.vancouver_phases) return;

      container.innerHTML = dashboardData.vancouver_phases.map(p => `
        <div style="background: var(--bg-secondary); border-radius: var(--radius-md); padding: 18px; border: 1px solid var(--border-subtle); display: flex; flex-direction: column; justify-content: space-between;">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: var(--accent-emerald);">Phase ${{p.phase_num}} • ${{p.weeks}}</span>
              <span style="font-size: 0.75rem; color: var(--text-muted);">${{p.date_range}}</span>
            </div>
            <h3 style="font-size: 1.05rem; font-weight: 700; color: var(--text-highlight); margin-bottom: 6px;">${{p.name}}</h3>
            <p style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.45; margin-bottom: 12px;">${{p.focus}}</p>
          </div>
          <div style="font-size: 0.85rem; font-weight: 700; color: var(--accent-emerald); font-family: 'JetBrains Mono', monospace; background: rgba(0,0,0,0.25); padding: 6px 10px; border-radius: 4px;">
            Target: ${{p.target_mileage_range}}
          </div>
        </div>
      `).join('');
    }}

    function renderIndicators() {{
      const container = document.getElementById('indicatorsGrid');
      if (!container || !dashboardData.proxy_indicators) return;

      container.innerHTML = dashboardData.proxy_indicators.map(ind => `
        <div class="indicator-card">
          <div>
            <div class="indicator-top">
              <div class="indicator-name">${{ind.name}}</div>
              <span class="indicator-status status-target">Active Proxy</span>
            </div>
            <div class="indicator-desc">${{ind.short_desc}}</div>

            <div class="indicator-metrics">
              <div class="metric-col">
                <div class="metric-label">Seattle '25</div>
                <div class="metric-num">${{ind.seattle_baseline}}</div>
              </div>
              <div class="metric-col">
                <div class="metric-label">Current</div>
                <div class="metric-num current">${{ind.current_value}}</div>
              </div>
              <div class="metric-col">
                <div class="metric-label">3:15 Goal</div>
                <div class="metric-num target">${{ind.target_value}}</div>
              </div>
            </div>
          </div>

          <div>
            <div class="indicator-why">
              <strong>Why Track:</strong> ${{ind.why_it_matters}}
            </div>
            <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 10px; display: flex; justify-content: space-between;">
              <span>Freq: ${{ind.tracking_frequency}}</span>
              <span style="font-family: monospace;">${{ind.formula}}</span>
            </div>
          </div>
        </div>
      `).join('');
    }}

    function renderWeeklyPlan() {{
      const container = document.getElementById('weeklyPlanContainer');
      if (!container) return;

      const activePlan = currentPlanRace === 'vancouver' 
        ? (dashboardData.vancouver_weekly_plan || []) 
        : (dashboardData.weekly_plan || []);

      const filtered = currentFilter === 'all' 
        ? activePlan 
        : activePlan.filter(w => w.phase === parseInt(currentFilter));

      const storagePrefix = currentPlanRace === 'vancouver' ? 'van_w_' : 'la_w_';

      container.innerHTML = filtered.map(w => {{
        const isDone = localStorage.getItem(storagePrefix + w.week) === 'true';
        
        const dailyRows = (w.daily_details || []).map(d => {{
          let badgeClass = 'run';
          if (d.miles === 0) badgeClass = 'rest';
          else if (d.workout.includes('Long Run') || d.workout.includes('PEAK') || d.workout.includes('REHEARSAL') || d.workout.includes('Simulation')) badgeClass = 'lr';
          else if (d.workout.includes('MARATHON') || d.workout.includes('BENCHMARK') || d.workout.includes('Race') || d.workout.includes('Time Trial')) badgeClass = 'race';

          let liftingHtml = '<span style="color: var(--text-muted); font-size: 0.8rem;">--</span>';
          if (d.lifting_type) {{
            liftingHtml = '<div style="font-weight: 700; color: var(--accent-purple); font-size: 0.83rem; margin-bottom: 2px;">' + d.lifting_type + '</div><div style="font-size: 0.77rem; color: var(--text-secondary); line-height: 1.35;">' + (d.lifting_exercises || '') + '</div>';
          }}

          return `
            <tr>
              <td>
                <span class="day-badge ${{badgeClass}}">${{d.day}}</span>
                <strong style="margin-left: 6px; color: var(--text-highlight);">${{d.day_full}}</strong>
              </td>
              <td class="daily-miles ${{d.miles === 0 ? 'rest' : ''}}">
                ${{d.miles > 0 ? d.miles + ' mi' : 'Rest'}}
              </td>
              <td>
                <strong style="color: var(--text-highlight);">${{d.workout}}</strong>
              </td>
              <td class="daily-pace">
                ${{d.pace}}
              </td>
              <td class="daily-hr">
                ${{d.hr_zone}}
              </td>
              <td>
                ${{liftingHtml}}
              </td>
              <td>
                <div class="daily-purpose">🎯 <strong>Purpose:</strong> ${{d.purpose}}</div>
                <div class="daily-instruction">${{d.description}}</div>
              </td>
            </tr>
          `;
        }}).join('');

        return `
          <div class="week-card" id="weekCard_${{w.week}}" style="${{isDone ? 'opacity: 0.6; border-color: rgba(16, 185, 129, 0.4);' : ''}}">
            <div class="week-card-main">
              <div class="week-badge">
                <div class="week-num">W${{w.week}}</div>
                <div class="week-tag">Phase ${{w.phase}}</div>
              </div>

              <div class="week-meta">
                <div class="week-dates">${{w.dates}}</div>
                <div class="week-miles">${{w.target_miles}} <span style="font-size: 0.8rem; color: var(--text-secondary); font-weight: normal;">mi</span></div>
              </div>

              <div class="week-details">
                <div class="workout-line">
                  <span class="workout-label lr">Long Run</span>
                  <strong>${{w.long_run}}</strong>
                </div>
                <div class="workout-line">
                  <span class="workout-label">Key Session</span>
                  <span>${{w.midweek_key}}</span>
                </div>
                <div class="workout-sub">
                  ${{w.structure}}
                </div>
                <div style="margin-top: 6px; display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                  <span style="font-size: 0.75rem; font-weight: 700; color: var(--accent-emerald); background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 4px; padding: 2px 8px; font-family: 'JetBrains Mono', monospace;">
                    📐 Daily Sum: ${{w.breakdown || ''}}
                  </span>
                  <button class="details-toggle-btn" id="btn_details_${{w.week}}" onclick="toggleWeekDetails(${{w.week}})">
                    <span>📋 View Day-by-Day Runs & Lifting (Mon–Sun)</span>
                    <span class="chevron">▼</span>
                  </button>
                </div>
              </div>

              <div class="week-checkpoint">
                <strong>Checkpoint:</strong><br>
                ${{w.proxy_checkpoint}}
              </div>

              <div class="week-check">
                <input type="checkbox" title="Mark Week Completed" ${{isDone ? 'checked' : ''}} onchange="toggleWeekDone(${{w.week}}, this.checked)">
              </div>
            </div>

            <!-- Collapsible Day-by-Day Details Drawer -->
            <div class="week-daily-breakdown" id="weekDetails_${{w.week}}" style="display: ${{allDetailsExpanded ? 'block' : 'none'}};">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid var(--border-subtle); padding-bottom: 8px; flex-wrap: wrap; gap: 8px;">
                <div style="font-weight: 700; font-size: 0.95rem; color: var(--text-highlight); display: flex; align-items: center; gap: 8px;">
                  <span>🗓️ Week ${{w.week}} Daily Running & Strength Schedule (Vancouver 2027):</span>
                  <span style="color: var(--accent-amber); font-family: 'JetBrains Mono', monospace; font-size: 0.9rem;">${{w.target_miles}} Miles Total</span>
                </div>
                <span style="font-size: 0.8rem; color: var(--text-muted);">${{w.dates}} • Phase ${{w.phase}}</span>
              </div>
              <div class="data-table-wrapper">
                <table class="daily-details-table">
                  <thead>
                    <tr>
                      <th style="min-width: 110px;">Day</th>
                      <th style="min-width: 75px;">Distance</th>
                      <th style="min-width: 170px;">Running Workout</th>
                      <th style="min-width: 140px;">Target Pace</th>
                      <th style="min-width: 140px;">Target HR</th>
                      <th style="min-width: 210px;">Strength / Lifting</th>
                      <th style="min-width: 260px;">Instructions & Coaching Notes</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${{dailyRows}}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        `;
      }}).join('');

      if (allDetailsExpanded) {{
        document.querySelectorAll('.details-toggle-btn').forEach(btn => {{
          btn.classList.add('active');
          btn.innerHTML = '<span>🔼 Hide Daily Details</span> <span class="chevron">▲</span>';
        }});
      }}
    }}

    function toggleWeekDetails(weekNum) {{
      const el = document.getElementById('weekDetails_' + weekNum);
      const btn = document.getElementById('btn_details_' + weekNum);
      if (!el) return;
      
      const isHidden = el.style.display === 'none' || el.style.display === '';
      if (isHidden) {{
        el.style.display = 'block';
        if (btn) {{
          btn.classList.add('active');
          btn.innerHTML = '<span>🔼 Hide Daily Details</span> <span class="chevron">▲</span>';
        }}
      }} else {{
        el.style.display = 'none';
        if (btn) {{
          btn.classList.remove('active');
          btn.innerHTML = '<span>📋 View Day-by-Day Runs (Mon–Sun)</span> <span class="chevron">▼</span>';
        }}
      }}
    }}

    function toggleAllDetails() {{
      allDetailsExpanded = !allDetailsExpanded;
      const allDrawers = document.querySelectorAll('.week-daily-breakdown');
      const allBtns = document.querySelectorAll('.details-toggle-btn');
      const toggleAllBtn = document.getElementById('toggleAllDetailsBtn');

      allDrawers.forEach(drawer => {{
        drawer.style.display = allDetailsExpanded ? 'block' : 'none';
      }});

      allBtns.forEach(btn => {{
        if (allDetailsExpanded) {{
          btn.classList.add('active');
          btn.innerHTML = '<span>🔼 Hide Daily Details</span> <span class="chevron">▲</span>';
        }} else {{
          btn.classList.remove('active');
          btn.innerHTML = '<span>📋 View Day-by-Day Runs (Mon–Sun)</span> <span class="chevron">▼</span>';
        }}
      }});

      if (toggleAllBtn) {{
        toggleAllBtn.textContent = allDetailsExpanded ? '🙈 Collapse All Week Details' : '👁️ Expand All Week Details';
        if (allDetailsExpanded) {{
          toggleAllBtn.classList.add('active');
        }} else {{
          toggleAllBtn.classList.remove('active');
        }}
      }}
    }}

    function filterPlan(phase) {{
      currentFilter = String(phase);
      document.querySelectorAll('.phase-pill').forEach(p => p.classList.remove('active'));
      const activePill = Array.from(document.querySelectorAll('.phase-pill')).find(p => {{
        if (phase === 'all') return p.textContent.includes('All');
        return p.textContent.includes('Phase ' + phase + ':') || p.textContent.includes('Phase ' + phase + ' ');
      }});
      if (activePill) activePill.classList.add('active');
      renderWeeklyPlan();
    }}

    function toggleWeekDone(weekNum, isChecked) {{
      const storagePrefix = currentPlanRace === 'vancouver' ? 'van_w_' : 'la_w_';
      localStorage.setItem(storagePrefix + weekNum, isChecked ? 'true' : 'false');
      renderWeeklyPlan();
    }}

    function renderSeattleRetrospective() {{
      const table = document.getElementById('seattleSplitsTable');
      if (!table || !dashboardData.seattle_baseline || !dashboardData.seattle_baseline.splits) return;

      table.innerHTML = dashboardData.seattle_baseline.splits.map(s => `
        <tr>
          <td><strong>${{s.segment}}</strong></td>
          <td>${{s.distance_km}} km</td>
          <td style="font-family: 'JetBrains Mono', monospace; font-weight: 600; color: ${{s.pace_min_mile < 8.0 ? 'var(--accent-emerald)' : 'var(--text-primary)'}};">
            ${{Math.floor(s.pace_min_mile)}}:${{Math.round((s.pace_min_mile % 1) * 60).toString().padStart(2, '0')}} / mi
          </td>
          <td style="font-family: 'JetBrains Mono', monospace; color: var(--accent-rose); font-weight: 600;">
            ${{s.avg_hr}} bpm
          </td>
        </tr>
      `).join('');
    }}

    function renderMonthlyHistory() {{
      const table = document.getElementById('monthlyHistoryTable');
      if (!table || !dashboardData.monthly_history) return;

      table.innerHTML = dashboardData.monthly_history.map(m => `
        <tr>
          <td><strong>${{m.month}}</strong></td>
          <td style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: var(--accent-amber);">${{m.total_miles}} mi</td>
          <td style="font-family: 'JetBrains Mono', monospace; color: var(--text-highlight);">${{Math.round(m.total_elevation_ft || 0).toLocaleString()}} ft <span style="font-size:0.75rem; color:var(--text-muted);">(${{m.avg_ft_per_mile}} ft/mi)</span></td>
          <td>${{m.run_count}} runs</td>
          <td style="font-family: 'JetBrains Mono', monospace;">${{m.longest_mile}} mi</td>
          <td style="font-family: 'JetBrains Mono', monospace;">${{Math.floor(m.avg_pace_min_mile)}}:${{Math.round((m.avg_pace_min_mile % 1) * 60).toString().padStart(2, '0')}} / mi</td>
          <td style="font-family: 'JetBrains Mono', monospace; color: var(--accent-cyan); font-weight: 600;">${{m.avg_gap_pace_min_mile ? Math.floor(m.avg_gap_pace_min_mile) + ':' + Math.round((m.avg_gap_pace_min_mile % 1) * 60).toString().padStart(2, '0') + ' / mi' : '--'}}</td>
          <td style="color: var(--accent-rose); font-family: 'JetBrains Mono', monospace;">${{m.avg_hr ? m.avg_hr + ' bpm' : '--'}}</td>
          <td>${{m.avg_cadence_spm ? m.avg_cadence_spm + ' spm' : '--'}}</td>
          <td style="font-family: 'JetBrains Mono', monospace; font-weight: 700;">
            <span style="color: var(--accent-emerald);">${{m.avg_ef ? m.avg_ef : '--'}}</span> / 
            <span style="color: var(--accent-purple);">${{m.avg_gap_ef ? m.avg_gap_ef : '--'}}</span>
          </td>
        </tr>
      `).join('');
    }}

    function renderRecentRuns() {{
      const table = document.getElementById('recentRunsTable');
      if (!table || !dashboardData.recent_runs) return;

      const runsRev = [...dashboardData.recent_runs].reverse();
      table.innerHTML = runsRev.map(r => `
        <tr>
          <td><strong>${{r.date}}</strong></td>
          <td style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: var(--accent-blue);">${{r.distance_miles}} mi</td>
          <td style="font-family: 'JetBrains Mono', monospace;">${{Math.floor(r.duration_seconds / 60)}}m ${{Math.round(r.duration_seconds % 60)}}s</td>
          <td style="font-family: 'JetBrains Mono', monospace; font-weight: 600;">${{Math.floor(r.pace_min_mile)}}:${{Math.round((r.pace_min_mile % 1) * 60).toString().padStart(2, '0')}} / mi</td>
          <td style="font-family: 'JetBrains Mono', monospace; color: var(--text-highlight);">+${{Math.round(r.elevation_gain_ft || 0)}} ft</td>
          <td style="font-family: 'JetBrains Mono', monospace; color: var(--text-muted);">${{r.elevation_ft_per_mile ? r.elevation_ft_per_mile.toFixed(0) : '--'}}</td>
          <td style="font-family: 'JetBrains Mono', monospace; color: var(--accent-cyan); font-weight: 600;">${{r.gap_pace_min_mile ? Math.floor(r.gap_pace_min_mile) + ':' + Math.round((r.gap_pace_min_mile % 1) * 60).toString().padStart(2, '0') + ' / mi' : '--'}}</td>
          <td style="color: var(--accent-rose); font-family: 'JetBrains Mono', monospace;">${{r.avg_hr ? r.avg_hr + ' bpm' : '--'}}</td>
          <td>${{r.avg_cadence_spm ? r.avg_cadence_spm + ' spm' : '--'}}</td>
          <td style="font-family: 'JetBrains Mono', monospace; font-weight: 700;">
            <span style="color: var(--accent-emerald);">${{r.ef ? r.ef : '--'}}</span> / 
            <span style="color: var(--accent-purple);">${{r.gap_ef ? r.gap_ef : '--'}}</span>
          </td>
        </tr>
      `).join('');
    }}

    function initCharts() {{
      if (typeof Chart === 'undefined') return;

      // 1. EF Trajectory Chart
      const ctxEF = document.getElementById('efChart');
      if (ctxEF && dashboardData.monthly_history) {{
        const labels = dashboardData.monthly_history.map(m => m.month);
        const actualEF = dashboardData.monthly_history.map(m => m.avg_ef);
        const actualGAPEF = dashboardData.monthly_history.map(m => m.avg_gap_ef);
        
        // Add target forward projection
        const extendedLabels = [...labels, '2026-10', '2026-11', '2026-12', '2027-01', '2027-02', '2027-03'];
        const targetCurve = new Array(labels.length - 1).fill(null);
        targetCurve.push(actualGAPEF[actualGAPEF.length - 1] || actualEF[actualEF.length - 1] || 1.34);
        targetCurve.push(1.36, 1.38, 1.40, 1.42, 1.43, 1.44);

        new Chart(ctxEF, {{
          type: 'line',
          data: {{
            labels: extendedLabels,
            datasets: [
              {{
                label: 'Historical Raw EF (Hilly Seattle Terrain)',
                data: actualEF,
                borderColor: '#38bdf8',
                backgroundColor: 'rgba(56, 189, 248, 0.05)',
                borderWidth: 2,
                pointRadius: 4,
                fill: true,
                tension: 0.3
              }},
              {{
                label: 'Grade-Adjusted EF (GAP-EF: Flat-Course Eq)',
                data: actualGAPEF,
                borderColor: '#a855f7',
                backgroundColor: 'rgba(168, 85, 247, 0.05)',
                borderWidth: 2,
                pointRadius: 4,
                pointBackgroundColor: '#a855f7',
                fill: false,
                tension: 0.3
              }},
              {{
                label: '3:15 Target Trajectory (≥ 1.42)',
                data: targetCurve,
                borderColor: '#10b981',
                borderDash: [5, 5],
                borderWidth: 2.5,
                pointRadius: 4,
                pointBackgroundColor: '#10b981',
                fill: false,
                tension: 0.3
              }}
            ]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
              legend: {{ labels: {{ color: '#94a3b8' }} }}
            }},
            scales: {{
              x: {{ grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8' }} }},
              y: {{ grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8' }}, min: 1.10, max: 1.48 }}
            }}
          }}
        }});
      }}

      // 2. Volume & Long Run Chart
      const ctxVol = document.getElementById('volumeChart');
      if (ctxVol && dashboardData.monthly_history) {{
        const labels = dashboardData.monthly_history.map(m => m.month);
        const miles = dashboardData.monthly_history.map(m => m.total_miles);
        const longest = dashboardData.monthly_history.map(m => m.longest_mile);

        new Chart(ctxVol, {{
          type: 'bar',
          data: {{
            labels: labels,
            datasets: [
              {{
                label: 'Monthly Total Miles',
                data: miles,
                backgroundColor: 'rgba(245, 158, 11, 0.4)',
                borderColor: '#f59e0b',
                borderWidth: 1,
                borderRadius: 4
              }},
              {{
                type: 'line',
                label: 'Longest Run (Miles)',
                data: longest,
                borderColor: '#a855f7',
                borderWidth: 2,
                pointRadius: 3,
                tension: 0.2
              }}
            ]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
              legend: {{ labels: {{ color: '#94a3b8' }} }}
            }},
            scales: {{
              x: {{ grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8' }} }},
              y: {{ grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8' }} }}
            }}
          }}
        }});
      }}

      // 3. Seattle Splits Chart
      const ctxSeattle = document.getElementById('seattleSplitsChart');
      if (ctxSeattle && dashboardData.seattle_baseline && dashboardData.seattle_baseline.splits) {{
        const segments = dashboardData.seattle_baseline.splits.map(s => s.segment);
        const paces = dashboardData.seattle_baseline.splits.map(s => s.pace_min_mile);
        const hrs = dashboardData.seattle_baseline.splits.map(s => s.avg_hr);

        new Chart(ctxSeattle, {{
          type: 'line',
          data: {{
            labels: segments,
            datasets: [
              {{
                label: 'Pace (min/mi)',
                data: paces,
                borderColor: '#38bdf8',
                borderWidth: 2,
                yAxisID: 'yPace',
                tension: 0.2
              }},
              {{
                label: 'Heart Rate (bpm)',
                data: hrs,
                borderColor: '#f43f5e',
                borderWidth: 2,
                yAxisID: 'yHR',
                tension: 0.2
              }}
            ]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{ legend: {{ labels: {{ color: '#94a3b8' }} }} }},
            scales: {{
              x: {{ grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8' }} }},
              yPace: {{
                type: 'linear',
                position: 'left',
                reverse: true,
                min: 7.4,
                max: 8.6,
                grid: {{ color: '#1e293b' }},
                ticks: {{ color: '#38bdf8' }}
              }},
              yHR: {{
                type: 'linear',
                position: 'right',
                min: 140,
                max: 175,
                grid: {{ drawOnChartArea: false }},
                ticks: {{ color: '#f43f5e' }}
              }}
            }}
          }}
        }});
      }}

      // 4. Interactive Proxy Indicator Historical Time Series Chart
      updateProxyTsChart();
    }}

    let currentTsMetric = 'gap_ef';
    let currentTsGranularity = 'weekly';
    let proxyTsChartInstance = null;

    function setTsMetric(metricId) {{
      currentTsMetric = metricId;
      document.querySelectorAll('.metric-btn').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById('tsBtn_' + metricId);
      if (activeBtn) activeBtn.classList.add('active');
      updateProxyTsChart();
    }}

    function setTsGranularity(gran) {{
      currentTsGranularity = gran;
      document.querySelectorAll('.granularity-btn').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById('granBtn_' + gran);
      if (activeBtn) activeBtn.classList.add('active');
      updateProxyTsChart();
    }}

    function updateProxyTsChart() {{
      const canvas = document.getElementById('proxyTsChart');
      if (!canvas || typeof Chart === 'undefined') return;

      const isWeekly = currentTsGranularity === 'weekly';
      const rawData = isWeekly 
        ? (dashboardData.weekly_time_series || []) 
        : (dashboardData.daily_time_series || []);

      if (!rawData || rawData.length === 0) return;

      const headingEl = document.getElementById('tsChartHeading');
      const badgeEl = document.getElementById('tsMetricBadge');
      const descEl = document.getElementById('tsChartDescription');

      let chartLabel = '';
      let chartColor = '#a855f7';
      let chartFillBg = 'rgba(168, 85, 247, 0.08)';
      let targetGoal = null;
      let targetLabel = '';
      let isReverseY = false;
      let yAxisTitle = '';
      let secondaryDataset = null;

      const labels = rawData.map(d => d.date);
      let values = [];

      if (currentTsMetric === 'gap_ef') {{
        chartLabel = isWeekly ? 'Weekly Mean Grade-Adjusted EF (GAP-EF)' : 'Per-Run Grade-Adjusted EF (GAP-EF)';
        chartColor = '#a855f7';
        chartFillBg = 'rgba(168, 85, 247, 0.08)';
        yAxisTitle = 'Speed m/s * 60 / HR';
        targetGoal = 1.45;
        targetLabel = 'Sub-3:15 Goal (≥ 1.45)';
        values = rawData.map(d => isWeekly ? d.avg_gap_ef : d.gap_ef);
        if (headingEl) headingEl.innerText = '📈 Proxy Indicator Time Series: Grade-Adjusted Efficiency Factor (GAP-EF)';
        if (badgeEl) {{ badgeEl.innerText = 'Grade-Adjusted'; badgeEl.style.color = 'var(--accent-purple)'; }}
        if (descEl) descEl.innerText = 'Speed normalized for Seattle climb gradients (ft/mi) divided by Average Heart Rate. Accounts for vertical elevation so you are credited for climbing power.';
      }} else if (currentTsMetric === 'ef') {{
        chartLabel = isWeekly ? 'Weekly Mean Raw Aerobic EF' : 'Per-Run Raw Aerobic EF';
        chartColor = '#38bdf8';
        chartFillBg = 'rgba(56, 189, 248, 0.08)';
        yAxisTitle = 'Speed m/s * 60 / HR';
        targetGoal = 1.42;
        targetLabel = 'Sub-3:15 Goal (≥ 1.42)';
        values = rawData.map(d => isWeekly ? d.avg_ef : d.ef);
        if (headingEl) headingEl.innerText = '⚡ Proxy Indicator Time Series: Raw Aerobic Efficiency Factor (EF)';
        if (badgeEl) {{ badgeEl.innerText = 'Raw Aerobic'; badgeEl.style.color = 'var(--accent-blue)'; }}
        if (descEl) descEl.innerText = 'Speed (m/min) divided by Average Heart Rate. Pure aerobic work capacity in Zone 2. As EF approaches 1.42, flat aerobic pace hits ~7:25 cruising speed.';
      }} else if (currentTsMetric === 'pace') {{
        chartLabel = isWeekly ? 'Weekly Mean Raw Pace (min/mi)' : 'Per-Run Raw Pace (min/mi)';
        chartColor = '#f59e0b';
        chartFillBg = 'rgba(245, 158, 11, 0.04)';
        isReverseY = true;
        yAxisTitle = 'Pace (min/mi)';
        targetGoal = 7.42;
        targetLabel = 'Target Marathon Pace (7:25 / mi)';
        values = rawData.map(d => isWeekly ? d.avg_pace : d.pace_min_mile);
        
        const gapValues = rawData.map(d => isWeekly ? d.avg_gap_pace : d.gap_pace_min_mile);
        secondaryDataset = {{
          label: isWeekly ? 'Weekly Grade-Adjusted Pace (Flat Eq)' : 'Per-Run Grade-Adjusted Pace (Flat Eq)',
          data: gapValues,
          borderColor: '#10b981',
          borderWidth: 2,
          pointRadius: isWeekly ? 4 : 2,
          pointBackgroundColor: '#10b981',
          tension: 0.25,
          fill: false
        }};

        if (headingEl) headingEl.innerText = '⏱️ Proxy Indicator Time Series: Pace vs Grade-Adjusted Pace (GAP)';
        if (badgeEl) {{ badgeEl.innerText = 'Pace Telemetry'; badgeEl.style.color = 'var(--accent-amber)'; }}
        if (descEl) descEl.innerText = 'Comparison between raw GPS watch pace and hill-compensated flat-course equivalent pace (GAP). Inverts Y-axis so faster pace points upward.';
      }} else if (currentTsMetric === 'hr') {{
        chartLabel = isWeekly ? 'Weekly Mean Heart Rate (bpm)' : 'Per-Run Average Heart Rate (bpm)';
        chartColor = '#f43f5e';
        chartFillBg = 'rgba(244, 63, 94, 0.08)';
        yAxisTitle = 'Heart Rate (bpm)';
        targetGoal = 153.0;
        targetLabel = 'Target Zone 3 Ceiling (~153 bpm)';
        values = rawData.map(d => d.avg_hr);

        if (headingEl) headingEl.innerText = '❤️ Proxy Indicator Time Series: Aerobic Heart Rate Stability';
        if (badgeEl) {{ badgeEl.innerText = 'Heart Rate'; badgeEl.style.color = 'var(--accent-rose)'; }}
        if (descEl) descEl.innerText = 'Cardiovascular demand across runs. Tracks cardiac efficiency as pace quickens without driving HR into threshold zones.';
      }} else if (currentTsMetric === 'vdot') {{
        chartLabel = isWeekly ? 'Weekly Estimated Daniels VDOT' : 'Per-Run Estimated Daniels VDOT';
        chartColor = '#06b6d4';
        chartFillBg = 'rgba(6, 182, 212, 0.08)';
        yAxisTitle = 'Daniels VDOT Score';
        targetGoal = 50.6;
        targetLabel = '3:15 Target VDOT (50.6)';
        values = rawData.map(d => d.vdot || (isWeekly ? d.avg_vdot : null));

        if (headingEl) headingEl.innerText = '🎯 Proxy Indicator Time Series: Daniels VDOT Aerobic Power Score';
        if (badgeEl) {{ badgeEl.innerText = 'Daniels VDOT'; badgeEl.style.color = 'var(--accent-cyan)'; }}
        if (descEl) descEl.innerText = 'Empirical Jack Daniels VDOT score calculated from workout Grade-Adjusted Pace. The Seattle 2025 baseline was 47.1 (flat eq), with the 3:15 target at 50.6.';
      }} else if (currentTsMetric === 'volume') {{
        chartLabel = isWeekly ? 'Weekly Mileage' : 'Daily Run Miles';
        chartColor = '#f59e0b';
        chartFillBg = 'rgba(245, 158, 11, 0.15)';
        yAxisTitle = 'Miles';
        targetGoal = 52.0;
        targetLabel = 'Peak Target Volume (52 mpw)';
        values = rawData.map(d => isWeekly ? d.total_miles : d.distance_miles);

        if (isWeekly) {{
          const rollValues = rawData.map(d => d.rolling_4w_mpw);
          secondaryDataset = {{
            label: 'Rolling 4-Week Average MPW',
            data: rollValues,
            borderColor: '#38bdf8',
            borderWidth: 2.5,
            borderDash: [4, 4],
            pointRadius: 3,
            tension: 0.3,
            fill: false
          }};
        }}

        if (headingEl) headingEl.innerText = '📊 Proxy Indicator Time Series: Chronic Volume & MPW Trajectory';
        if (badgeEl) {{ badgeEl.innerText = 'Mileage Volume'; badgeEl.style.color = 'var(--accent-amber)'; }}
        if (descEl) descEl.innerText = 'Weekly mileage volume building through the 31-week periodization cycle alongside chronic 4-week rolling load.';
      }} else if (currentTsMetric === 'decoupling') {{
        chartLabel = isWeekly ? 'Weekly Aerobic Decoupling (%)' : 'Per-Run Decoupling (%) on Long Runs';
        chartColor = '#e11d48';
        chartFillBg = 'rgba(225, 29, 72, 0.08)';
        yAxisTitle = 'Cardiac Drift (%)';
        targetGoal = 4.0;
        targetLabel = 'Target Max Drift (≤ 4.0%)';
        values = rawData.map(d => d.decoupling_pct);

        if (headingEl) headingEl.innerText = '📉 Proxy Indicator Time Series: Aerobic Decoupling (Cardiac Drift)';
        if (badgeEl) {{ badgeEl.innerText = 'Decoupling'; badgeEl.style.color = 'var(--accent-rose)'; }}
        if (descEl) descEl.innerText = 'Percentage drop in efficiency factor between 1st half and 2nd half of long runs (> 10 miles). Lower drift confirms glycogen economy and heat resilience.';
      }}

      const datasets = [
        {{
          label: chartLabel,
          data: values,
          borderColor: chartColor,
          backgroundColor: chartFillBg,
          borderWidth: isWeekly ? 2.5 : 1.5,
          pointRadius: isWeekly ? 3.5 : 2,
          pointBackgroundColor: chartColor,
          tension: 0.25,
          fill: true
        }}
      ];

      if (secondaryDataset) {{
        datasets.push(secondaryDataset);
      }}

      if (targetGoal !== null) {{
        datasets.push({{
          label: targetLabel,
          data: new Array(labels.length).fill(targetGoal),
          borderColor: '#10b981',
          borderDash: [6, 6],
          borderWidth: 2,
          pointRadius: 0,
          fill: false,
          tension: 0
        }});
      }}

      if (proxyTsChartInstance) {{
        proxyTsChartInstance.destroy();
      }}

      proxyTsChartInstance = new Chart(canvas, {{
        type: 'line',
        data: {{
          labels: labels,
          datasets: datasets
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          interaction: {{
            mode: 'index',
            intersect: false
          }},
          plugins: {{
            legend: {{
              labels: {{ color: '#94a3b8', font: {{ family: 'Plus Jakarta Sans', size: 12 }} }}
            }},
            tooltip: {{
              callbacks: {{
                label: function(context) {{
                  let val = context.parsed.y;
                  if (val === null || val === undefined) return null;
                  if (currentTsMetric === 'pace' && (context.datasetIndex === 0 || context.datasetIndex === 1)) {{
                    const m = Math.floor(val);
                    const s = Math.round((val % 1) * 60).toString().padStart(2, '0');
                    return context.dataset.label + ': ' + m + ':' + s + ' / mi';
                  }}
                  return context.dataset.label + ': ' + val;
                }}
              }}
            }}
          }},
          scales: {{
            x: {{
              grid: {{ color: '#1e293b' }},
              ticks: {{
                color: '#94a3b8',
                maxTicksLimit: isWeekly ? 16 : 14,
                font: {{ family: 'JetBrains Mono', size: 11 }}
              }}
            }},
            y: {{
              title: {{
                display: true,
                text: yAxisTitle,
                color: '#94a3b8',
                font: {{ family: 'Plus Jakarta Sans', size: 11 }}
              }},
              reverse: isReverseY,
              grid: {{ color: '#1e293b' }},
              ticks: {{
                color: '#94a3b8',
                font: {{ family: 'JetBrains Mono', size: 11 }},
                callback: function(value) {{
                  if (currentTsMetric === 'pace') {{
                    const m = Math.floor(value);
                    const s = Math.round((value % 1) * 60).toString().padStart(2, '0');
                    return m + ':' + s;
                  }}
                  return value;
                }}
              }}
            }}
          }}
        }}
      }});
    }}

    // Calculator Functions
    function calculateEF() {{
      const dist = parseFloat(document.getElementById('calcDist').value) || 0;
      const min = parseFloat(document.getElementById('calcDurMin').value) || 0;
      const sec = parseFloat(document.getElementById('calcDurSec').value) || 0;
      const hr = parseFloat(document.getElementById('calcHR').value) || 0;
      const elev = parseFloat(document.getElementById('calcElev').value) || 0;

      const totalSec = (min * 60) + sec;
      if (dist <= 0 || totalSec <= 0 || hr <= 0) return;

      const rawPaceSec = totalSec / dist;
      const rawPaceMinMile = rawPaceSec / 60.0;
      const distMeters = dist * 1609.34;
      const speedMps = distMeters / totalSec;
      const ef = (speedMps * 60.0) / hr;

      // Grade adjusted pace calculation: ~0.35s deduction per ft/mi climb
      const ftPerMile = elev / dist;
      const gapSecDeduction = ftPerMile * 0.35;
      const gapPaceSec = Math.max(1, rawPaceSec - gapSecDeduction);
      const gapPaceMinMile = gapPaceSec / 60.0;
      const gapSpeedMps = 1609.34 / gapPaceSec;
      const gapEf = (gapSpeedMps * 60.0) / hr;

      document.getElementById('efResultVal').textContent = ef.toFixed(3);
      if (document.getElementById('gapEfResultVal')) {{
        document.getElementById('gapEfResultVal').textContent = gapEf.toFixed(3);
      }}

      const rawPaceStr = Math.floor(rawPaceMinMile) + ':' + Math.round((rawPaceMinMile % 1) * 60).toString().padStart(2, '0') + '/mi';
      const gapPaceStr = Math.floor(gapPaceMinMile) + ':' + Math.round((gapPaceMinMile % 1) * 60).toString().padStart(2, '0') + '/mi';
      if (document.getElementById('gapPaceText')) {{
        document.getElementById('gapPaceText').textContent = 'Raw Pace: ' + rawPaceStr + ' ➔ Flat Equivalent GAP: ' + gapPaceStr + ' (+' + Math.round(ftPerMile) + ' ft/mi)';
      }}
      
      let verdict = '';
      if (gapEf >= 1.42) {{
        verdict = '🔥 Outstanding! GAP-EF is ≥ 1.42 — you have arrived at full 3:15 aerobic capacity!';
      }} else if (gapEf >= 1.37) {{
        verdict = '✅ Strong progress (GAP-EF: ' + gapEf.toFixed(3) + '). Approaching peak cycle fitness for sub-3:15 pacing.';
      }} else if (gapEf >= 1.32) {{
        verdict = '🟢 Solid aerobic baseline (GAP-EF: ' + gapEf.toFixed(3) + '). Seattle hill tax is offset; Zone 2 volume will push this to 1.38+ over Phase 1 & 2.';
      }} else {{
        verdict = 'ℹ️ GAP-EF: ' + gapEf.toFixed(3) + '. Keep building steady aerobic miles in Phase 1 to establish the 1.34+ baseline.';
      }}
      document.getElementById('efVerdict').textContent = verdict;
    }}

    function calculateVDOT() {{
      const event = document.getElementById('raceEvent').value;
      const h = parseFloat(document.getElementById('raceHr').value) || 0;
      const m = parseFloat(document.getElementById('raceMin').value) || 0;
      const s = parseFloat(document.getElementById('raceSec').value) || 0;

      const totalMin = (h * 60) + m + (s / 60.0);
      if (totalMin <= 0) return;

      // Approximate Daniels VDOT & Marathon conversion
      let vdot = 45.0;
      if (event === '5k') {{
        vdot = (totalMin <= 19.5) ? 52.0 : (totalMin <= 20.3) ? 50.5 : (totalMin <= 21.5) ? 47.5 : (totalMin <= 22.5) ? 45.5 : 43.0;
      }} else if (event === '10k') {{
        vdot = (totalMin <= 40.5) ? 52.5 : (totalMin <= 42.25) ? 50.5 : (totalMin <= 44.5) ? 47.5 : (totalMin <= 46.5) ? 45.5 : 43.0;
      }} else if (event === 'half') {{
        vdot = (totalMin <= 90.0) ? 52.5 : (totalMin <= 93.5) ? 50.5 : (totalMin <= 98.0) ? 47.5 : (totalMin <= 103.0) ? 45.5 : 43.0;
      }}

      // Projected marathon based on VDOT
      let predMarathonMin = 0;
      if (vdot >= 52.0) predMarathonMin = 190.0; // 3:10
      else if (vdot >= 50.5) predMarathonMin = 195.0; // 3:15:00
      else if (vdot >= 49.0) predMarathonMin = 200.0; // 3:20
      else if (vdot >= 47.5) predMarathonMin = 206.0; // 3:26
      else if (vdot >= 45.5) predMarathonMin = 214.0; // 3:34
      else predMarathonMin = 225.0;

      const predH = Math.floor(predMarathonMin / 60);
      const predM = Math.floor(predMarathonMin % 60);
      const predS = Math.round((predMarathonMin % 1) * 60);

      document.getElementById('vdotMarathonPred').textContent = `${{predH}}:${{predM.toString().padStart(2, '0')}}:${{predS.toString().padStart(2, '0')}}`;
      document.getElementById('vdotScoreText').textContent = `Calculated VDOT: ${{vdot.toFixed(1)}} (Goal: 50.5)`;

      let pct = Math.min(100, Math.round((vdot / 50.5) * 100));
      let verdict = '';
      if (vdot >= 50.5) {{
        verdict = `🎯 Readiness: 100%! This performance matches or exceeds 3:15:00 capability (VDOT ≥ 50.5).`;
      }} else if (vdot >= 48.5) {{
        verdict = `📈 Readiness: ${{pct}}%. Strong trajectory. You are within 5 minutes of 3:15 shape with training runway remaining.`;
      }} else {{
        verdict = `⏳ Readiness: ${{pct}}%. Consistent base building and threshold workouts over Weeks 6-16 will bridge this gap.`;
      }}
      document.getElementById('vdotVerdict').textContent = verdict;
    }}

    // Auto-initialize on DOM ready
    window.addEventListener('DOMContentLoaded', init);
  </script>
</body>
</html>
"""

    with open(OUTPUT_HTML, 'w') as f:
        f.write(html_content)

    print(f"✅ Generated standalone index.html at {OUTPUT_HTML} ({len(html_content)} bytes)")

if __name__ == "__main__":
    generate()
