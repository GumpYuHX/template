#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:Yu
@file:template.py
@time:2022/06/21
"""


import numpy as np
import random


def move(res_label,pos):
    #需要移动的类别,移动的距离
    #移动的位置一定是小于链表总长的
    lenth = len(res_label)
    temp = res_label.copy()#深拷贝
    if(pos>=lenth):
        print("移动位数大于传入链表长度")
        return
    else:
        for i in range(lenth-1,pos-1,-1):
            temp[i] = temp[i-pos]


    return temp

def add_zero(res_label,pos):
    #在pos位前面添加0
    temp = res_label.copy()#深拷贝
    for i in range(pos):
        temp[i] = 0

    return temp



def combine(res_label1,res_label2,num_point):
    #两个类别 和需要移动的点数
    lenth = len(res_label1)

    template = []

    for i in range(lenth):
        for j in range(lenth):
            for k in range(num_point):
                temp = move(res_label2[j],k)
                temp= add_zero(temp,k)
                res = res_label1[i] + temp #每个点位叠加
                template.append(res)

    return template





def make_template(res_label1,res_label2,res_label3):
    template = []

    #注意叠加的顺序，例如combine(res_label1,res_label2) 和combine(res_label2,res_label1)是两种完全不同的叠加方式
    template1 = combine(res_label1,res_label2,25)
    template2 = combine(res_label1,res_label3,25)
    template3 = combine(res_label2, res_label3,25)

    template.append(template1)
    template.append(template2)
    template.append(template3)


    return template

def make_template_part1(label,len_label,num):
    res = []
    start = 0 #记录点初始位置
    pick = int(len_label/num) #选取多少个尖峰来制作num个模板,并向下取整
    random.shuffle(label)#随机打乱列表中的顺序


    for i in range(num):
        all = np.zeros(len(label[0]))#创建一个和尖峰长度一样的0数组
        for j in range(pick):
            temp = np.array(label[start+j])
            all = all+temp
        k = j+1
        start = start+k
        avg = all/len_label
        res.append(avg)


    return res

# def save(template):
#     #第一个文件：一个数组，对应一个标签的形式（字典）
#     data_one_to_one_0 = dict(one = template[0],label = [0 for i in range(len(template[0]))])
#     data_one_to_one_1 = dict(two = template[1],label = [1 for i in range(len(template[1]))])
#     data_one_to_one_2 = dict(three = template[2],label = [2 for i in range(len(template[2]))])
#
#
#     np.savez('one_to_one_data.npz', data_one_to_one_0=data_one_to_one_0, data_one_to_one_1=data_one_to_one_1, data_one_to_one_2=data_one_to_one_2)
#
#     #第二类文件：两个数组，一个数组为所以数据，另一个数组为所有书记标签
#
#     all_data = template[0][:]
#     all_data.extend(template[1])
#     all_data.extend(template[2])
#
#
#     #标签制作为4,5,6
#     label_cluster0 = [4 for i in range(len(template[0]))]
#     label_cluster1 = [5 for i in range(len(template[1]))]
#     label_cluster2 = [6 for i in range(len(template[2]))]
#
#     all_label = label_cluster0[:]
#     all_label.extend(label_cluster1)
#     all_label.extend(label_cluster2)
#
#
#
#
#
#     np.savez('all_data_and_all_label.npz', all_data=all_data,all_label=all_label)











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
#     # 将不是重叠的尖峰分类
#     for i in range(len(isnot_overlap)):
#         if (isnot_overlap_class[i] == 1):
#             label1.append(isnot_overlap[i])
#         elif (isnot_overlap_class[i] == 2):
#             label2.append(isnot_overlap[i])
#         else:
#             label3.append(isnot_overlap[i])
#
#
#
#     #三个类别的各自的数量
#     len_label1 = len(label1)
#     len_label2 = len(label2)
#     len_label3 = len(label3)
#
#
#     #制作出平均波形
#     res_label1 = make_template_part1(label1,len_label1,5)
#     res_label2 = make_template_part1(label2, len_label2, 5)
#     res_label3 = make_template_part1(label3, len_label3, 5)
#
#
#
#     #制作模板
#     template = make_template(res_label1,res_label2,res_label3) # 3类每类625个
#
#
#
#
#     save(template)



















