import pandas as pd

# อ่านข้อมูลจาก CSV
df = pd.read_csv('01-Guitar-Warm-Resampled.csv')

# แปลงคอลัมน์ 'LocalTimestamp' เป็น datetime
df['LocalTimestamp'] = pd.to_datetime(df['LocalTimestamp'])

# กำหนดให้ 'LocalTimestamp' เป็น index
df.set_index('LocalTimestamp', inplace=True)

# แบ่งข้อมูลทุก 15 วินาที
interval = '15S'
dfs_by_interval = [group for name, group in df.groupby(pd.Grouper(freq=interval))]

# สร้างไฟล์ CSV สำหรับแต่ละช่วงเวลา 15 วินาที
for i, df_interval in enumerate(dfs_by_interval):
    filename = f'output_{i}.csv'
    df_interval.to_csv(filename)
    print(f'Saved {filename}')
