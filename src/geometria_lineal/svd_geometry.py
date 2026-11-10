"""
Módulo de Descomposición en Valores Singulares (SVD) orientada a la Geometría.

Toda aplicación lineal A: R^n -> R^m se descompone como:
  A = U @ Sigma @ V^T

Interpretación geométrica fundamental:
  1. V^T efectúa una rotación/reflexión en el espacio de origen, alineando
     las direcciones de máxima deformación con la base canónica.
  2. Sigma estira o comprime a lo largo de los ejes ortogonales por los factores sigma_1, sigma_2, ...
     Transforma la esfera unitaria en un elipsoide con semiejes principales de longitud sigma_i.
  3. U efectúa una rotación/reflexión en el espacio de destino, orientando el elipsoide.

Consecuencias geométricas:
  - Factorización Polar: A = R @ S (Rotación pura por estiramiento simétrico definido positivo).
  - Problema de Procrustes: Hallar la rotación/isometría más cercana a una deformación dada: R = U @ V^T.
  - Deformación de área/volumen: det(A) = (+-) prod(sigma_i).
"""

from __future__ import annotations
from typing import Sequence, Tuple, Dict, Any, List
import numpy as np


class GeometricSVD:
    """Análisis geométrico completo del SVD de una transformación lineal/afín."""

    def __init__(self, matrix: np.ndarray):
        self.A = np.array(matrix, dtype=np.float64)
        if self.A.ndim != 2:
            raise ValueError("La matriz debe ser bidimensional.")

        self.m, self.n = self.A.shape
        self.U, self.singular_values, self.Vt = np.linalg.svd(self.A, full_matrices=True)
        self.V = self.Vt.T

        # Construcción de la matriz Sigma con dimensiones (m, n)
        self.Sigma = np.zeros((self.m, self.n), dtype=np.float64)
        for i in range(min(self.m, self.n)):
            self.Sigma[i, i] = self.singular_values[i]

    @property
    def condition_number(self) -> float:
        """Número de condición: razón sigma_max / sigma_min. Mide la anisotropía."""
        if self.singular_values[-1] == 0:
            return float("inf")
        return float(self.singular_values[0] / self.singular_values[-1])

    @property
    def rank(self) -> int:
        return int(np.sum(self.singular_values > 1e-10))

    def polar_decomposition(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcula la descomposición polar A = R @ S, donde R es ortogonal y S es simétrica semidefinida positiva.
        R = U @ V^T
        S = V @ Sigma @ V^T
        """
        if self.m != self.n:
            raise ValueError("La descomposición polar requiere una matriz cuadrada.")
        R = self.U @ self.Vt
        # Si det(R) < 0, podemos corregir la reflexión si se desea rotación pura, pero R es ortogonal canónica
        S = self.V @ self.Sigma @ self.Vt
        return R, S

    def closest_rotation(self) -> np.ndarray:
        """Resuelve el problema ortogonal de Procrustes: argmin_{R in SO(n)} ||A - R||_F."""
        R = self.U @ self.Vt
        if np.linalg.det(R) < 0:
            # Corrección para asegurar det(R) = +1
            u_mod = self.U.copy()
            u_mod[:, -1] *= -1
            R = u_mod @ self.Vt
        return R

    def principal_axes_2d(self) -> Dict[str, Any]:
        """Para transformaciones en R^2, devuelve los ejes semiejes, orientaciones y vectores."""
        if (self.m, self.n) != (2, 2):
            raise ValueError("Este método requiere una matriz de 2x2.")

        sigma1, sigma2 = self.singular_values[0], self.singular_values[1]
        u1, u2 = self.U[:, 0], self.U[:, 1]
        v1, v2 = self.V[:, 0], self.V[:, 1]

        # Semiejes del elipsoide deformado
        semi_axis_1 = sigma1 * u1
        semi_axis_2 = sigma2 * u2

        angle_v1 = float(np.arctan2(v1[1], v1[0]))
        angle_u1 = float(np.arctan2(u1[1], u1[0]))

        return {
            "sigma1": sigma1,
            "sigma2": sigma2,
            "v1": v1,
            "v2": v2,
            "u1": u1,
            "u2": u2,
            "semi_axis_1": semi_axis_1,
            "semi_axis_2": semi_axis_2,
            "angle_input_rad": angle_v1,
            "angle_output_rad": angle_u1,
            "area_scale_factor": float(sigma1 * sigma2),
            "anisotropy_ratio": float(sigma1 / sigma2) if sigma2 > 1e-12 else float("inf")
        }

    def transform_unit_circle(self, n_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genera los puntos del círculo unitario theta in [0, 2pi]
        y su imagen transformada (elipse) bajo A.
        """
        thetas = np.linspace(0, 2 * np.pi, n_points)
        circle = np.vstack([np.cos(thetas), np.sin(thetas)]) # 2 x n_points
        ellipse = self.A @ circle
        return circle, ellipse


def analyze_geometric_transformation(matrix: np.ndarray) -> Dict[str, Any]:
    gsvd = GeometricSVD(matrix)
    data = {
        "singular_values": gsvd.singular_values.tolist(),
        "condition_number": gsvd.condition_number,
        "rank": gsvd.rank,
        "det": float(np.linalg.det(matrix)) if matrix.shape[0] == matrix.shape[1] else None
    }
    if matrix.shape == (2, 2):
        data["2d_details"] = gsvd.principal_axes_2d()
    return data


def ellipse_axes_from_svd(matrix: np.ndarray) -> Tuple[np.ndarray, np.ndarray, float, float]:
    """Devuelve (u1, u2, sigma1, sigma2) para visualización paramétrica de la elipse."""
    gsvd = GeometricSVD(matrix)
    axes = gsvd.principal_axes_2d()
    return axes["u1"], axes["u2"], axes["sigma1"], axes["sigma2"]
