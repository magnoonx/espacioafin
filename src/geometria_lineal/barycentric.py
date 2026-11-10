"""
Módulo de Coordenadas Baricéntricas y Combinaciones Convexas.

Cubre:
- Independencia afín de familias de puntos.
- Definición formal de k-símplices (segmento, triángulo, tetraedro, n-símplice).
- Cálculo algebraico y geométrico de coordenadas baricéntricas.
- Combinaciones convexas (lambda_i >= 0, sum(lambda_i) == 1) y envoltura convexa.
- Interpolación afín de funciones escalares y vectoriales (shaders, elementos finitos).
"""

from __future__ import annotations
import math
from typing import Sequence, List, Tuple, Union, Dict, Any
import numpy as np
from .affine_space import AffinePoint, Vector


def are_affinely_independent(points: Sequence[AffinePoint]) -> bool:
    """
    Determina si un conjunto de k+1 puntos {P_0, P_1, ..., P_k} es afínmente independiente.
    Equivale a que los k vectores {P_1 - P_0, ..., P_k - P_0} sean linealmente independientes.
    """
    k = len(points) - 1
    if k <= 0:
        return True

    p0 = points[0]
    vectors = [points[i].coordinates - p0.coordinates for i in range(1, len(points))]
    matrix = np.column_stack(vectors)
    rank = np.linalg.matrix_rank(matrix)
    return rank == k


class BarycentricCoordinates:
    """Almacena y manipula las coordenadas baricéntricas (lambda_0, ..., lambda_n)."""

    def __init__(self, lambdas: Sequence[float]):
        self._lambdas = np.array(lambdas, dtype=np.float64)
        if not np.isclose(np.sum(self._lambdas), 1.0, atol=1e-5):
            raise ValueError(
                f"Las coordenadas baricéntricas deben sumar 1. Suma actual: {np.sum(self._lambdas)}"
            )

    @property
    def values(self) -> np.ndarray:
        return self._lambdas

    def is_convex(self, tol: float = 1e-7) -> bool:
        """Determina si la combinación es convexa (todos los lambda_i >= 0)."""
        return bool(np.all(self._lambdas >= -tol))

    def is_interior(self, tol: float = 1e-7) -> bool:
        """Verifica si el punto pertenece al interior relativo del símplice (lambda_i > 0)."""
        return bool(np.all(self._lambdas > tol))

    def is_boundary(self, tol: float = 1e-7) -> bool:
        """Verifica si el punto está en la frontera del símplice (convexa y algún lambda_i == 0)."""
        return self.is_convex(tol) and bool(np.any(np.isclose(self._lambdas, 0.0, atol=tol)))

    def __getitem__(self, index: int) -> float:
        return float(self._lambdas[index])

    def __len__(self) -> int:
        return len(self._lambdas)

    def __repr__(self) -> str:
        vals = ", ".join(f"λ_{i}={v:.4f}" for i, v in enumerate(self._lambdas))
        return f"BarycentricCoords({vals})"


