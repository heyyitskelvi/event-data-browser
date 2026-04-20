import pandas as pd

def fetch_and_clean():
    url = "https://genconreg-production.s3.amazonaws.com/exports/events.xlsx"
    df = pd.read_excel(url)
    dt_objs = pd.to_datetime(df['Start Date & Time'])
    df['Day'] = dt_objs.dt.day_name()
    df['Time'] = dt_objs.dt.strftime('%I:%M %p')
    df.to_json('events.json', orient='records')

if __name__ == "__main__":
    fetch_and_clean()
