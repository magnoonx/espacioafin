import numpy as np

def calcular_interseccion_plano_recta():
    # Pedir al usuario que introduzca los parámetros del plano y la recta
    print("Introduce los parámetros del plano Ax + By + Cz + D = 0 separados por espacios:")
    parametros_plano = list(map(float, input().split()))

    print("Introduce los parámetros del vector director de la recta separados por espacios:")
    vector_director = np.array(list(map(float, input().split())))

    print("Introduce un punto de la recta separando sus coordenadas por espacios:")
    punto_recta = np.array(list(map(float, input().split())))

    # Calcular la intersección del plano con la recta
    A, B, C, D = parametros_plano
    x0, y0, z0 = punto_recta
    t = (-D - A*x0 - B*y0 - C*z0) / (A*vector_director[0] + B*vector_director[1] + C*vector_director[2])
    punto_interseccion = punto_recta + t * vector_director

    print("El punto de intersección es:", punto_interseccion)

if __name__ == "__main__":
    calcular_interseccion_plano_recta()
