#! /usr/bin/env python

import serial
import rospy
from uwb.msg import tag_distance
from std_msgs.msg import float32

T0_range = [[30.6450018484, 28.624953668, 26.6535843271, 24.6803529412, 22.6643444816, 20.631245, 18.6275224439, 16.6177760417, 14.6861462523, 12.659512381, 10.6106143791, 8.64467602996, 6.60003623188, 4.65925793651, 2.67090524194],
            [30.5942107209, 28.5760984556, 26.5987427598, 24.625973262, 22.610638796, 20.581645, 18.5721284289, 16.5647170139, 14.6455301645, 12.6076304762, 10.5726797386, 8.60158614232, 6.55592934783, 4.61434126984, 2.6620483871],
            [30.5605434381, 28.5508706564, 26.5740698467, 24.5922263815, 22.5869130435, 20.5507616667, 18.5556334165, 16.5723142361, 14.6224186472, 12.6164819048, 10.5634362745, 8.60564794007, 6.55372282609, 4.6295515873, 2.62921169355],
            [30.5308207024, 28.5102567568, 26.5360613288, 24.5513404635, 22.5843060201, 20.5464616667, 18.4927194514, 16.5110329861, 14.5977879342, 12.556632381, 10.5150147059, 8.55449438202, 6.52500362319, 4.57290674603, 2.62113104839]]
T0_bias = [[0.645001848429, 0.624953667954, 0.653584327087, 0.680352941176, 0.664344481605, 0.631245, 0.62752244389, 0.617776041667, 0.686146252285, 0.659512380952, 0.610614379085, 0.644676029963, 0.600036231884, 0.659257936508, 0.670905241935],
           [0.594210720887, 0.576098455598, 0.598742759796, 0.625973262032, 0.610638795987, 0.581645, 0.572128428928, 0.564717013889, 0.645530164534, 0.60763047619, 0.572679738562, 0.601586142322, 0.555929347826, 0.614341269841, 0.662048387097],
           [0.560543438078, 0.550870656371, 0.574069846678, 0.592226381462, 0.586913043478, 0.550761666667, 0.555633416459, 0.572314236111, 0.622418647166, 0.616481904762, 0.56343627451, 0.605647940075, 0.553722826087, 0.629551587302, 0.629211693548],
           [0.530820702403, 0.510256756757, 0.53606132879, 0.551340463458, 0.584306020067, 0.546461666667, 0.492719451372, 0.511032986111, 0.597787934187, 0.556632380952, 0.515014705882, 0.554494382022, 0.525003623188, 0.572906746032, 0.621131048387]]
T1_range = [[30.6426007326, 28.6308151751, 26.6093508475, 24.6558003565, 22.6542466667, 20.6557571189, 18.628256962, 16.6292191304, 14.6765594796, 12.6485047438, 10.6018943894, 8.62648613678, 6.605066787, 4.65008661417, 2.67373895582],
            [30.5739267399, 28.5668949416, 26.5337220339, 24.5981212121, 22.5834266667, 20.585201005, 18.5493037975, 16.5654852174, 14.6079107807, 12.5858785579, 10.5643960396, 8.59138077634, 6.54067689531, 4.60453543307, 2.63790361446],
            [30.5308663004, 28.5397412451, 26.5213016949, 24.5718698752, 22.56209, 20.5532462312, 18.5542949367, 16.5860573913, 14.6163122677, 12.6149525617, 10.5698910891, 8.59395563771, 6.53598555957, 4.59480708661, 2.62416064257],
            [30.5085238095, 28.5103774319, 26.4771305085, 24.5164278075, 22.554785, 20.5539748744, 18.4841189873, 16.5087565217, 14.5694144981, 12.5343529412, 10.5213382838, 8.53518853974, 6.4940234657, 4.54725393701, 2.60828313253]]
T1_bias = [[0.642600732601, 0.630815175097, 0.609350847458, 0.655800356506, 0.654246666667, 0.655757118928, 0.628256962025, 0.629219130435, 0.676559479554, 0.648504743833, 0.601894389439, 0.626486136784, 0.605066787004, 0.650086614173, 0.673738955823],
           [0.573926739927, 0.566894941634, 0.533722033898, 0.598121212121, 0.583426666667, 0.585201005025, 0.549303797468, 0.565485217391, 0.607910780669, 0.585878557875, 0.564396039604, 0.59138077634, 0.540676895307, 0.604535433071, 0.637903614458],
           [0.530866300366, 0.539741245136, 0.521301694915, 0.571869875223, 0.56209, 0.553246231156, 0.554294936709, 0.586057391304, 0.616312267658, 0.61495256167, 0.569891089109, 0.593955637708, 0.535985559567, 0.594807086614, 0.62416064257],
           [0.508523809524, 0.510377431907, 0.477130508475, 0.516427807487, 0.554785, 0.553974874372, 0.484118987342, 0.508756521739, 0.569414498141, 0.534352941176, 0.521338283828, 0.535188539741, 0.494023465704, 0.547253937008, 0.60828313253]]


