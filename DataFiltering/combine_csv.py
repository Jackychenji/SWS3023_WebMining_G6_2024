import pandas as pd
import os

# 设置文件夹路径
folder_path = 'filter'

# 获取所有 CSV 文件的文件名列表
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# 初始化一个空的数据框
combined_df = pd.DataFrame()

# 逐个读取 CSV 文件并合并到数据框中
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)
    combined_df = pd.concat([combined_df, df], ignore_index=True)

# 保存合并后的数据框到新的 CSV 文件
combined_df.to_csv('Valid_NoDuplicate_djl.csv', index=False)
