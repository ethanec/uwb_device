from socket import timeout
import time
import serial

import rospy
from uwb.msg import tag_distance

import csv

import signal
import sys 


def initialize():
    T0 = open('/home/meclab/catkin_ws/src/uwb/uwb_calibrationdata/data/20220224/T0_150cm.csv', 'w')
    T0_writer = csv.writer(T0)

    T1 = open('/home/meclab/catkin_ws/src/uwb/uwb_calibrationdata/data/20220224/T1_150cm.csv', 'w')
    T1_writer = csv.writer(T1)
    writer_list = [T0_writer, T1_writer]

    for i in range(len(writer_list)):
        row = ["A0", "A1", "A2", "A3"]
        writer_list[i].writerow(row)

    return writer_list

def write_csv(writer, num, row_number):
    row = [num.first, num.second, num.third, num.fourth]
    writer.writerow(row)
    print(row_number, row)
    
def tag_number(td, data):
    
    td.first = 0.
    td.second = 0.
    td.third = 0.
    td.fourth = 0.
    
    if(data[0] == "mc"):
        tag_used = int(data[1], 16)
        if(tag_used >= 1):
            td.first = int(data[2], 16) / 1000.
        if(tag_used >= 2):
            td.second = int(data[3], 16) / 1000.
        if(tag_used >= 4):
            td.third = int(data[4], 16) / 1000.
        if(tag_used >= 10):
            td.fourth = int(data[5], 16) / 1000.
        return True
    else:
        return False

def publish_uwb():
    pub = rospy.Publisher('uxb_publisher', tag_distance, queue_size=10)
    rospy.init_node("uwb_distance", anonymous=True)
    rate = rospy.Rate(10)
    ser = serial.Serial("/dev/ttyUSB1",115200)

    writer_list = initialize()
    row_T0 = 1
    row_T1 = 1
    
    while not rospy.is_shutdown():
        try:
            data = ser.readline()
            data = data.split(" ")
            td = tag_distance()
            # print(data)
            connection = tag_number(td, data)

            if connection:
                if str(data[9])[1] == '0':
                    write_csv(writer_list[0], td, row_T0)
                    row_T0 += 1
                elif str(data[9])[1] == '1':
                    write_csv(writer_list[1], td, row_T1)
                    row_T1 += 1

                print("tag id : " + str(data[9])[1])
                print("first base distance(m): " + str(td.first))
                print("second base distance(m): " + str(td.second))
                print("third base distance(m): " + str(td.third))
                print("fourth base distance(m): " + str(td.fourth))
                print("-----------------------------")
            else:
                print(data)
                print("****Connection Failed****")
                print("-----------------------------")
            pub.publish(td)
            rate.sleep()

        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            break

    ser.close()
    print("save the file")
    

if __name__ == '__main__':
    publish_uwb()
