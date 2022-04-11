#include <iostream>
#include <eigen3/Eigen/Dense>
using namespace Eigen;  
using namespace std;  

// function
double distance(VectorXd, VectorXd);
VectorXd guess_range();
MatrixXd Anchor_matrix();
MatrixXd H_matrix();// (guess location - anchor location)/guess range
MatrixXd r_matrix();// (measured range - guess range) from each anchor
MatrixXd invert_matrix(MatrixXd); //pseudo-inverse
VectorXd update_guess(); 


// Anchors
int Anchor_num = 3;
VectorXd A1(3);
VectorXd A2(3);
VectorXd A3(3);

// Guess position
VectorXd G(3);
VectorXd G_range(3);

// Measured range
VectorXd m(Anchor_num);

// Variables
MatrixXd H;
MatrixXd H_inverse;
MatrixXd delta_R;
MatrixXd delta_w;

int flag = 1;
int iteration = 1;


int main()  
{  

    
    // initialize anchor locations 
    A1 << 0, 0, 1;
    A2 << 1, 0, 0;
    A3 << 0, 1, 0;
    G << 5, 5, 0; //(9, 6, 0)
    m << 15.843 + 0.01, 15.2643 - 0.01, 15 - 0.01;

    cout << "A1:\n" << A1.transpose() << endl;
    cout << "A2:\n" << A2.transpose() << endl;
    cout << "A3:\n" << A3.transpose() << endl;
    cout << "Initial guess:  " << G.transpose() << endl;

    MatrixXd test;
    VectorXd Ans(3);
    Ans << 9, 13, 0;
    test = Ans - A1;
    cout << test.norm() << endl;
    test = Ans - A2;
    cout << test.norm() << endl;
    test = Ans - A3;
    cout << test.norm() << endl;

    while(flag)
    {
        //compute guessed range
        G_range = guess_range();
        cout << "guess_range: " << endl << G_range.transpose() << endl;

        // Generate H matrix
        H = H_matrix();
        cout << "H_matrix: " << endl << H << endl;

        // invert H matrix
        H_inverse = invert_matrix(H);
        cout << "invert_matrix: " << endl << H_inverse << endl;

        // Generate delta R
        delta_R = r_matrix();
        cout << "delta_R: " << endl << delta_R << endl;

        G = update_guess();
        cout << "Iteration " << iteration << ": " << G.transpose() << endl;
        iteration++;

        // flag = 0;

        if ((delta_w.norm() < 0.00001) || iteration > 8)
        {
            flag = 0;
        }

    }
}  

VectorXd guess_range()
{
    VectorXd g_range(Anchor_num);
    MatrixXd anchor_h = Anchor_matrix();
    for (int i = 0; i < Anchor_num; i++)
    {
        g_range(i) = distance(G, anchor_h.row(i));
    }  
    return g_range;
}

MatrixXd H_matrix()
{
    MatrixXd H_final(Anchor_num, 3);
    MatrixXd anchor_h = Anchor_matrix();
    MatrixXd guess = G.transpose();

    for (int i = 0; i < Anchor_num; i++)
    {
        H_final.row(i) = (guess - anchor_h.row(i)) / G_range(i);
    }
    return H_final;
}

MatrixXd Anchor_matrix()
{
    MatrixXd h(Anchor_num,3);
    h << A1, A2, A3;
    return h.transpose();
}


double distance(VectorXd a, VectorXd b)
{  
    VectorXd m = a - b;
    double dist = m.norm();
    return dist;
}

MatrixXd invert_matrix(MatrixXd m)
{
    MatrixXd Inverse;
    Inverse = m.transpose() * m;
    Inverse = Inverse.inverse() * m.transpose();
    return Inverse;
}

MatrixXd r_matrix()
{
    MatrixXd delta_r(3,1);
    delta_r = m - G_range;
    return delta_r;
}

VectorXd update_guess()
{
    VectorXd updated_G;
    delta_w = H_inverse * delta_R;
    updated_G = G + delta_w;
    return updated_G;
}