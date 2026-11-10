"""
Módulo de Espacios Euclidianos, Isometrías y Teorema de Cartan-Dieudonné.

Una isometría afín f: E -> E preserva la distancia euclidiana:
  d(f(P), f(Q)) = d(P, Q) para todo P, Q.

Estructura:
- La parte lineal A pertenece al grupo ortogonal O(n) (A^T * A = I).
- Directa (movimiento rígido) si det(A) = +1 (A en SO(n)).
- Inversa si det(A) = -1.

Teorema de Cartan-Dieudonné:
  Toda isometría en un espacio afín euclidiano de dimensión n se puede
  descomponer en el producto de a lo más (n + 1) reflexiones hiperplanas.
"""

from __future__ import annotations
from typing import Sequence, Union, Optional, Tuple, List, Dict, Any
import numpy as np
from .affine_space import AffinePoint, Vector
from .affine_group import AffineTransform


class HyperplaneReflection:
    """
    Representa una reflexión respecto a un hiperplano H definido por:
      H = { P : <P - P_0, n> = 0 }, donde n es el vector normal unitario.
    La acción en un punto es:
      S_H(P) = P - 2 * <P - P_0, n> * n
    """

    def __init__(self, point_on_plane: AffinePoint, normal: Union[Vector, Sequence[float]]):
        self.p0 = point_on_plane
        norm_vec = normal if isinstance(normal, Vector) else Vector(normal)
        self.n = norm_vec.normalized()
        self.dim = self.p0.dim

        # Matriz lineal de Householder: H = I - 2 * (n * n^T)
        n_arr = self.n.data.reshape(-1, 1)
        self.A = np.eye(self.dim) - 2.0 * (n_arr @ n_arr.T)
        self.b = 2.0 * float(np.dot(self.p0.coordinates, self.n.data)) * self.n.data

    def to_affine_transform(self) -> AffineTransform:
        return AffineTransform(self.A, self.b)

    def apply(self, point: AffinePoint) -> AffinePoint:
        return self.to_affine_transform().apply_point(point)

    def __repr__(self) -> str:
        return f"HyperplaneReflection(p0={self.p0}, normal={self.n})"


class EuclideanIsometry(AffineTransform):
    """
    Isometría en espacio euclidiano. Hereda de AffineTransform pero
    restringida a matrices ortogonales (A^T A = I).
    """

    def __init__(self, orthogonal_matrix: np.ndarray, translation_vector: Union[Sequence[float], np.ndarray]):
        A = np.array(orthogonal_matrix, dtype=np.float64)
        if not np.allclose(A.T @ A, np.eye(A.shape[0]), atol=1e-5):
            raise ValueError("La matriz lineal no es ortogonal (A^T A != I). No es una isometría.")
        super().__init__(A, translation_vector)

    @property
    def is_direct(self) -> bool:
        """True si preserva la orientación (det = +1), False si la invierte (det = -1)."""
        return np.isclose(self.determinant, 1.0, atol=1e-5)


