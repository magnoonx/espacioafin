"""
Módulo de Estructura de Espacio Afín.

Define de forma axiomática y rigurosa la distinción entre puntos y vectores:
- Espacio afín (A, V, +):
  1. A es un conjunto no vacío de puntos.
  2. V es un espacio vectorial sobre un cuerpo K (aquí K = R).
  3. La acción +: A x V -> A cumple:
     - (P + u) + v = P + (u + v) para todo P en A, u, v en V.
     - Para todo P en A, P + 0 = P.
     - Para cada par (P, Q) en A x A, existe un único vector v en V tal que Q = P + v (denotado Q - P).
"""

from __future__ import annotations
from typing import Sequence, Union, Optional
import numpy as np


class Vector:
    """Representa un vector libre en el espacio vectorial asociado V."""

    def __init__(self, coordinates: Union[Sequence[float], np.ndarray]):
        self._v = np.array(coordinates, dtype=np.float64).flatten()

    @property
    def data(self) -> np.ndarray:
        return self._v

    @property
    def dim(self) -> int:
        return len(self._v)

    def __len__(self) -> int:
        return self.dim

    def __getitem__(self, item: int) -> float:
        return float(self._v[item])

    def __add__(self, other: Union[Vector, np.ndarray]) -> Vector:
        if isinstance(other, Vector):
            return Vector(self._v + other._v)
        if isinstance(other, (list, tuple, np.ndarray)):
            return Vector(self._v + np.array(other, dtype=np.float64))
        raise TypeError(f"Operación no permitida: Vector + {type(other).__name__}")

    def __sub__(self, other: Union[Vector, np.ndarray]) -> Vector:
        if isinstance(other, Vector):
            return Vector(self._v - other._v)
        if isinstance(other, (list, tuple, np.ndarray)):
            return Vector(self._v - np.array(other, dtype=np.float64))
        raise TypeError(f"Operación no permitida: Vector - {type(other).__name__}")

    def __mul__(self, scalar: float) -> Vector:
        return Vector(self._v * float(scalar))

    def __rmul__(self, scalar: float) -> Vector:
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> Vector:
        return Vector(self._v / float(scalar))

    def __neg__(self) -> Vector:
        return Vector(-self._v)

    def dot(self, other: Vector) -> float:
        """Producto interno canónico."""
        return float(np.dot(self._v, other._v))

    def norm(self) -> float:
        """Norma euclidiana inducida."""
        return float(np.linalg.norm(self._v))

    def normalized(self) -> Vector:
        """Vector unitario en la misma dirección."""
        n = self.norm()
        if n == 0:
            raise ValueError("No se puede normalizar el vector nulo.")
        return self / n

    def __repr__(self) -> str:
        coords_str = ", ".join(f"{x:.4g}" for x in self._v)
        return f"Vector([{coords_str}])"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return False
        return np.allclose(self._v, other._v)


class AffinePoint:
    """
    Representa un punto en el espacio afín A.
    Los puntos no tienen origen intrínseco.
    Operaciones permitidas:
      - Punto + Vector -> Punto
      - Punto - Vector -> Punto
      - Punto - Punto  -> Vector
      - Combinaciones afines (suma ponderada con sum(pesos) == 1).
    Operación prohibida:
      - Punto + Punto (lanza TypeError explicativo).
    """

    def __init__(self, coordinates: Union[Sequence[float], np.ndarray]):
        self._coords = np.array(coordinates, dtype=np.float64).flatten()

    @property
    def coordinates(self) -> np.ndarray:
        return self._coords

    @property
    def dim(self) -> int:
        return len(self._coords)

    def __len__(self) -> int:
        return self.dim

    def __getitem__(self, item: int) -> float:
        return float(self._coords[item])

    def __add__(self, other: object) -> AffinePoint:
        if isinstance(other, Vector):
            return AffinePoint(self._coords + other.data)
        if isinstance(other, AffinePoint):
            raise TypeError(
                "¡Error de Fundamento Geométrico! La suma de dos puntos (P + Q) "
                "no está definida en un espacio afín porque los puntos carecen de origen. "
                "Para promediar o combinar puntos, use combinaciones baricéntricas: "
                "sum(lambda_i * P_i) con sum(lambda_i) = 1."
            )
        raise TypeError(f"No se puede sumar {type(other).__name__} a un AffinePoint.")

    def __sub__(self, other: object) -> Union[Vector, AffinePoint]:
        if isinstance(other, AffinePoint):
            # Punto - Punto = Vector que une ambos puntos
            return Vector(self._coords - other._coords)
        if isinstance(other, Vector):
            # Punto - Vector = Punto trasladado en dirección opuesta
            return AffinePoint(self._coords - other.data)
        raise TypeError(f"Operación inválida: AffinePoint - {type(other).__name__}")

    def distance_to(self, other: AffinePoint) -> float:
        """Distancia euclidiana entre dos puntos: ||P - Q||."""
        return (self - other).norm()

    def __repr__(self) -> str:
        coords_str = ", ".join(f"{x:.4g}" for x in self._coords)
        return f"AffinePoint({coords_str})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AffinePoint):
            return False
        return np.allclose(self._coords, other._coords)


