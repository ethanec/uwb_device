#! /usr/bin/env python
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

def cal_bias_std(df, filename):
    mean = df.mean(axis = 0)
    try:
        true_range = float(filename[3:7])/100
    except ValueError:
        try:
            true_range = float(filename[3:6])/100
        except ValueError:
            print(filename)
            true_range = float(filename[3:5])/100
    bias = mean - true_range
    std = df.std(axis = 0)

    print(filename + ": ")
    print("True range: "+ str(true_range))
    print("")
    print("Bias")
    print(bias)
    print("")
    print("STD")
    print(std)
    return filename[0:2], true_range, mean, bias, std

def print_bias(bias_t0, bias_t1, mean_t0, mean_t1):
    print("Measured Range | " + str(mean_t0[0][0]) + ", " + str(mean_t0[0][1]) + ", " + str(mean_t0[0][2]) + ", " + str(mean_t0[0][3]) + ", " + str(mean_t0[0][4]) + ", " + str(mean_t0[0][5]) + ", " + str(mean_t0[0][6]) + ", " + str(mean_t0[0][7]) + ", " + str(mean_t0[0][8]) + ", " + str(mean_t0[0][9]) + ", " + str(mean_t0[0][10]) + ", " + str(mean_t0[0][11]) + ", " + str(mean_t0[0][12]) + ", " + str(mean_t0[0][13]) + ", " + str(mean_t0[0][14]))
    print("T0_A0 Bias     | " + str(bias_t0[0][0]) + ", " + str(bias_t0[0][1]) + ", " + str(bias_t0[0][2]) + ", " + str(bias_t0[0][3]) + ", " + str(bias_t0[0][4]) + ", " + str(bias_t0[0][5]) + ", " + str(bias_t0[0][6]) + ", " + str(bias_t0[0][7]) + ", " + str(bias_t0[0][8]) + ", " + str(bias_t0[0][9]) + ", " + str(bias_t0[0][10]) + ", " + str(bias_t0[0][11]) + ", " + str(bias_t0[0][12]) + ", " + str(bias_t0[0][13]) + ", " + str(bias_t0[0][14]))
    print("------------------------------------------")
    print("Measured Range | " + str(mean_t0[1][0]) + ", " + str(mean_t0[1][1]) + ", " + str(mean_t0[1][2]) + ", " + str(mean_t0[1][3]) + ", " + str(mean_t0[1][4]) + ", " + str(mean_t0[1][5]) + ", " + str(mean_t0[1][6]) + ", " + str(mean_t0[1][7]) + ", " + str(mean_t0[1][8]) + ", " + str(mean_t0[1][9]) + ", " + str(mean_t0[1][10]) + ", " + str(mean_t0[1][11]) + ", " + str(mean_t0[1][12]) + ", " + str(mean_t0[1][13]) + ", " + str(mean_t0[1][14]))
    print("T0_A1 Bias     | " + str(bias_t0[1][0]) + ", " + str(bias_t0[1][1]) + ", " + str(bias_t0[1][2]) + ", " + str(bias_t0[1][3]) + ", " + str(bias_t0[1][4]) + ", " + str(bias_t0[1][5]) + ", " + str(bias_t0[1][6]) + ", " + str(bias_t0[1][7]) + ", " + str(bias_t0[1][8]) + ", " + str(bias_t0[1][9]) + ", " + str(bias_t0[1][10]) + ", " + str(bias_t0[1][11]) + ", " + str(bias_t0[1][12]) + ", " + str(bias_t0[1][13]) + ", " + str(bias_t0[1][14]))
    print("------------------------------------------")
    print("Measured Range | " + str(mean_t0[2][0]) + ", " + str(mean_t0[2][1]) + ", " + str(mean_t0[2][2]) + ", " + str(mean_t0[2][3]) + ", " + str(mean_t0[2][4]) + ", " + str(mean_t0[2][5]) + ", " + str(mean_t0[2][6]) + ", " + str(mean_t0[2][7]) + ", " + str(mean_t0[2][8]) + ", " + str(mean_t0[2][9]) + ", " + str(mean_t0[2][10]) + ", " + str(mean_t0[2][11]) + ", " + str(mean_t0[2][12]) + ", " + str(mean_t0[2][13]) + ", " + str(mean_t0[2][14]))
    print("T0_A2 Bias     | " + str(bias_t0[2][0]) + ", " + str(bias_t0[2][1]) + ", " + str(bias_t0[2][2]) + ", " + str(bias_t0[2][3]) + ", " + str(bias_t0[2][4]) + ", " + str(bias_t0[2][5]) + ", " + str(bias_t0[2][6]) + ", " + str(bias_t0[2][7]) + ", " + str(bias_t0[2][8]) + ", " + str(bias_t0[2][9]) + ", " + str(bias_t0[2][10]) + ", " + str(bias_t0[2][11]) + ", " + str(bias_t0[2][12]) + ", " + str(bias_t0[2][13]) + ", " + str(bias_t0[2][14]))
    print("------------------------------------------")
    print("Measured Range | " + str(mean_t0[3][0]) + ", " + str(mean_t0[3][1]) + ", " + str(mean_t0[3][2]) + ", " + str(mean_t0[3][3]) + ", " + str(mean_t0[3][4]) + ", " + str(mean_t0[3][5]) + ", " + str(mean_t0[3][6]) + ", " + str(mean_t0[3][7]) + ", " + str(mean_t0[3][8]) + ", " + str(mean_t0[3][9]) + ", " + str(mean_t0[3][10]) + ", " + str(mean_t0[3][11]) + ", " + str(mean_t0[3][12]) + ", " + str(mean_t0[3][13]) + ", " + str(mean_t0[3][14]))
    print("T0_A3 Bias     | " + str(bias_t0[3][0]) + ", " + str(bias_t0[3][1]) + ", " + str(bias_t0[3][2]) + ", " + str(bias_t0[3][3]) + ", " + str(bias_t0[3][4]) + ", " + str(bias_t0[3][5]) + ", " + str(bias_t0[3][6]) + ", " + str(bias_t0[3][7]) + ", " + str(bias_t0[3][8]) + ", " + str(bias_t0[3][9]) + ", " + str(bias_t0[3][10]) + ", " + str(bias_t0[3][11]) + ", " + str(bias_t0[3][12]) + ", " + str(bias_t0[3][13]) + ", " + str(bias_t0[3][14]))
    print(" ")
    print(" ")
    print("Measured Range | " + str(mean_t1[0][0]) + ", " + str(mean_t1[0][1]) + ", " + str(mean_t1[0][2]) + ", " + str(mean_t1[0][3]) + ", " + str(mean_t1[0][4]) + ", " + str(mean_t1[0][5]) + ", " + str(mean_t1[0][6]) + ", " + str(mean_t1[0][7]) + ", " + str(mean_t1[0][8]) + ", " + str(mean_t1[0][9]) + ", " + str(mean_t1[0][10]) + ", " + str(mean_t1[0][11]) + ", " + str(mean_t1[0][12]) + ", " + str(mean_t1[0][13]) + ", " + str(mean_t1[0][14]))
    print("T1_A0 Bias     | " + str(bias_t1[0][0]) + ", " + str(bias_t1[0][1]) + ", " + str(bias_t1[0][2]) + ", " + str(bias_t1[0][3]) + ", " + str(bias_t1[0][4]) + ", " + str(bias_t1[0][5]) + ", " + str(bias_t1[0][6]) + ", " + str(bias_t1[0][7]) + ", " + str(bias_t1[0][8]) + ", " + str(bias_t1[0][9]) + ", " + str(bias_t1[0][10]) + ", " + str(bias_t1[0][11]) + ", " + str(bias_t1[0][12]) + ", " + str(bias_t1[0][13]) + ", " + str(bias_t1[0][14]))
    print("------------------------------------------")
    print("Measured Range | " + str(mean_t1[1][0]) + ", " + str(mean_t1[1][1]) + ", " + str(mean_t1[1][2]) + ", " + str(mean_t1[1][3]) + ", " + str(mean_t1[1][4]) + ", " + str(mean_t1[1][5]) + ", " + str(mean_t1[1][6]) + ", " + str(mean_t1[1][7]) + ", " + str(mean_t1[1][8]) + ", " + str(mean_t1[1][9]) + ", " + str(mean_t1[1][10]) + ", " + str(mean_t1[1][11]) + ", " + str(mean_t1[1][12]) + ", " + str(mean_t1[1][13]) + ", " + str(mean_t1[1][14]))
    print("T1_A1 Bias     | " + str(bias_t1[1][0]) + ", " + str(bias_t1[1][1]) + ", " + str(bias_t1[1][2]) + ", " + str(bias_t1[1][3]) + ", " + str(bias_t1[1][4]) + ", " + str(bias_t1[1][5]) + ", " + str(bias_t1[1][6]) + ", " + str(bias_t1[1][7]) + ", " + str(bias_t1[1][8]) + ", " + str(bias_t1[1][9]) + ", " + str(bias_t1[1][10]) + ", " + str(bias_t1[1][11]) + ", " + str(bias_t1[1][12]) + ", " + str(bias_t1[1][13]) + ", " + str(bias_t1[1][14]))
    print("------------------------------------------")
    print("Measured Range | " + str(mean_t1[2][0]) + ", " + str(mean_t1[2][1]) + ", " + str(mean_t1[2][2]) + ", " + str(mean_t1[2][3]) + ", " + str(mean_t1[2][4]) + ", " + str(mean_t1[2][5]) + ", " + str(mean_t1[2][6]) + ", " + str(mean_t1[2][7]) + ", " + str(mean_t1[2][8]) + ", " + str(mean_t1[2][9]) + ", " + str(mean_t1[2][10]) + ", " + str(mean_t1[2][11]) + ", " + str(mean_t1[2][12]) + ", " + str(mean_t1[2][13]) + ", " + str(mean_t1[2][14]))
    print("T1_A2 Bias     | " + str(bias_t1[2][0]) + ", " + str(bias_t1[2][1]) + ", " + str(bias_t1[2][2]) + ", " + str(bias_t1[2][3]) + ", " + str(bias_t1[2][4]) + ", " + str(bias_t1[2][5]) + ", " + str(bias_t1[2][6]) + ", " + str(bias_t1[2][7]) + ", " + str(bias_t1[2][8]) + ", " + str(bias_t1[2][9]) + ", " + str(bias_t1[2][10]) + ", " + str(bias_t1[2][11]) + ", " + str(bias_t1[2][12]) + ", " + str(bias_t1[2][13]) + ", " + str(bias_t1[2][14]))
    print("------------------------------------------")
    print("Measured Range | " + str(mean_t1[3][0]) + ", " + str(mean_t1[3][1]) + ", " + str(mean_t1[3][2]) + ", " + str(mean_t1[3][3]) + ", " + str(mean_t1[3][4]) + ", " + str(mean_t1[3][5]) + ", " + str(mean_t1[3][6]) + ", " + str(mean_t1[3][7]) + ", " + str(mean_t1[3][8]) + ", " + str(mean_t1[3][9]) + ", " + str(mean_t1[3][10]) + ", " + str(mean_t1[3][11]) + ", " + str(mean_t1[3][12]) + ", " + str(mean_t1[3][13]) + ", " + str(mean_t1[3][14]))
    print("T1_A3 Bias     | " + str(bias_t1[3][0]) + ", " + str(bias_t1[3][1]) + ", " + str(bias_t1[3][2]) + ", " + str(bias_t1[3][3]) + ", " + str(bias_t1[3][4]) + ", " + str(bias_t1[3][5]) + ", " + str(bias_t1[3][6]) + ", " + str(bias_t1[3][7]) + ", " + str(bias_t1[3][8]) + ", " + str(bias_t1[3][9]) + ", " + str(bias_t1[3][10]) + ", " + str(bias_t1[3][11]) + ", " + str(bias_t1[3][12]) + ", " + str(bias_t1[3][13]) + ", " + str(bias_t1[3][14]))

