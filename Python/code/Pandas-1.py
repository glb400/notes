# Pandas.py

import pandas as pd

# pandas的两种数据类型：series & dataframe
# series：一维数据结构，类似于numpy中元素带标签的数组
# dataframe：二维表结构，类似于series的字典项

# Reading a csv into Pandas
# header关键字告诉Pandas这些数据是否有列名，在哪里。如果没有列名，你可以将其置为None。
df = pd.read_csv('filepath',header = 0)

# Getting first x rows
df.head(5)

# Getting last x rows
df.tail(5)

# Changing column labels
df.columns = ['water_year','rain_octsep','outflow_octsep',
			  'rain_decfeb','outflow_decfeb','rain_junaug',
			  'outflow_junaug']

df.head(5)

len(df)


# Finding out basic statistical information on your dataset.
# 这将返回一个包含多种统计信息的表格，例如，计数，均值，标准方差等
# Limit output to 3 decimal places
pd.options.display.float_format = '{:,.3f}'.format
df.describe()

# Getting a column by label
df['rain_octsep']
# Getting a column by label using .
df.rain_octsep

# Creating a series of booleans based on a conditional
df.rain_octsep < 1000 
# 上述代码将范围一个布尔值的dataframe，其中，如果9、10月的降雨量低于1000毫米，则对应的布尔值为‘True’,反之，则为’False’。
# Filtering by mutiple conditions
df[(df.rain_octsep < 1000) & (df.outflow_octsep < 4000)]

# Filtering by string method
df[df.water_year.str.startswith('199')]


# Getting a row via a numerical index
df.iloc[30]
# Getting a row via a label-based index
df.loc['2000/01']


# Setting a new index from an existing column
df = df.set_index(['water_year'])

# sort the table: inplace= True to apple the sorting in place
df.sort_index(ascending = False).head(5)

# Returning an index to data
df = df.reset_index('water_year')