"""
Módulo del Grupo Afín y Transformaciones Afines.

El grupo afín Aff(E) representa todas las biyecciones de un espacio afín
que preservan combinaciones afines (preservan rectas, paralelismo y razones simples).
Estructuralmente es un producto semidirecto:
  Aff(n) = R^n ⋊ GL(n, R)

En coordenadas homogéneas, cualquier transformación afín f(P) = A*P + b
se representa como una matriz de (n+1) x (n+1):
  [ A   b ]
  [ 0   1 ]
"""

from __future__ import annotations
from typing import Sequence, Union, Optional, Tuple
import numpy as np
from .affine_space import AffinePoint, Vector


class AffineTransform:
    """
    Representa una aplicación afín f: A -> A definida por:
      f(P) = A @ P + b
    y su aplicación lineal asociada (diferencial):
      vec{f}(v) = A @ v
    """

    def __init__(self, linear_matrix: np.ndarray, translation_vector: Union[Sequence[float], np.ndarray]):
        self.A = np.array(linear_matrix, dtype=np.float64)
        self.b = np.array(translation_vector, dtype=np.float64).flatten()
        self.dim = len(self.b)

        if self.A.shape != (self.dim, self.dim):
            raise ValueError(f"Las dimensiones no coinciden: matriz {self.A.shape} y vector {self.b.shape}")

    @classmethod
    def from_homogeneous_matrix(cls, matrix: np.ndarray) -> AffineTransform:
        """Construye la transformación a partir de su matriz homogénea (n+1) x (n+1)."""
        mat = np.array(matrix, dtype=np.float64)
        dim = mat.shape[0] - 1
        A = mat[:dim, :dim]
        b = mat[:dim, dim]
        return cls(A, b)

    @classmethod
    def translation(cls, v: Union[Vector, Sequence[float]]) -> AffineTransform:
        coords = v.data if isinstance(v, Vector) else np.array(v, dtype=np.float64)
        dim = len(coords)
        return cls(np.eye(dim), coords)

    @classmethod
    def scaling(cls, factors: Union[float, Sequence[float]], center: Optional[AffinePoint] = None, dim: int = 2) -> AffineTransform:
        """Homotecia / escalado respecto a un centro especificado (por defecto el origen)."""
        if isinstance(factors, (int, float)):
            A = np.eye(dim) * float(factors)
        else:
            A = np.diag(factors)
            dim = len(factors)

        if center is None:
            return cls(A, np.zeros(dim))

        c = center.coordinates
        b = c - A @ c
        return cls(A, b)

    @classmethod
    def rotation_2d(cls, angle_rad: float, center: Optional[AffinePoint] = None) -> AffineTransform:
        """Rotación en el plano por un ángulo theta (en radianes) respecto a un centro."""
        cos_t, sin_t = np.cos(angle_rad), np.sin(angle_rad)
        A = np.array([[cos_t, -sin_t], [sin_t, cos_t]])
        if center is None:
            return cls(A, [0.0, 0.0])
        c = center.coordinates
        b = c - A @ c
        return cls(A, b)

    @classmethod
    def shear_2d(cls, kx: float = 0.0, ky: float = 0.0) -> AffineTransform:
        """Cizalladura (shear) plana."""
        A = np.array([[1.0, kx], [ky, 1.0]])
        return cls(A, [0.0, 0.0])

    @property
    def homogeneous_matrix(self) -> np.ndarray:
        """Devuelve la matriz en coordenadas homogéneas de tamaño (n+1) x (n+1)."""
        h_mat = np.eye(self.dim + 1, dtype=np.float64)
        h_mat[:self.dim, :self.dim] = self.A
        h_mat[:self.dim, self.dim] = self.b
        return h_mat

    @property
    def determinant(self) -> float:
        """Determinante de la parte lineal: razón de cambio de volumen con signo."""
        return float(np.linalg.det(self.A))

    def is_invertible(self) -> bool:
        """Verifica si pertenece al grupo afín Aff(n) (det(A) != 0)."""
        return not np.isclose(self.determinant, 0.0)

    def inverse(self) -> AffineTransform:
        """Calcula la transformación inversa f^(-1)(P) = A^(-1) P - A^(-1) b."""
        if not self.is_invertible():
            raise ValueError("La transformación afín es singular; no pertenece a Aff(n).")
        inv_A = np.linalg.inv(self.A)
        inv_b = -inv_A @ self.b
        return AffineTransform(inv_A, inv_b)

    def compose(self, other: AffineTransform) -> AffineTransform:
        """
        Composición (self o other): primero aplica 'other', luego 'self'.
        f(g(P)) = A_1 (A_2 P + b_2) + b_1 = (A_1 A_2) P + (A_1 b_2 + b_1).
        """
        if self.dim != other.dim:
            raise ValueError("Las transformaciones deben operar en la misma dimensión.")
        new_A = self.A @ other.A
        new_b = self.A @ other.b + self.b
        return AffineTransform(new_A, new_b)

    def __matmul__(self, other: AffineTransform) -> AffineTransform:
        return self.compose(other)

    def apply_point(self, point: AffinePoint) -> AffinePoint:
        """Aplica la transformación afín a un punto: f(P) = A @ P + b."""
        return AffinePoint(self.A @ point.coordinates + self.b)

    def apply_vector(self, vector: Vector) -> Vector:
        """Aplica la parte lineal a un vector libre (las traslaciones no afectan vectores): vec{f}(v) = A @ v."""
        return Vector(self.A @ vector.data)

    def find_fixed_points(self) -> Tuple[str, Optional[AffinePoint]]:
        """
        Analiza el conjunto de puntos fijos Resolviendo (A - I) x = -b.
        Devuelve ('unique', punto), ('manifold', None) o ('none', None).
        """
        M = self.A - np.eye(self.dim)
        rank_M = np.linalg.matrix_rank(M)
        augmented = np.column_stack([M, -self.b])
        rank_aug = np.linalg.matrix_rank(augmented)

        if rank_M < rank_aug:
            return "none", None
        elif rank_M == self.dim:
            x = np.linalg.solve(M, -self.b)
            return "unique", AffinePoint(x)
        else:
            return "manifold", None

    def __repr__(self) -> str:
        return f"AffineTransform(dim={self.dim}, det={self.determinant:.4g})"


AffineGroupElement = AffineTransform
