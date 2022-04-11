#include <iostream>
#include <eigen3/Eigen/Dense>
using namespace Eigen;  
using namespace std;  


double distance(MatrixXd, MatrixXd);
MatrixXd invert_matrix(MatrixXd);

// Anchors
VectorXd A1(3);
VectorXd A2(3);
VectorXd A3(3);

int main()  
{  
    MatrixXd a1 = MatrixXd::Constant(3,3,2);
    MatrixXd a2 = MatrixXd::Constant(3,3,3);
    double a = distance(a1, a2);

    A1 << 1, 2, 3;
    A2 << 1, 2, 3;
    A3 << 1, 2, 3;

    cout << "  A1:\n" << A1 << endl;
    cout << "  A2:\n" << A2 << endl;
    cout << "  A3:\n" << A3 << endl;

    VectorXd A4(4);
    A1 = A4;
    A1 << 1, 2, 3, 4;
    cout << "  A1:\n" << A1 << endl;

    MatrixXd a3(4,3);
    a3 << 1, 2, 1, 
          2, 1, 0, 
         -1, 1, 2,
          5, 9, 6;
    cout << endl << a3 << endl;
    cout << endl << invert_matrix(a3) << endl;
    cout << endl << invert_matrix(a3) * a3 << endl;

}  

double distance(MatrixXd a, MatrixXd b)
{  
    cout << "a =" << endl << a << endl;
    cout << "b =" << endl << b << endl;
    cout << "size of a: " << a.size() << endl;
    cout << "size of b: " << b.size() << endl;
    MatrixXd m1 = a - b;
    cout << "a - b: " << endl << m1 << endl;
    MatrixXd m2 = a * b;
    cout << "a x b: " << endl << m2 << endl;
    MatrixXd m3 = a.array() * b.array();
    cout << "a .x b: " << endl << m3 << endl;
    double m4 = a.sum();
    cout << "sum of a: " << endl << m4 << endl;

    return 0;
}

MatrixXd invert_matrix(MatrixXd m)
{
    MatrixXd Inverse;
    Inverse = m.transpose() * m;
    Inverse = Inverse.inverse() * m.transpose();
    return Inverse;
}