#!/usr/bin/env python3
"""
sync_and_update.py - Sync newest Garmin runs and rebuild dashboard_data.json
"""

import os
import sys
import subprocess

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.abspath(os.path.join(REPO_DIR, "../../.."))
HEATMAP_SYNC = os.path.join(WORKSPACE_ROOT, "Projects/running-heatmap/repo/sync_garmin.py")
BUILD_DATA = os.path.join(REPO_DIR, "build_data.py")
GENERATE_HTML = os.path.join(REPO_DIR, "generate_dashboard_html.py")

def main():
    print("🏃 Syncing latest runs for LA Marathon 2027 Dashboard...")
    if os.path.exists(HEATMAP_SYNC):
        print("\n1️⃣ Running Garmin Connect sync via running-heatmap engine...")
        try:
            subprocess.run([sys.executable, HEATMAP_SYNC], check=False)
        except Exception as e:
            print(f"⚠️ Garmin sync notice: {e}")
    else:
        print("ℹ️ Garmin sync script not found, proceeding directly to data rebuild.")

    print("\n2️⃣ Rebuilding dashboard metrics...")
    subprocess.run([sys.executable, BUILD_DATA], check=True)
    
    print("\n3️⃣ Compiling updated index.html dashboard...")
    subprocess.run([sys.executable, GENERATE_HTML], check=True)
    
    print("\n🎉 Dashboard successfully updated and re-compiled! Refresh your browser tab to view.")

if __name__ == "__main__":
    main()
