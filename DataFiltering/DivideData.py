import pandas as pd
# 读取CSV文件
df = pd.read_csv('Valid_NoDuplicate_djl.csv')

# 计算总行数
total_rows = df.shape[0]

# 计算需要的子数据框数量
num_subframes = (total_rows // 10) + (1 if total_rows % 10 != 0 else 0)

# 分割数据框并保存
for i in range(num_subframes):
    start_row = i * 10
    end_row = min(start_row + 10, total_rows)
    subframe = df.iloc[start_row:end_row]
    subframe.to_csv(f'users/subframe_{i+1}.csv', index=False)

print(f'{num_subframes} subframes have been created.')