class AffineFrame:
    """
    Sistema de referencia afín R = (O; e_1, e_2, ..., e_n).
    Permite expresar cualquier punto P como: P = O + sum(x_i * e_i).
    """

    def __init__(self, origin: AffinePoint, basis: Sequence[Vector]):
        self.origin = origin
        self.basis = list(basis)
        self.dim = origin.dim

        if len(self.basis) != self.dim:
            raise ValueError(
                f"La base debe tener {self.dim} vectores linealmente independientes para dimensión {self.dim}."
            )

        # Matriz cuyas columnas son los vectores de la base
        self._basis_matrix = np.column_stack([v.data for v in self.basis])
        det = np.linalg.det(self._basis_matrix)
        if np.isclose(det, 0.0):
            raise ValueError("Los vectores de la base no son linealmente independientes (det = 0).")

        self._inv_basis_matrix = np.linalg.inv(self._basis_matrix)

    def point_to_coordinates(self, point: AffinePoint) -> np.ndarray:
        """Calcula las coordenadas afines (x_1, ..., x_n) del punto en este marco."""
        diff_vector = (point - self.origin).data
        return self._inv_basis_matrix @ diff_vector

    def coordinates_to_point(self, coords: Sequence[float]) -> AffinePoint:
        """Reconstruye el punto a partir de sus coordenadas en el marco: P = O + sum(x_i * e_i)."""
        coords_arr = np.array(coords, dtype=np.float64)
        disp = Vector(self._basis_matrix @ coords_arr)
        return self.origin + disp

    @classmethod
    def canonical(cls, dim: int = 2) -> AffineFrame:
        """Crea el marco afín canónico (origen en 0 y base canónica)."""
        origin = AffinePoint(np.zeros(dim))
        basis = [Vector(np.eye(dim)[:, i]) for i in range(dim)]
        return cls(origin, basis)


class AffineSpace:
    """Espacio afín de dimensión n."""

    def __init__(self, dim: int):
        self.dim = dim
        self.canonical_frame = AffineFrame.canonical(dim)

    def point(self, *coords: float) -> AffinePoint:
        if len(coords) != self.dim:
            raise ValueError(f"Se esperaban {self.dim} coordenadas, pero se recibieron {len(coords)}.")
        return AffinePoint(coords)

    def vector(self, *coords: float) -> Vector:
        if len(coords) != self.dim:
            raise ValueError(f"Se esperaban {self.dim} coordenadas, pero se recibieron {len(coords)}.")
        return Vector(coords)

    @staticmethod
    def affine_combination(points: Sequence[AffinePoint], weights: Sequence[float]) -> AffinePoint:
        """
        Calcula una combinación afín sum(lambda_i * P_i) sujeta a sum(lambda_i) == 1.
        Es independiente del sistema de referencia afín elegido.
        """
        weights_arr = np.array(weights, dtype=np.float64)
        if not np.isclose(np.sum(weights_arr), 1.0, atol=1e-7):
            raise ValueError(
                f"La suma de ponderaciones afines debe ser exactamente 1. Suma actual: {np.sum(weights_arr)}"
            )

        coords = sum(w * p.coordinates for w, p in zip(weights_arr, points))
        return AffinePoint(coords)