history = []
test_range = ["3000", "2800", "2600", "2400", "2200", "2000", "1800", "1600", "1400", "1200", "1000", "800", "600", "400", "200"]
#########################################################################################################################################################################
for i in range(len(test_range)):
    df = pd.read_csv("/home/meclab/catkin_ws/src/uwb/uwb_calibrationdata/data/20220315/preprocessed/T0_" + test_range[i] + "cm.csv")
    (T0_filename, T0_true_range, T0_mean, T0_bias, T0_std) = cal_bias_std(df, "T0_" + test_range[i])
    print("--------------------------------")
    df = pd.read_csv("/home/meclab/catkin_ws/src/uwb/uwb_calibrationdata/data/20220315/preprocessed/T1_" + test_range[i] + "cm.csv")
    (T1_filename, T1_true_range, T1_mean, T1_bias, T1_std) = cal_bias_std(df, "T1_" + test_range[i])
    print("--------------------------------")
    history.append([T0_filename, T0_true_range, T0_mean, T0_bias, T0_std])
    history.append([T1_filename, T1_true_range, T1_mean, T1_bias, T1_std])

# print(history)
T0_true_range = []
T0_mean_range = [[], [], [], []]
T0_bias = [[], [], [], []]
T0_std = [[], [], [], []]

T1_true_range = []
T1_mean_range = [[], [], [], []]
T1_bias = [[], [], [], []]
T1_std = [[], [], [], []]

