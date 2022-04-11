#! /usr/bin/env python
import csv
import pandas as pd
import os

def write_csv(writer, num):
    row = [num[0], num[1], num[2], num[3]]
    writer.writerow(row)


def value_validation(df, writer): ## Check if value == 0
    for i in range(df.shape[0]):
        if df.iloc[i][0] <= 0 or df.iloc[i][1] <= 0 or df.iloc[i][2] <= 0 or df.iloc[i][3] <= 0:
            continue
        else:
            write_csv(writer, df.iloc[i])



filename = os.listdir("/home/meclab/catkin_ws/src/uwb/uwb_calibrationdata/data/20220315/raw/")

for i in range(len(filename)):
    print(filename[i])
    df = pd.read_csv("/home/meclab/catkin_ws/src/uwb/uwb_calibrationdata/data/20220315/raw/" + filename[i])
    f =  open('/home/meclab/catkin_ws/src/uwb/uwb_calibrationdata/data/20220315/preprocessed/' + filename[i], 'w')
    writer = csv.writer(f)
    row = ["A0", "A1", "A2", "A3"]
    writer.writerow(row)
    value_validation(df, writer)


    
