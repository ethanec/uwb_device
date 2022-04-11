#include <iostream>
#include "uwb/Position.h"


using namespace Eigen;  
using namespace std;  

Position::Position(int Anchor_num, VectorXd A[3], VectorXd m, VectorXd G, double threshold_w, double threshold_iteration)
{
    A1_ = A[0];
    A2_ = A[1];
    A3_ = A[2];
    G_ = G; //(9, 6, 0)
    m_ = m;
    threshold_w_ = threshold_w;
    threshold_iteration_ = threshold_iteration;

    cout << "A1:\n" << A1_.transpose() << endl;
    cout << "A2:\n" << A2_.transpose() << endl;
    cout << "A3:\n" << A3_.transpose() << endl;
    cout << "Initial guess:  " << G_.transpose() << endl;
}
    
Position::Position()
{
    VectorXd A1(3);
    VectorXd A2(3);
    VectorXd A3(3);
    VectorXd G(3);
    VectorXd m(Anchor_num_);
    A1 << 0, 0, 1;
    A2 << 1, 0, 0;
    A3 << 0, 1, 0;
    G << 8, 5, 0; //(9, 6, 0)
    m<< 15.843 + 0.01, 15.2643 - 0.01, 15 - 0.01;

    A1_ = A1;
    A2_ = A2;
    A3_ = A3;
    G_ = G;
    m_ = m;


    cout << "A1:\n" << A1_.transpose() << endl;
    cout << "A2:\n" << A2_.transpose() << endl;
    cout << "A3:\n" << A3_.transpose() << endl;
    cout << "Initial guess:  " << G_.transpose() << endl;
}
    
Position::~Position(){}

VectorXd Position::guess_range()
{
    VectorXd g_range(Anchor_num_);
    MatrixXd anchor_h = Anchor_matrix();
    for (int i = 0; i < Anchor_num_; i++)
    {
        g_range(i) = distance(G_, anchor_h.row(i));
    }  
    return g_range;
}

MatrixXd Position::H_matrix()
{
    MatrixXd H_final(Anchor_num_, 3);
    MatrixXd anchor_h = Anchor_matrix();
    MatrixXd guess = G_.transpose();

    for (int i = 0; i < Anchor_num_; i++)
    {
        H_final.row(i) = (guess - anchor_h.row(i)) / G_range_(i);
    }
    return H_final;
}

MatrixXd Position::Anchor_matrix()
{
    MatrixXd h(Anchor_num_,3);
    h << A1_, A2_, A3_;
    return h.transpose();
}


double Position::distance(VectorXd a, VectorXd b)
{  
    VectorXd m = a - b;
    double dist = m.norm();
    return dist;
}

MatrixXd Position::invert_matrix(MatrixXd m)
{
    MatrixXd Inverse;
    Inverse = m.transpose() * m;
    Inverse = Inverse.inverse() * m.transpose();
    return Inverse;
}

MatrixXd Position::r_matrix()
{
    MatrixXd delta_r(3,1);
    delta_r = m_ - G_range_;
    return delta_r;
}

VectorXd Position::update_guess()
{
    VectorXd updated_G;
    delta_w_ = H_inverse_ * delta_R_;
    updated_G = G_ + delta_w_;
    return updated_G;
}

VectorXd Position::propagate_sol()
{
    while(flag_)
    {
        //compute guessed range
        G_range_ = guess_range();
        // cout << "guess_range: " << endl << G_range.transpose() << endl;

        // Generate H matrix
        H_ = H_matrix();
        // cout << "H_matrix: " << endl << H << endl;

        // invert H matrix
        H_inverse_ = invert_matrix(H_);
        // cout << "invert_matrix: " << endl << H_inverse << endl;

        // Generate delta R
        delta_R_ = r_matrix();
        // cout << "delta_R: " << endl << delta_R << endl;

        G_ = update_guess();
        // cout << "Iteration " << iteration << ": " << G.transpose() << endl;
        iteration_++;

        if ((delta_w_.norm() < threshold_w_) || iteration_ > threshold_iteration_)
        {
            flag_ = 0;
        }
    }
    return G_;
}