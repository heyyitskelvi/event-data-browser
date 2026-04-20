import pandas as pd

def fetch_and_clean():
    url = "https://genconreg-production.s3.amazonaws.com/exports/events.xlsx"
    # Load only the columns you actually care about to keep JSON small
    df = pd.read_excel(url)
    
    # Example: Simple cleaning
    df.columns = [c.strip() for c in df.columns]
    
    # Save as JSON for the browser
    df.to_json('events.json', orient='records')

if __name__ == "__main__":
    fetch_and_clean()
