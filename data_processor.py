import pandas as pd

def fetch_and_clean():
    df = pd.read_excel("https://genconreg-production.s3.amazonaws.com/exports/events.xlsx")
    df['Day'] = pd.to_datetime(df['Start Date & Time']).dt.day_name()
    df.to_json('events.json', orient='records')

if __name__ == "__main__":
    fetch_and_clean()