for i in history:
    if i[0] == 'T0':
        T0_true_range.append(i[1])
        T0_mean_range[0].append(i[2][0])
        T0_mean_range[1].append(i[2][1])
        T0_mean_range[2].append(i[2][2])
        T0_mean_range[3].append(i[2][3])
        T0_bias[0].append(i[3][0])
        T0_bias[1].append(i[3][1])
        T0_bias[2].append(i[3][2])
        T0_bias[3].append(i[3][3])
        T0_std[0].append(i[4][0])
        T0_std[1].append(i[4][1])
        T0_std[2].append(i[4][2])
        T0_std[3].append(i[4][3])
    elif i[0] == 'T1':
        T1_true_range.append(i[1])
        T1_mean_range[0].append(i[2][0])
        T1_mean_range[1].append(i[2][1])
        T1_mean_range[2].append(i[2][2])
        T1_mean_range[3].append(i[2][3])
        T1_bias[0].append(i[3][0])
        T1_bias[1].append(i[3][1])
        T1_bias[2].append(i[3][2])
        T1_bias[3].append(i[3][3])
        T1_std[0].append(i[4][0])
        T1_std[1].append(i[4][1])
        T1_std[2].append(i[4][2])
        T1_std[3].append(i[4][3])

print_bias(T0_bias, T1_bias, T0_mean_range, T1_mean_range)
# print(T1_std[0])