def classify_isometry_2d(isometry: EuclideanIsometry) -> Dict[str, Any]:
    """
    Clasificación exhaustiva de isometrías en R^2:
    1. Directas (det = +1):
       - Traslación pura (A = I, b != 0)
       - Identidad (A = I, b == 0)
       - Rotación pura alrededor de un centro C con ángulo theta != 0.
    2. Inversas (det = -1):
       - Reflexión pura respecto a una recta L (puntos fijos forman la recta).
       - Reflexión con deslizamiento (glide reflection): reflexión respecto a L seguida de traslación paralela a L.
    """
    A = isometry.A
    b = isometry.b
    is_direct = isometry.is_direct

    if is_direct:
        # Rotación o traslación
        angle = float(np.arctan2(A[1, 0], A[0, 0]))
        if np.isclose(angle, 0.0, atol=1e-6):
            if np.allclose(b, 0.0, atol=1e-6):
                return {"type": "identity", "description": "Identidad"}
            return {"type": "translation", "vector": Vector(b), "description": f"Traslación por {Vector(b)}"}
        else:
            # Centro de rotación: (I - A) C = b => C = (I - A)^(-1) b
            center_coords = np.linalg.solve(np.eye(2) - A, b)
            center = AffinePoint(center_coords)
            angle_deg = np.degrees(angle)
            return {
                "type": "rotation",
                "center": center,
                "angle_rad": angle,
                "angle_deg": angle_deg,
                "description": f"Rotación de {angle_deg:.2f}° con centro en {center}"
            }
    else:
        # Reflexión o reflexión con deslizamiento
        # Valores propios de A son +1 y -1.
        eigvals, eigvecs = np.linalg.eigh(A)
        # Vector director de la recta (eje propio asociado a +1)
        idx_pos = int(np.argmax(eigvals))
        idx_neg = 1 - idx_pos
        v_dir = eigvecs[:, idx_pos]  # Dirección del eje de reflexión
        n_norm = eigvecs[:, idx_neg] # Normal a la recta

        # Descomponemos b en componente paralela y normal a v_dir:
        b_parallel = np.dot(b, v_dir) * v_dir
        b_perp = np.dot(b, n_norm) * n_norm

        # Punto sobre el eje: (I - A) p0 = b_perp
        # Como A * n_norm = - n_norm, (I - A) n_norm = 2 n_norm
        # Por tanto, p0 = b_perp / 2
        p0 = AffinePoint(b_perp / 2.0)

        if np.allclose(b_parallel, 0.0, atol=1e-5):
            return {
                "type": "reflection",
                "axis_point": p0,
                "axis_direction": Vector(v_dir),
                "description": f"Reflexión pura respecto a la recta por {p0} con dirección {Vector(v_dir)}"
            }
        else:
            return {
                "type": "glide_reflection",
                "axis_point": p0,
                "axis_direction": Vector(v_dir),
                "glide_vector": Vector(b_parallel),
                "description": f"Reflexión con deslizamiento: eje por {p0} y vector {Vector(b_parallel)}"
            }


def cartan_dieudonne_decomposition(isometry: EuclideanIsometry) -> List[HyperplaneReflection]:
    """
    Implementación constructiva del Teorema de Cartan-Dieudonné para R^2:
    Descompone cualquier isometría en a lo más 3 reflexiones hiperplanas (rectas).
    """
    dim = isometry.dim
    if dim != 2:
        raise NotImplementedError("La descomposición explícita está implementada para R^2.")

    info = classify_isometry_2d(isometry)
    t_type = info["type"]

    if t_type == "identity":
        return []

    if t_type == "reflection":
        # 1 reflexión
        p0 = info["axis_point"]
        v_dir = info["axis_direction"].data
        normal = np.array([-v_dir[1], v_dir[0]])
        return [HyperplaneReflection(p0, normal)]

    if t_type == "translation":
        # 2 reflexiones respecto a dos rectas paralelas separadas por d = ||b|| / 2
        b = isometry.b
        dist = np.linalg.norm(b)
        n = b / dist
        # Recta 1: pasa por el origen con normal n
        r1 = HyperplaneReflection(AffinePoint([0.0, 0.0]), n)
        # Recta 2: pasa por b/2 con la misma normal n
        r2 = HyperplaneReflection(AffinePoint(b / 2.0), n)
        return [r1, r2]

    if t_type == "rotation":
        # 2 reflexiones respecto a dos rectas que se intersecan en el centro C con ángulo theta / 2
        c = info["center"]
        theta = info["angle_rad"]
        # Recta 1: horizontal a través de C (normal = (0, 1))
        n1 = np.array([0.0, 1.0])
        # Recta 2: rotada un ángulo theta/2
        alpha = theta / 2.0
        n2 = np.array([-np.sin(alpha), np.cos(alpha)])
        return [
            HyperplaneReflection(c, n1),
            HyperplaneReflection(c, n2)
        ]

    if t_type == "glide_reflection":
        # 3 reflexiones: la reflexión pura + las 2 de la traslación paralela
        p0 = info["axis_point"]
        v_dir = info["axis_direction"].data
        glide_v = info["glide_vector"].data
        normal = np.array([-v_dir[1], v_dir[0]])

        # R1: el eje de reflexión
        r1 = HyperplaneReflection(p0, normal)
        # R2 y R3: descomponen la traslación paralela glide_v a lo largo de v_dir
        n_glide = v_dir / np.linalg.norm(v_dir)
        r2 = HyperplaneReflection(p0, n_glide)
        r3 = HyperplaneReflection(AffinePoint(p0.coordinates + glide_v / 2.0), n_glide)
        return [r1, r2, r3]

    return []
