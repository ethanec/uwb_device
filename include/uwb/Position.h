#ifndef POSITION_H_
#define POSITION_H_

#include <eigen3/Eigen/Dense>
using namespace Eigen;  

typedef struct Anchor
{
    int number;
    double range;
    double std;
}Anchor;

class Position
{
private:
    // Anchors
    int Anchor_num_ = 3;
    VectorXd A1_;
    VectorXd A2_;
    VectorXd A3_;

    // Guess position
    VectorXd G_;
    VectorXd G_range_;

    // Measured range
    VectorXd m_;

    // Variables
    MatrixXd H_;
    MatrixXd H_inverse_;
    MatrixXd delta_R_;
    MatrixXd delta_w_;
    int flag_ = 1;
    int iteration_ = 1;
    double threshold_w_ = 0.0001;
    double threshold_iteration_ = 8;

public:
    Position(int Anchor_num, VectorXd A[3], VectorXd m, VectorXd G, double threshold_w, double threshold_iteration);
    Position();
    ~Position();
    double distance(VectorXd, VectorXd);
    VectorXd guess_range();
    MatrixXd Anchor_matrix();
    MatrixXd H_matrix();// (guess location - anchor location)/guess range
    MatrixXd r_matrix();// (measured range - guess range) from each anchor
    MatrixXd invert_matrix(MatrixXd); //pseudo-inverse
    VectorXd update_guess(); 
    VectorXd propagate_sol();

};
#endif