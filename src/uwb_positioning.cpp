#include <iostream>
#include "uwb/Position.h"
#include "ros/ros.h"

#include <uwb/tag_distance.h>
#include <uwb/uwb_Position.h>

using namespace Eigen;  
using namespace std;  


uwb::uwb_Position data;
enum Nav_sufficiency {unsufficient, sufficient}; //unsufficient: < 3 ranges received, sufficient >= 3

void uwb_distance_callback(const uwb::tag_distance& msg)
{
  uwb::uwb_Position new_data;
  data = new_data;
  Anchor range_0 = {0, msg.to_A0, 1}; 
  Anchor range_1 = {1, msg.to_A1, 1}; 
  Anchor range_2 = {2, msg.to_A2, 1}; 
  Anchor range_3 = {3, msg.to_A3, 1}; 
  Anchor temp;
  Anchor range[4] = {range_0, range_1, range_2, range_3};
  Nav_sufficiency nav_sufficiency;

  if (msg.Anchor_available == 15)
  {
    nav_sufficiency = sufficient;
    for(int i = 0; i < 4; i++)
    {
      for(int j = 0; i < 4; i++)
      {
        if (range[j].range > range[j+1].range)
        {
          swap(range[j], range[j+1]);
        }
      }
    }
  }
  else if (msg.Anchor_available == 7) //00000111
  {
    nav_sufficiency = sufficient;
  }
  else if (msg.Anchor_available == 11)//00001011
  {
    nav_sufficiency = sufficient;
    swap(range[3], range[2]);
  }
  else if (msg.Anchor_available == 13)//00001101
  {
    nav_sufficiency = sufficient;
    swap(range[3], range[1]);
  }
  else if (msg.Anchor_available == 14)//00001110
  {
    nav_sufficiency = sufficient;
    swap(range[3], range[0]);
  }
  else 
  {
    nav_sufficiency = unsufficient;
  }


  if (nav_sufficiency == sufficient)
  {
    VectorXd final_position;
    int Anchor_num = 3;

    VectorXd A1(3);
    VectorXd A2(3);
    VectorXd A3(3);
    A1 << 0, 0, 1;
    A2 << 1, 0, 0;
    A3 << 0, 1, 0;
    VectorXd A[3] = {A1, A2, A3};

    VectorXd m(3);
    m << range[0].range, range[1].range, range[2].range;

    VectorXd G(3);
    G << 3, 3, 0;
    double threshold_w = 0.000001;
    double threshold_iteration = 10;

    Position position(Anchor_num, A, m, G, threshold_w, threshold_iteration);


    final_position = position.propagate_sol();

    data.header.stamp = ros::Time::now();
    data.header.frame_id = "velodyne";
    data.x = final_position(0);
    data.y = final_position(1);
    data.z = final_position(2);
    data.Tag_id = msg.Tag_id;
    data.quality = 1;
  }
  else
  {
    cout << "***** Not enough ranging data received ! *****" << endl;
  }

}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "uwb_positioning");
  ros::NodeHandle n;

  //publisher
  ros::Publisher uwb_positioning_pub = n.advertise<uwb::uwb_Position>("uwb_position", 1);

  //subscriber
  ros::Subscriber uwb_distance_sub = n.subscribe("/uwb_distance", 1, uwb_distance_callback);

    ros::Rate loop_rate(5);

    while (ros::ok())
  {

    uwb_positioning_pub.publish(data);

    ros::spinOnce();

    loop_rate.sleep();
  }

  return 0;
}