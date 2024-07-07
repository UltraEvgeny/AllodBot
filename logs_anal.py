import pandas as pd
import json
from utils.funcs import dataframe_to_sheet

with open('logs.txt', 'r', encoding='utf-8') as f:
    events = [json.loads(x) for x in f.readlines()]


writer = pd.ExcelWriter("logs_anal.xlsx", engine='xlsxwriter')
df = pd.DataFrame(events)
df['dt'] = pd.to_datetime(df['dt'], format='%Y-%m-%d %H:%M:%S')
df = df.sort_values(by='dt')
df['time_spent'] = (df['dt'] - df['dt'].shift(1)).dt.total_seconds()
dataframe_to_sheet(writer, df, 'raw_data')
df = df.sort_values(by='time_spent')
df = df[(df['event'] != 'session_start') & (df['time_spent'] < 300)].sort_values(by='dt')
dataframe_to_sheet(writer, df, 'df')
dataframe_to_sheet(writer, df.groupby('event')['time_spent'].sum().reset_index(), 'sum_times')
writer.close()

