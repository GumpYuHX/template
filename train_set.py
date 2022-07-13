#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:Yu
@file:train_set.py
'''
制作模板创造训练集
'''
@time:2022/07/11
"""
from is_overlap_and_less_25 import *
from template import *

def create_train_set():
    datapath_class = "D:/ANN_SNN/data/Simulator/C_Difficult1_noise01/class.mat"
    datapath_distance = "D:/ANN_SNN/data/Simulator/C_Difficult1_noise01/distance.mat"
    datapath_spikes = "D:/ANN_SNN/data/Simulator/C_Difficult1_noise01/spikes.mat"
    datapath_isOverlap_label = "D:/ANN_SNN/data/Simulator/C_Difficult1_noise01/is_overlap.mat"

    file_spikes = scio.loadmat(datapath_spikes)
    file_class = scio.loadmat(datapath_class)
    flie_distance = scio.loadmat(datapath_distance)
    flie_isOverlap_label = scio.loadmat(datapath_isOverlap_label)

    spikes = file_spikes['spikes']
    spike_class = file_class['class']
    overlap_spikes_distance = flie_distance['distance']
    isOverlap_label = flie_isOverlap_label['is_overlap']

    is_overlap = []  # 是重叠尖峰
    isnot_overlap = []  # 不是重叠尖峰

    is_overlap_class = []  # 是重叠尖峰类别
    isnot_overlap_class = []  # 不是重叠尖峰类别
    distance = []  # 重叠峰值距离

    is_distance_less_25 = []  # 重叠峰值小于25的尖峰
    is_distance_less_25_class = []  # 重叠峰值小于25的类别
    is_distance_less_25_distance = []  # 重叠峰值小于25的距离
    label1 = []
    label2 = []
    label3 = []

#第一步制作模板
    for i in range(len(spike_class[0])):
        if(isOverlap_label[0][i]>0):
            is_overlap.append(spikes[i])
            is_overlap_class.append(spike_class[0][i])
            distance.append(overlap_spikes_distance[0][i])
        else:
            isnot_overlap.append(spikes[i])
            isnot_overlap_class.append(spike_class[0][i])


    # 将不是重叠的尖峰分类
    for i in range(len(isnot_overlap)):
        if (isnot_overlap_class[i] == 1):
            label1.append(isnot_overlap[i])
        elif (isnot_overlap_class[i] == 2):
            label2.append(isnot_overlap[i])
        else:
            label3.append(isnot_overlap[i])



    #三个类别的各自的数量
    len_label1 = len(label1)
    len_label2 = len(label2)
    len_label3 = len(label3)


    #制作出平均波形
    res_label1 = make_template_part1(label1,len_label1,5)
    res_label2 = make_template_part1(label2, len_label2, 5)
    res_label3 = make_template_part1(label3, len_label3, 5)



    #制作模板
    template = make_template(res_label1,res_label2,res_label3)

    #第一种标签方式：一个数组，对应一个标签的形式（字典）
    data_one_to_one_0 = dict(one = template[0],label = [0 for i in range(len(template[0]))])
    data_one_to_one_1 = dict(two = template[1],label = [1 for i in range(len(template[1]))])
    data_one_to_one_2 = dict(three = template[2],label = [2 for i in range(len(template[2]))])

    # 第二种标签方式：两个数组，一个数组为所以数据，另一个数组为所有书记标签

    all_template = template[0][:]
    all_template.extend(template[1])
    all_template.extend(template[2])

    # 标签制作为4,5,6
    label_cluster0 = [4 for i in range(len(template[0]))]
    label_cluster1 = [5 for i in range(len(template[1]))]
    label_cluster2 = [6 for i in range(len(template[2]))]

    all_label = label_cluster0[:]
    all_label.extend(label_cluster1)
    all_label.extend(label_cluster2)



#第二步：根据重叠点数小于24个点的重叠的数据保存为数据+标签的格式，根据标签制作重叠峰值的标签（重叠峰值标签为：4,5,6）
    for i in range(len(spike_class[0])):
        if (isOverlap_label[0][i] > 0):
            is_overlap.append(spikes[i])
            is_overlap_class.append(spike_class[0][i])
            distance.append(overlap_spikes_distance[0][i])
        else:
            isnot_overlap.append(spikes[i])
            isnot_overlap_class.append(spike_class[0][i])

    # 判断distance小于25
    for i in range(len(distance)):
        if (distance[i] < 25):
            is_distance_less_25.append(is_overlap[i])
            is_distance_less_25_class.append(is_overlap_class[i])
            is_distance_less_25_distance.append(distance[i])

    label_spike, label_class, label_distance = findClass(is_distance_less_25, is_distance_less_25_distance,
                                                         is_distance_less_25_class)

    label_spike_new = []
    label_class_new = []
    # 重新打包便于训练
    for i in range(len(label_spike)):
        # 排除不应期的情况
        if (label_class[i] != -1):
            label_spike_new.append(label_spike[i][0])
            label_class_new.append(label_class[i])
            label_spike_new.append(label_spike[i][1])
            label_class_new.append(label_class[i])


#第三步：制作训练集+测试集：

    num_template = len(all_template)#模板数量
    train_spike_set = all_template[:]
    train_class_set = all_label[:]
    num_save_spike = num_template+150#大约保存模板数量多150个的尖峰
    for i in range(num_save_spike):
        train_spike_set.append(isnot_overlap[i])
        train_class_set.append(isnot_overlap_class[i])

#第四步：制作验证集：
    verify_spike_set = label_spike_new[:]
    verify_class_set = label_class_new[:]
    for i in range(num_save_spike+1,len(isnot_overlap)):
        verify_spike_set.append(isnot_overlap[i])
        verify_class_set.append(isnot_overlap_class[i])
#第五步：保存

    np.savez('train_set.npz', train_spike_set=train_spike_set,train_class_set=train_class_set)
    np.savez('verify_set.npz', verify_spike_set=verify_spike_set, verify_class_set=verify_class_set)





if __name__ == '__main__':
    create_train_set()