class Simplex:
    """
    Representa un n-símplice en R^m (generalmente m = n, e.g., triángulo en R^2, tetraedro en R^3).
    Formado por n+1 vértices afínmente independientes.
    """

    def __init__(self, vertices: Sequence[AffinePoint]):
        if len(vertices) < 2:
            raise ValueError("Un símplice requiere al menos 2 vértices (1-símplice / segmento).")

        self.vertices = [AffinePoint(v.coordinates) if isinstance(v, AffinePoint) else AffinePoint(v) for v in vertices]
        self.dim_ambient = self.vertices[0].dim
        self.dim_simplex = len(self.vertices) - 1

        if not are_affinely_independent(self.vertices):
            raise ValueError("Los vértices del símplice no son afínmente independientes.")

    @property
    def barycenter(self) -> AffinePoint:
        """El centro de masa geométrico (isobaricentro): todos los pesos iguales 1/(n+1)."""
        weights = [1.0 / len(self.vertices)] * len(self.vertices)
        coords = np.mean([v.coordinates for v in self.vertices], axis=0)
        return AffinePoint(coords)

    def to_barycentric(self, point: AffinePoint) -> BarycentricCoordinates:
        """
        Calcula las coordenadas baricéntricas de un punto respecto al símplice.
        Resuelve el sistema lineal aumentado:
          [ P_0  P_1 ... P_n ] [ lambda_0 ] = [ P ]
          [  1    1  ...  1  ] [ lambda_n ]   [ 1 ]
        """
        p_coords = point.coordinates
        k = len(self.vertices)

        # Matriz con las coordenadas aumentadas de los vértices
        # Fila superior/intermedia: coordenadas de cada vértice en columnas
        # Última fila: 1's para imponer sum(lambda) = 1
        mat_cols = []
        for v in self.vertices:
            mat_cols.append(np.append(v.coordinates, 1.0))
        m_matrix = np.column_stack(mat_cols)
        rhs = np.append(p_coords, 1.0)

        # Resolución por mínimos cuadrados o sistema directo
        if m_matrix.shape[0] == m_matrix.shape[1]:
            lambdas = np.linalg.solve(m_matrix, rhs)
        else:
            lambdas, _, _, _ = np.linalg.lstsq(m_matrix, rhs, rcond=None)

        # Normalizamos numéricamente la suma
        lambdas = lambdas / np.sum(lambdas)
        return BarycentricCoordinates(lambdas)

    def from_barycentric(self, bcoords: Union[BarycentricCoordinates, Sequence[float]]) -> AffinePoint:
        """Calcula el punto cartesiano correspondiente a unas coordenadas baricéntricas."""
        weights = bcoords.values if isinstance(bcoords, BarycentricCoordinates) else np.array(bcoords)
        if len(weights) != len(self.vertices):
            raise ValueError(f"Se esperaban {len(self.vertices)} ponderaciones, llegaron {len(weights)}.")

        coords = sum(w * v.coordinates for w, v in zip(weights, self.vertices))
        return AffinePoint(coords)

    def contains(self, point: AffinePoint, tol: float = 1e-7) -> bool:
        """Determina si el punto yace dentro de la envoltura convexa del símplice."""
        bcoords = self.to_barycentric(point)
        return bcoords.is_convex(tol)

    def interpolate_attribute(
        self,
        vertex_attributes: Sequence[Union[float, Sequence[float], np.ndarray]],
        point: AffinePoint
    ) -> np.ndarray:
        """
        Interpola afínmente cualquier atributo (temperatura, color RGB, normales)
        en el punto mediante sus coordenadas baricéntricas.
        """
        bcoords = self.to_barycentric(point)
        attrs = [np.array(a, dtype=np.float64) for a in vertex_attributes]
        interpolated = sum(w * a for w, a in zip(bcoords.values, attrs))
        return interpolated

    def measure(self) -> float:
        """
        Calcula la medida (longitud, área o volumen n-dimensional) del símplice:
        Vol = 1 / n! * |det([v_1 - v_0, v_2 - v_0, ..., v_n - v_0])|
        """
        n = self.dim_simplex
        p0 = self.vertices[0].coordinates
        edges = [self.vertices[i].coordinates - p0 for i in range(1, len(self.vertices))]
        mat = np.column_stack(edges)
        if mat.shape[0] == mat.shape[1]:
            vol = abs(np.linalg.det(mat)) / math.factorial(n)
        else:
            # Caso de subespacio embebido (ej. triángulo en R^3): determinante de Gram
            gram = mat.T @ mat
            vol = np.sqrt(max(0.0, float(np.linalg.det(gram)))) / math.factorial(n)
        return float(vol)


def cartesian_to_barycentric(simplex: Simplex, point: AffinePoint) -> BarycentricCoordinates:
    return simplex.to_barycentric(point)


def barycentric_to_cartesian(simplex: Simplex, bcoords: BarycentricCoordinates) -> AffinePoint:
    return simplex.from_barycentric(bcoords)


def is_in_convex_hull(points: Sequence[AffinePoint], target: AffinePoint) -> bool:
    """Verifica si target pertenece a la envoltura convexa de points via programación lineal/optimización."""
    n_points = len(points)
    dim = target.dim
    # Minimizar 0 sujeto a: sum(lambda_i * P_i) = target, sum(lambda_i) = 1, lambda_i >= 0
    from scipy.optimize import linprog

    c = np.zeros(n_points)
    a_eq = np.vstack([
        np.array([p.coordinates for p in points]).T,
        np.ones((1, n_points))
    ])
    b_eq = np.append(target.coordinates, 1.0)
    bounds = [(0, 1) for _ in range(n_points)]

    res = linprog(c, A_eq=a_eq, b_eq=b_eq, bounds=bounds, method="highs")
    return bool(res.success)