def cal_bias(value, bias, range_ref, anchor_number): #interpolation
    if value == 0: ### miss signal 
        return 0
    n = len(range_ref[anchor_number])
    final_bias = 0

    for i in range(n): ### ranging value equals to ranging reference
        if value == range_ref[anchor_number][i]:
            final_bias = bias[anchor_number][i]
            return final_bias

    if value > range_ref[anchor_number][0]: ### ranging value bigger than the biggest ranging reference  
        slope = (bias[anchor_number][0] - bias[anchor_number][1])/(range_ref[anchor_number][0] - range_ref[anchor_number][1])
        final_bias = bias[anchor_number][0] - (slope * (value - range_ref[anchor_number][0]))
        # print("A" +str(anchor_number) + " bias = " + str(bias[anchor_number][0]) + " - (" + str(slope) + " * " + str(value) + ") = " + str(final_bias))
        return final_bias
    elif value < range_ref[anchor_number][n-1]: ### ranging value smaller than the smallest ranging reference  
        slope = (bias[anchor_number][n-2] - bias[anchor_number][n-1])/(range_ref[anchor_number][n-2] - range_ref[anchor_number][n-1])
        final_bias = bias[anchor_number][n-1] - (slope * (range_ref[anchor_number][n-1] - value))
        # print("A" +str(anchor_number) + " bias = " + str(bias[anchor_number][n-1]) + " - (" + str(slope) + " * " + str((range_ref[anchor_number][n-1] - value)) + ") = " + str(final_bias))
        return final_bias

    for i in range(n-1): ### ranging value is between ranging reference  
        if value < range_ref[anchor_number][i] and value > range_ref[anchor_number][i+1]:
            slope = (bias[anchor_number][i] - bias[anchor_number][i+1])/(range_ref[anchor_number][i] - range_ref[anchor_number][i+1])
            final_bias = bias[anchor_number][i+1] + (slope * (value - range_ref[anchor_number][i+1]))
            # print("A" +str(anchor_number) + " bias = " + str(bias[anchor_number][i+1]) + " + (" + str(slope) + " * " + str((value - range_ref[anchor_number][i+1])) + ") = " + str(final_bias))
            return final_bias
    ### no corresponding interval
    print("********no corresponding interval********")
    print("error value: ", value)
    return final_bias


def tag_number(td, data):
    td.header.stamp = rospy.Time.now()
    td.to_A0 = 0.
    td.to_A1 = 0.
    td.to_A2 = 0.
    td.to_A3 = 0.
    try: 
        tag_number = str(data[9])[1]

    except IndexError:
            print("data: ", data)
            return False
    
    if tag_number == '0':
        td.Tag_id = 0
        bias = T0_bias
        range_ref = T0_range
    elif tag_number == '1':
        td.Tag_id = 1
        bias = T1_bias
        range_ref = T1_range

    if(data[0] == "mc"):
        tag_used = int(data[1], 16)
        td.Anchor_available = tag_used
        if(tag_used % 2 >= 1):
            td.to_A0 = int(data[2], 16) / 1000.
        if(tag_used % 4 >= 2):
            td.to_A1 = int(data[3], 16) / 1000.
        if(tag_used % 8 >= 4):
            td.to_A2 = int(data[4], 16) / 1000.
        if(tag_used >= 8):
            td.to_A3 = int(data[5], 16) / 1000.
    else:
        return False

    print("----------------------------------------------------")
    print("T" + str(tag_number) + "_A0 raw value: " + str(td.to_A0))
    td.to_A0 = td.to_A0 - cal_bias(td.to_A0, bias, range_ref, 0)
    print("T" + str(tag_number) + "_A0 range: " + str(td.to_A0))
    print("")
    print("T" + str(tag_number) + "_A1 raw value: " + str(td.to_A1))
    td.to_A1 = td.to_A1 - cal_bias(td.to_A1, bias, range_ref, 1)
    print("T" + str(tag_number) + "_A1 range: " + str(td.to_A1))
    print("")
    print("T" + str(tag_number) + "_A2 raw value: " + str(td.to_A2))
    td.to_A2 = td.to_A2 - cal_bias(td.to_A2, bias, range_ref, 2)
    print("T" + str(tag_number) + "_A2 range: " + str(td.to_A2))
    print("")
    print("T" + str(tag_number) + "_A3 raw value: " + str(td.to_A3))
    td.to_A3 = td.to_A3 - cal_bias(td.to_A3, bias, range_ref, 3)
    print("T" + str(tag_number) + "_A3 range: " + str(td.to_A3))
    return True

def fusion(td):
    dist = float32()
    if td.Anchor_available == 15:
        dist = (td.to_A0 + td.to_A1 + td.to_A2 + td.to_A3)/4
    else if td.Anchor_available == 7 or td.Anchor_available == 11 or td.Anchor_available == 13 or td.Anchor_available == 14:
        dist = (td.to_A0 + td.to_A1 + td.to_A2 + td.to_A3)/3
    else if td.Anchor_available == 1 or td.Anchor_available == 2 or td.Anchor_available == 4 or td.Anchor_available == 8:
        dist = (td.to_A0 + td.to_A1 + td.to_A2 + td.to_A3)
    else 
        dist = (td.to_A0 + td.to_A1 + td.to_A2 + td.to_A3)/2
    return dist




    return dist

def publish_uwb():
    pub_0 = rospy.Publisher('uwb_distance_raw', tag_distance, queue_size=10)
    pub = rospy.Publisher('uwb_distance', float32, queue_size=10)
    rospy.init_node("uwb_distance", anonymous=True)
    rate = rospy.Rate(10)
    ser = serial.Serial("/dev/ttyUSB0",115200)
    
    while not rospy.is_shutdown():
        try:
            data = ser.readline()
            data = data.split(" ")
            td = tag_distance()
            distance = float32()
            # print(data)
            connection = tag_number(td, data)

            if connection == False:
                print(data)
                print("****Connection Failed****")
                print("-----------------------------")
            else:
                pub_0.publish(td)
                distance = fusion(td)
                pub.publish(distance)

            rate.sleep()

        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            break
    ser.close()
    

if __name__ == '__main__':
    publish_uwb()