### bias
pic = plt.plot(T1_mean_range[0], T1_bias[0],':', label='T1_A0')
pic = plt.plot(T1_mean_range[1], T1_bias[1],':', label='T1_A1')
pic = plt.plot(T1_mean_range[2], T1_bias[2],':', label='T1_A2')
pic = plt.plot(T1_mean_range[3], T1_bias[3],':', label='T1_A3')
plt.title('T1_bias')
plt.legend(loc='upper left', shadow=False, fontsize='medium')
plt.show()

pic = plt.plot(T0_mean_range[0], T0_bias[0],':', label='T0_A0')
pic = plt.plot(T0_mean_range[1], T0_bias[1],':', label='T0_A1')
pic = plt.plot(T0_mean_range[2], T0_bias[2],':', label='T0_A2')
pic = plt.plot(T0_mean_range[3], T0_bias[3],':', label='T0_A3')
plt.title('T0_bias')
plt.legend(loc='upper left', shadow=False, fontsize='medium')
plt.show()

### std
pic = plt.plot(T1_true_range, T1_std[0],':', label='T1_A0')
pic = plt.plot(T1_true_range, T1_std[1],':', label='T1_A1')
pic = plt.plot(T1_true_range, T1_std[2],':', label='T1_A2')
pic = plt.plot(T1_true_range, T1_std[3],':', label='T1_A3')
plt.title('T1_std')
plt.legend(loc='upper left', shadow=False, fontsize='medium')
plt.show()

pic = plt.plot(T0_true_range, T0_std[0],':', label='T0_A0')
pic = plt.plot(T0_true_range, T0_std[1],':', label='T0_A1')
pic = plt.plot(T0_true_range, T0_std[2],':', label='T0_A2')
pic = plt.plot(T0_true_range, T0_std[3],':', label='T0_A3')
plt.title('T0_std')
plt.legend(loc='upper left', shadow=False, fontsize='medium')
plt.show()
