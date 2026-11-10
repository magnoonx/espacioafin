#include "matplotlibcpp.h"
#include <cmath>

namespace plt = matplotlibcpp;

int main() {
    // Parámetros de la elipse
    double a = 3.0;  // Semieje mayor
    double b = 2.0;  // Semieje menor

    // Crear los puntos de la elipse
    int num_points = 100;
    std::vector<double> x(num_points);
    std::vector<double> y(num_points);
    for (int i = 0; i < num_points; i++) {
        double angle = 2 * M_PI * i / num_points;
        x[i] = a * cos(angle);
        y[i] = b * sin(angle);
    }

    // Graficar la elipse
    plt::plot(x, y);
    plt::title("Elipse");
    plt::show();

    return 0;
}