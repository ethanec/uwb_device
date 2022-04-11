from socket import timeout
import time
import serial

import rospy
from uwb.msg import tag_distance

import xlsxwriter

import signal
import sys 

# offsets(m)
first_tag_offset = 0
second_tag_offset = 0
third_tag_offset = 0
fourth_tag_offset = 0


def initialize():
    T0_workbook = xlsxwriter.Workbook('/home/meclab/catkin_ws/src/uwb/uwb_calibrationdata/data/20220224/T0_150cm.xlsx')
    T1_workbook = xlsxwriter.Workbook('/home/meclab/catkin_ws/src/uwb/uwb_calibrationdata/data/20220224/T1_150cm.xlsx')
    workbook_list = [T0_workbook, T1_workbook]

    T0_worksheet = T0_workbook.add_worksheet()
    T1_worksheet = T1_workbook.add_worksheet()
    worksheet_list = [T0_worksheet, T1_worksheet]

    for i in range(len(worksheet_list)):
        worksheet_list[i].write('A1', 'A0')
        worksheet_list[i].write('B1', 'A1')
        worksheet_list[i].write('C1', 'A2')
        worksheet_list[i].write('D1', 'A3')

    return worksheet_list, workbook_list

def write_excel(worksheet, row, num):
    worksheet.write(row, 0, num.first)
    worksheet.write(row, 1, num.second)
    worksheet.write(row, 2, num.third)
    worksheet.write(row, 3, num.fourth)
    print(row, num.first, num.second, num.third, num.fourth)

def tag_number(td, data):
    
    td.first = 0.
    td.second = 0.
    td.third = 0.
    td.fourth = 0.
    
    if(data[0] == "mc"):
        tag_used = int(data[1], 16)
        if(tag_used >= 1):
            td.first = int(data[2], 16) / 1000. - first_tag_offset
        if(tag_used >= 2):
            td.second = int(data[3], 16) / 1000. - second_tag_offset
        if(tag_used >= 4):
            td.third = int(data[4], 16) / 1000. - third_tag_offset
        if(tag_used >= 10):
            td.fourth = int(data[5], 16) / 1000. - fourth_tag_offset
        return True
    else:
        return False

def publish_uwb():
    pub = rospy.Publisher('uxb_publisher', tag_distance, queue_size=10)
    rospy.init_node("uwb_distance", anonymous=True)
    rate = rospy.Rate(10)
    ser = serial.Serial("/dev/ttyUSB0",115200)

    [worksheet_list, workbook_list] = initialize()
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
                    write_excel(worksheet_list[0], row_T0, td)
                    row_T0 += 1
                elif str(data[9])[1] == '1':
                    write_excel(worksheet_list[1], row_T1, td)
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

    for i in workbook_list:
        i.close()
    ser.close()
    print("save the file")
    

if __name__ == '__main__':
    publish_uwb()
