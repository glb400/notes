#CART算法
#输入：训练数据集D，停止计算的条件
#输出：CART决策树

#根据训练数据集，从根结点开始，递归地对每个结点进行以下操作，构建二叉树：
#Step1：设结点的训练数据集为D，计算现有特征对该数据集的基尼指数。此时，对每一个特征A，对其可能取的每个值a，根据样本点A=a的测试为“是”或“否”将D分割为D1和D2两部分，利用上式Gini(D,A)来计算A=a时的基尼指数。
#Step2：在所有可能的特征A以及他们所有可能的切分点a中，选择基尼指数最小的特征及其对应可能的切分点作为最有特征与最优切分点。依最优特征与最有切分点，从现结点生成两个子节点，将训练数据集依特征分配到两个子节点中去。
#Step3：对两个子结点递归地调用Step1、Step2，直至满足条件。
#Step4：生成CART决策树
#算法停止计算的条件是节点中的样本个数小于预定阈值，或样本集的基尼指数小于预定阈值，或者没有更多特征。
#
#cart.py：

# -*- coding: utf-8 -*-
import numpy as np


class Tree(object):
    def __init__(self, value=None, true_branch=None, false_branch=None, results=None, col=-1, summary=None, data=None):
        self.value = value
        self.true_branch = true_branch
        self.false_branch = false_branch
        self.results = results
        self.col = col
        self.summary = summary
        self.data = data

    def __str__(self):
        print(self.col, self.value)
        print(self.results)
        print(self.summary)
        return ""


def split_datas(rows, value, column):
    """
    根据条件分离数据集
    :param rows:
    :param value:
    :param column:
    :return:  (list1, list2)
    """
    list1 = []
    list2 = []
    if isinstance(value, int) or isinstance(value, float):
        for row in rows:
            if row[column] >= value:
                list1.append(row)
            else:
                list2.append(row)
    else:
        for row in rows:
            if row[column] == value:
                list1.append(row)
            else:
                list2.append(row)

    return list1, list2


def calculate_diff_count(data_set):
    """
    分类统计data_set中每个类别的数量
    :param datas:如：[[5.1, 3.5, 1.4, 0.2, 'setosa'], [4.9, 3, 1.4, 0.2, 'setosa'],....]
    :return: 如：{'setosa': 50, 'versicolor': 50, 'virginica': 50}
    """
    results = {}
    for data in data_set:
        # 数据的最后一列data[-1]是类别
        if data[-1] not in results:
            results.setdefault(data[-1], 1)
        else:
            results[data[-1]] += 1
    return results


def gini(data_set):
    """
    计算gini的值，即Gini(p)
    :param data_set: 如：[[5.1, 3.5, 1.4, 0.2, 'setosa'], [4.9, 3, 1.4, 0.2, 'setosa'],....]
    :return:
    """
    length = len(data_set)
    category_2_cnt = calculate_diff_count(data_set)
    sum = 0.0
    for category in category_2_cnt:
        sum += pow(float(category_2_cnt[category]) / length, 2)
    return 1 - sum


def build_decision_tree(data_set, evaluation_function=gini):
    """
    递归建立决策树，当gain=0时，停止回归
    :param data_set: 如：[[5.1, 3.5, 1.4, 0.2, 'setosa'], [4.9, 3, 1.4, 0.2, 'setosa'],....]
    :param evaluation_function:
    :return:
    """
    current_gain = evaluation_function(data_set)
    column_length = len(data_set[0])
    rows_length = len(data_set)

    best_gain = 0.0
    best_value = None
    best_set = None

    # choose the best gain
    for feature_idx in range(column_length - 1):
        feature_value_set = set(row[feature_idx] for row in data_set)
        for feature_value in feature_value_set:
            sub_data_set1, sub_data_set2 = split_datas(data_set, feature_value, feature_idx)
            p = float(len(sub_data_set1)) / rows_length
            # Gini(D,A)表示在特征A的条件下集合D的基尼指数，gini_d_a越小，样本集合不确定性越小
            # 我们的目的是找到另gini_d_a最小的特征，及gain最大的特征
            gini_d_a = p * evaluation_function(sub_data_set1) + (1 - p) * evaluation_function(sub_data_set2)
            gain = current_gain - gini_d_a
            if gain > best_gain:
                best_gain = gain
                best_value = (feature_idx, feature_value)
                best_set = (sub_data_set1, sub_data_set2)
    dc_y = {'impurity': '%.3f' % current_gain, 'sample': '%d' % rows_length}

    # stop or not stop
    if best_gain > 0:
        true_branch = build_decision_tree(best_set[0], evaluation_function)
        false_branch = build_decision_tree(best_set[1], evaluation_function)
        return Tree(col=best_value[0], value=best_value[1], true_branch=true_branch, false_branch=false_branch, summary=dc_y)
    else:
        return Tree(results=calculate_diff_count(data_set), summary=dc_y, data=data_set)


def prune(tree, mini_gain, evaluation_function=gini):
    """
    裁剪
    :param tree:
    :param mini_gain:
    :param evaluation_function:
    :return:
    """
    if tree.true_branch.results == None:
        prune(tree.true_branch, mini_gain, evaluation_function)
    if tree.false_branch.results == None:
        prune(tree.false_branch, mini_gain, evaluation_function)

    if tree.true_branch.results != None and tree.false_branch.results != None:
        len1 = len(tree.true_branch.data)
        len2 = len(tree.false_branch.data)
        len3 = len(tree.true_branch.data + tree.false_branch.data)

        p = float(len1) / (len1 + len2)

        gain = evaluation_function(tree.true_branch.data + tree.false_branch.data) \
               - p * evaluation_function(tree.true_branch.data)\
               - (1 - p) * evaluation_function(tree.false_branch.data)

        if gain < mini_gain:
            # 当节点的gain小于给定的 mini Gain时则合并这两个节点
            tree.data = tree.true_branch.data + tree.false_branch.data
            tree.results = calculate_diff_count(tree.data)
            tree.true_branch = None
            tree.false_branch = None


def classify(data, tree):
    """
    分类
    :param data:
    :param tree:
    :return:
    """
    if tree.results != None:
        return tree.results
    else:
        branch = None
        v = data[tree.col]
        if isinstance(v, int) or isinstance(v, float):
            if v >= tree.value:
                branch = tree.true_branch
            else:
                branch = tree.false_branch
        else:
            if v == tree.value:
                branch = tree.true_branch
            else:
                branch = tree.false_branch
        return classify(data, branch)


def load_csv():
    def convert_types(s):
        s = s.strip()
        try:
            return float(s) if '.' in s else int(s)
        except ValueError:
            return s
    data = np.loadtxt("datas.csv", dtype="str", delimiter=",")
    data = data[1:, :]
    data_set = ([[convert_types(item) for item in row] for row in data])
    return data_set


if __name__ == '__main__':
    data_set = load_csv()
    print data_set
    decistion_tree = build_decision_tree(data_set, evaluation_function=gini)
    print decistion_tree.results
    # prune(decistion_tree, 0.4)
    print classify([5.1,3.5,1.4,0.2], decistion_tree) # setosa
    print classify([6.8,2.8,4.8,1.4], decistion_tree) # versicolor
    print classify([6.8,3.2,5.9,2.3], decistion_tree) # virginica