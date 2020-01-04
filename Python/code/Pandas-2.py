# Pandas-2.py
# 对数据集应用函数
# 有时候你会想以某些方式操作数据集中的数据。
# 例如，如果你有一列年份的数据而你希望创建一个新的列显示这些年份所对应的年代
# Pandas对此给出了两个非常有用的函数，apply和applymap

# Applying a function to a column
def base_year(year):
	base_year = year[:4]
	base_year = pd.to_date_time(base_year).year
	return base_year

df['year'] = df.water_year.apply(base_year)
df.head(5)
# 这会创建一个名为‘year‘的新列。这一列是由’water_year’列所导出的,它获取的是主年份。这便是使用apply的方法，即如何对一列应用一个函数。
# 如果你想对整个数据集应用某个函数，你可以使用dataset.applymap()


# 另一件经常会对dataframe所做的操作是为了让它们呈现出一种更便于使用的形式而对它们进行的重构

# Manipulating structure (groupby, unstack, pivot)
# Groupby
df.groupby(df.year // 10 * 10).max()
# grouby所做的是将你所选择的列组成一组。上述代码首先将年代组成一组。
# 虽然这样做没有给我们带来任何便利，但我们可以紧接着在这个基础上调用其它方法，例如max, min, mean等。
# 例子中，我们可以得到90年代的均值。
 

# unstacking
# 它的功能是将某一列前置成为列标签。我们最好如下看看它的实际效果。
decade_rain.unstack(0)
# 这个操作会将我们在上面小节创建的dataframe转变成如下形式。它将标识‘year’索引的第0列推起来，变为了列标签。


# pivot实际上是在本文中我们已经见过的操作的组合。首先，它设置了一个新的索引(set_index()),然后它对这个索引排序(sort_index())，最后它会进行unstack操作
# 组合起来就是一个pivot
# Pivoting
# does set_index, sort_index & unstack in a row
high_rain.pivot('year', 'rain_octsep')[['outflow_octsep',
				'outflow_decfeb','outflow_junaug']].fillna('')


# 合并数据集
# 有时候你有两个单独的数据集，它们直接相互关联，而你想要比较它们的差异或者合并它们。
# Merging 2 datasets together
rain_jpn = pd.read_csv('filepath')
rain_jpn.columns = ['year', 'jpn_rainfall']

uk_jpn_rain = df.merge(rain_jpn, on = "year")
uk_jpn_rain.head(5)
# 开始时你需要通过’on’关键字参数指定你想要合并的列。


# 采用Pandas快速绘制图表
# Using pandas to quickly plot graphs
uk_jpn_rain.plot(x = 'year', y = ['rain_octsep','jpn_rainfall'])

# saving your data to a csv
df.to_csv('uk_rain.csv')