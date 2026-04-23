import pandas as pd
import json
import os
from datetime import datetime

def fetch_and_clean():
    url = "https://genconreg-production.s3.amazonaws.com/exports/events.xlsx"
    new_df = pd.read_excel(url)
    
    dt_objs = pd.to_datetime(new_df['Start Date & Time'])
    new_df['Day'] = dt_objs.dt.day_name()
    new_df['Time'] = dt_objs.dt.strftime('%I:%M %p')

    changelog_file = 'changelog.json'
    history = []
    if os.path.exists(changelog_file):
        with open(changelog_file, 'r') as f:
            history = json.load(f)

    if os.path.exists('events.json'):
        old_df = pd.read_json('events.json')
        
        new_ids = set(new_df['Game ID']) - set(old_df['Game ID'])

        removed_ids = set(old_df['Game ID']) - set(new_df['Game ID'])
        
        if new_ids or removed_ids:
            history.insert(0, {
                "timestamp": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
                "added": len(new_ids),
                "removed": len(removed_ids)
            })

            history = history[:10]
            
        with open(changelog_file, 'w') as f:
            json.dump(history, f)


    new_df.to_json('events.json', orient='records')

if __name__ == "__main__":
    fetch_and_clean()
