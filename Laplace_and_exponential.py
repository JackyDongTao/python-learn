# -*- coding: utf-8 -*-
"""以拉普拉斯机制和指数机制实现差分隐私"""

import numpy as np

#__author__ = 'Geneviève Gilbert'

def exponential_mechanism(data, utility_fct, R, epsilon, test=None):
    """
    按照指数机制来加入噪声数据
     data —— 数据库中的实际条目（从0到x）
     utility_fct —— 定义条目之间距离的矩阵
     R —— 可能的输入（0到x）列表服从在 utility_fct中的顺序
     epsilon - 隐私损失
     返回epsilon差分私人数据对应
    """
    prob = np.empty(utility_fct.shape)
    delta_u = sensitivity_exp(utility_fct)
    dp_data = np.zeros_like(data)
    # 定义概率 probabilities
    if len(utility_fct):
        row = utility_fct.shape[0]
        col = utility_fct.shape[1]
    else:
        raise ValueError('Unusefull utility function')
    for r in R:
        for c in R:
            prob[r][c] = np.exp(epsilon * utility_fct[r][c] * (1 / (2 * delta_u)))
    # 在行上标准化（row）
    for r in range(row):
        row_sum = np.sum(prob[r])
        prob[r] /= row_sum

    print('\nutility fct\n{}'.format(utility_fct))
    print('\nprobs\n{}'.format(prob))
    # 生成epsilon不同的私人替代品
    for idx, d in enumerate(data):
        np.random.seed(42)
        dp_data[idx,0] = np.random.choice(R, p=prob[int(d[0])])
    return dp_data

def laplace_mechanism(data, epsilon, min_=None, max_=None):
    """
    在拉普拉斯机制之后的数据增加了噪音
     data --数据库中包含真正条目的数组（从0到x）
     min_ -- 理论上的最小值，如果没有给出，则将取代观测值
     max_ -- 理论最大值，如果没有给出，观测值将被替换
     epsilon -- 隐私损失
     返回epsilon差分私人数据对应
    """
    sensitivity = sensitivity_laplace(data, min_, max_)
    if sensitivity <= 0:
        raise ValueError('You are not sensitive enough')
    noisy_data = data.copy()
    w, h = noisy_data.shape[1], noisy_data.shape[0]
    for col in range(w):
        column_serie = data[:, col]
        # case _without_ human 固定的边界
        if ((max_ == None) and (min_ == None)):
            column_max = np.max(column_serie)
            column_min = np.min(column_serie)
        # case _with_ 固定的边界
        elif len(min_) == len(max_):
            if len(min_) == w:
                column_max = max_[col]
                column_min = min_[col]
        else:
            raise ValueError('Innapropriate min_ max_')
        # 在边界之后添加噪音
        old_column = noisy_data[:, col]
        np.random.seed(42)
        noise = np.random.laplace(loc=0.0, scale=sensitivity/epsilon, size=h)
        new_column = old_column + noise
        new_column = np.clip(new_column, a_min=column_min, a_max=column_max)
        noisy_data[:, col] = new_column

    return noisy_data

def sensitivity_exp(utility_fct):
    """
    返回指数机制的给定fct的灵敏度
  utility_fct -- matrix其中rows = real_entries和columns = possibles_answers
    """
    if len(utility_fct):
        col = utility_fct.shape[1]
    else:
        raise ValueError('Unusefull utility function')
    maxs = []
    for c in range(col):
        column = utility_fct[:,c]
        column_max = column.max()
        column_min = column.min()
        maxs.append(column_max - column_min)
    return max(maxs)

def sensitivity_laplace(data, min_=None, max_=None):
    """
    返回拉普拉斯机制的给定数据的灵敏度
  data - 包含数据的numpy数组
    """
    if not data.size:
        raise ValueError('No data')
    rows = data.shape[0]
    columns = data.shape[1]
    sensitivity = 0
    # case _without_ human fixed boundaries
    if ((max_ == None) or (min_ == None)):
        for col in range(columns):
            local_sensitivity = np.max(data[:, col]) - np.min(data[:, col])
            if (not isinstance(local_sensitivity, str)):
                if (not np.isnan(local_sensitivity)):
                    sensitivity += local_sensitivity
    # case _with_ human fixed boundaries
    elif len(min_) == len(max_):
        if len(min_) == columns:
            sensitivity = np.sum(max_) - np.sum(min_)
        else:
            raise ValueError('min_ and max_ length not related to data')
    else:
        raise ValueError('Innapropriate min_ max_')
    print('\nSensitivity : {}'.format(sensitivity))

    return sensitivity
