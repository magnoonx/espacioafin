import numpy as np

def calcular_distancia_plano_punto():
    # Pedir al usuario que introduzca los parámetros del plano
    print("Introduce los parámetros del plano Ax + By + Cz + D = 0 separados por espacios:")
    parametros_plano = list(map(float, input().split()))

    # Pedir al usuario que introduzca las coordenadas del punto
    print("Introduce las coordenadas del punto separadas por espacios:")
    punto = np.array(list(map(float, input().split())))

    # Calcular la distancia del punto al plano
    A, B, C, D = parametros_plano
    x, y, z = punto
    distancia = abs(A*x + B*y + C*z + D) / np.sqrt(A**2 + B**2 + C**2)

    print("La distancia del punto al plano es:", distancia)

if __name__ == "__main__":
    calcular_distancia_plano_punto()