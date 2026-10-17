import pandas as pd
import json
import os
from datetime import datetime

def fetch_and_clean():
    url = "https://genconreg-production.s3.amazonaws.com/exports/events.xlsx"
    df = pd.read_excel(url)
    
    gc_format = '%m/%d/%Y %I:%M %p'
    
    # Standard Date/Time Processing
    start_dt = pd.to_datetime(df['Start Date & Time'], format=gc_format)
    df['Day'] = start_dt.dt.day_name()
    df['Time'] = start_dt.dt.strftime('%I:%M %p')
    df['EndTime'] = pd.to_datetime(df['End Date & Time'], format=gc_format).dt.strftime('%I:%M %p')
    
    # Numeric conversions
    df['Tickets Available'] = pd.to_numeric(df['Tickets Available'], errors='coerce').fillna(0)
    df['Maximum Players'] = pd.to_numeric(df['Maximum Players'], errors='coerce').fillna(0)
    df['Cost $'] = pd.to_numeric(df['Cost $'], errors='coerce').fillna(0)
    
    # --- Change Log Logic ---
    changelog_file = 'changelog.json'
    history = []
    if os.path.exists(changelog_file):
        with open(changelog_file, 'r') as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []

    if os.path.exists('events.json'):
        try:
            old_df = pd.read_json('events.json')
            
            # Ensure 'Game ID' exists in both dataframes before comparing
            if 'Game ID' in df.columns and 'Game ID' in old_df.columns:
                new_ids = list(set(df['Game ID']) - set(old_df['Game ID']))
                removed_ids = list(set(old_df['Game ID']) - set(df['Game ID']))
                
                if new_ids or removed_ids:
                    history.insert(0, {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
                        "added_count": len(new_ids),
                        "removed_count": len(removed_ids),
                        "added_ids": new_ids,
                        "removed_ids": removed_ids
                    })
                    history = history[:10]
                    
                    with open(changelog_file, 'w') as f:
                        json.dump(history, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not process old events.json for changelog: {e}")

    # Save fresh data
    df.to_json('events.json', orient='records')

if __name__ == "__main__":
    fetch_and_clean()
