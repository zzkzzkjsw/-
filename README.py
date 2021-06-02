# -python
color = ['#ff9408','#fef96e','#b6ffbb','#7bc8f8','#cea2fd']

import random
import numpy as np
import math
from time import time as glo_time
n,m=map(int,input().split())
time=[]
# get time[i][j] from input
# time[i][j] means time used for workpiece i and machine j
for i in range(n):
    ls=list(map(int,input().split()))
    ls1=[]
    for index,i in enumerate(ls):
        if(index%2==1):
            ls1.append(i)
    time.append(ls1)

time_start=glo_time()
# randomly initialize the order of workpiece being processed
order=list(range(n))
random.shuffle(order)

# calculate the time given the order
def cal_time(order):
    t=np.zeros((m,n),dtype=int)
    # t[i][j] means all the time that has been cost for piece order j and machine i
    t[0][0]=time[order[0]][0]
    #for machine 0, we initialize the time
    for index,j in enumerate(order):
        if index>0:
            t[0][index]=t[0][index-1]+time[j][0]

    #for machine 1...m-1, we update the t[i][j]
    for i in range(1,m):
        t[i][0]=t[i-1][0]+time[order[0]][i]
        for index,j in enumerate(order):
            if index>0:
                t1=t[i][index-1]+time[j][i]
                t2=t[i-1][index]+time[j][i]
                #  for machine i and workpiece j, it is determined by two things,
                #  one is last machine i-1 and workpiece j,
                #  the other is machine i and last workpiece j-1
                t[i][index]=max(t1,t2)

    return t

epochs=10000

#here we choose randomly swap 3 elements in order[]
#we have also chosen randomly swap 2 elements in order[], but this works worse than 3 elements
def get_next_order(order):
    x=random.randint(0,n-1)
    y=random.randint(0,n-1)
    z=random.randint(0,n-1)
    new_order=order.copy()
    temp=new_order[x]
    new_order[x]=new_order[y]
    new_order[y]=temp
    temp=new_order[x]
    new_order[x]=new_order[z]
    new_order[z]=temp
    return new_order


for epoch in range(epochs):
    next_order=get_next_order(order)
    delta_E=cal_time(order)[m-1][n-1]-cal_time(next_order)[m-1][n-1]

    if delta_E>0:
        # print("next is better than current")
        order=next_order
    else:
        # print("next is worse than current")
        # here,we choose T0=100, T=T0*0.95**epoch
        p=math.exp(delta_E*0.02*1.05**epoch)
        if random.random()<p:
            # print("but we still accept next with possibility p{:.2f}".format(p))
            order=next_order

res=cal_time(order)
print(res[m-1][n-1])
print(order)
time_end=glo_time()
print("{:.2f}s".format(time_end-time_start))


left=np.zeros((m,n),dtype=int)
add=np.zeros((m,n),dtype=int)
for i in range(m):
    for j in range(n):
        left[i][j]=res[i][j]-time[order[j]][i]
        add[i][j]=time[order[j]][i]
left=left.T.tolist()
add=add.T.tolist()
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
del m,n
m = range(len(add))
n = range(len(add[0]))
color = ['#ff9408','#fef96e','#b6ffbb','#7bc8f8','#cea2fd']
 
#画布设置，大小与分辨率
plt.figure(figsize=(20,8),dpi=80)
#barh-柱状图换向，循坏迭代-层叠效果
for i in m:
    for j in n:
        plt.barh(m[i]+1, add[i][j], left=left[i][j],color=color[j])
plt.title("流水加工甘特图")
labels =[''] *len(add[0])
for f in n:
    labels[f] = "工序%d"%(f+1)
#图例绘制
patches = [ mpatches.Patch(color=color[i], label="{:s}".format(labels[i]) ) for i in range(len(add[0])) ]
plt.legend(handles=patches,loc=4)
#XY轴标签
plt.xlabel("加工时间/s")
plt.ylabel("工件加工优先级")
#网格线，此图使用不好看，注释掉
#plt.grid(linestyle="--",alpha=0.5)
plt.show()


<!-- 11 5
0 375 1  12 2 142 3 245 4 412
0 632 1 452 2 758 3 278 4 398
0  12 1 876 2 124 3 534 4 765
0 460 1 542 2 523 3 120 4 499
0 528 1 101 2 789 3 124 4 999
0 796 1 245 2 632 3 375 4 123
0 532 1 230 2 543 3 896 4 452
0  14 1 124 2 214 3 543 4 785
0 257 1 527 2 753 3 210 4 463
0 896 1 896 2 214 3 258 4 259
0 532 1 302 2 501 3 765 4 988 -->
