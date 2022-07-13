#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:Yu
@file:is_overlap_and_less_25.py
@time:2022/06/26
"""
import scipy.io as scio
import numpy as np
import matplotlib.pyplot as plt

def Judg_category(is_distance_less_25_class_label1,is_distance_less_25_class_label2):
    '''

    :param is_distance_less_25_class_label1:
    :param is_distance_less_25_class_label2:
    :return: int类别数
    '''
    if(is_distance_less_25_class_label1*is_distance_less_25_class_label2 == 2 ):
        return 4
    elif(is_distance_less_25_class_label1*is_distance_less_25_class_label2 == 3):
        return 5
    elif (is_distance_less_25_class_label1 * is_distance_less_25_class_label2 == 6):
        return 6
    else:
        #-1是出现不应期的情况
        return -1



def findClass(is_distance_less_25,is_distance_less_25_distance,is_distance_less_25_class):
    '''
    :param is_distance_less_25: 尖峰，二维数组
    :param is_distance_less_25_distance: 尖峰间距离，一维数组
    :param is_distance_less_25_class: 重叠尖峰类别数组，一维数组
    :return: 返回三个结果数组，label_spike, label_class, label_distance
    '''
    lenth = len(is_distance_less_25_distance)

    #打标签，为了和之后的模板进行比较，注意打标签的顺序要和模板顺序一致
    label_spike = []
    label_class = []
    label_distance = []

    for i in range(0,lenth-1,2):
        j = i+1
        temp = []
        if(is_distance_less_25_distance[i]==is_distance_less_25_distance[j]):
            temp.append(is_distance_less_25[i])
            temp.append(is_distance_less_25[j])
            label_spike.append(temp)
            label = Judg_category(is_distance_less_25_class[i],is_distance_less_25_class[j])
            #print("第一个标签为：{},第二个标签为：{},综合标签为：{}\n".format(is_distance_less_25_class[i], is_distance_less_25_class[j],label))
            label_class.append(label)
            label_distance.append(is_distance_less_25_distance[i])

    return label_spike,label_class,label_distance









# if __name__ == '__main__':
#
#     datapath_class = "D:/ANN_SNN/data/Simulator/C_Difficult1_noise01/class.mat"
#     datapath_distance = "D:/ANN_SNN/data/Simulator/C_Difficult1_noise01/distance.mat"
#     datapath_spikes = "D:/ANN_SNN/data/Simulator/C_Difficult1_noise01/spikes.mat"
#     datapath_isOverlap_label = "D:/ANN_SNN/data/Simulator/C_Difficult1_noise01/is_overlap.mat"
#
#
#     file_spikes = scio.loadmat(datapath_spikes)
#     file_class = scio.loadmat(datapath_class)
#     flie_distance =scio.loadmat(datapath_distance)
#     flie_isOverlap_label = scio.loadmat(datapath_isOverlap_label)
#
#     spikes = file_spikes['spikes']
#     spike_class = file_class['class']
#     overlap_spikes_distance = flie_distance['distance']
#     isOverlap_label = flie_isOverlap_label['is_overlap']
#
#     is_overlap = [] #是重叠尖峰
#     isnot_overlap = [] #不是重叠尖峰
#
#     is_overlap_class = [] #是重叠尖峰类别
#     isnot_overlap_class = [] #不是重叠尖峰类别
#     distance = []#重叠峰值距离
#
#     is_distance_less_25 = []#重叠峰值小于25的尖峰
#     is_distance_less_25_class = []  #重叠峰值小于25的类别
#     is_distance_less_25_distance = [] #重叠峰值小于25的距离
#     label1 = []
#     label2 = []
#     label3 = []
#
#     for i in range(len(spike_class[0])):
#         if(isOverlap_label[0][i]>0):
#             is_overlap.append(spikes[i])
#             is_overlap_class.append(spike_class[0][i])
#             distance.append(overlap_spikes_distance[0][i])
#         else:
#             isnot_overlap.append(spikes[i])
#             isnot_overlap_class.append(spike_class[0][i])
#
#
#     #判断distance小于25
#     for i in range(len(distance)):
#         if(distance[i]<25):
#             is_distance_less_25.append(is_overlap[i])
#             is_distance_less_25_class.append(is_overlap_class[i])
#             is_distance_less_25_distance.append(distance[i])
#
#
#
#
#     label_spike, label_class, label_distance = findClass(is_distance_less_25,is_distance_less_25_distance,is_distance_less_25_class)
#
#     label_spike_new = []
#     label_class_new = []
#     #重新打包便于训练
#     for i in range(len(label_spike)):
#         if(label_class[i]!= -1):
#             label_spike_new.append(label_spike[i][0])
#             label_class_new.append(label_class[i])
#             label_spike_new.append(label_spike[i][1])
#             label_class_new.append(label_class[i])
#
#
#
#
#
#
#     np.savez('is_overlap_less_25.npz', label_spike=label_spike_new, label_class=label_class_new, label_distance=label_distance)


