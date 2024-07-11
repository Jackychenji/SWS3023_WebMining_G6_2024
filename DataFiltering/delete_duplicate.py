import pandas as pd

# 读取数据
df_results = pd.read_csv('combine/results_djl_zs.csv')
names = set(df_results['user'])

df_user_list = pd.read_csv("user_list_djl.csv")
name_djl = df_user_list['user']

# 过滤名字
filtered_name_djl = name_djl[~name_djl.isin(names)]

# 将结果保存回CSV文件
df_filtered = df_user_list[df_user_list['user'].isin(filtered_name_djl)]
df_filtered.to_csv("filtered_user_list_djl.csv", index=False)

# 输出结果
print(df_filtered)
