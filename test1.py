import pandas as pd
from sklearn.preprocessing import StandardScaler

# อ่านไฟล์ CSV และโหลดข้อมูลลงใน DataFrame
df = pd.read_csv('01-warm-0.csv')

# แปลงคอลัมน์ LocalTimestamp เป็น datetime
df['LocalTimestamp'] = pd.to_datetime(df['LocalTimestamp'], unit='s')

# กำหนดคอลัมน์ LocalTimestamp เป็น index
df.set_index('LocalTimestamp', inplace=True)

# รวมข้อมูลในระยะเวลา 1 วินาที
result = df.resample('1S').max().fillna(0)

print(result)


# # กำหนดคอลัมน์ LocalTimestamp เป็นคอลัมน์ปกติ
result.reset_index(inplace=True)
# #
# print(normalized_result)
# # บันทึกผลลัพธ์ Normalize ลงในไฟล์ CSV ใหม่
# result.to_csv('01-Guitar-Warm-Resampled.csv', index=False)


