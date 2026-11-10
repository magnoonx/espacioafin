"""
Biblioteca de Geometría Lineal, Afín y Euclidiana de Nivel de Posgrado.
Incluye modelos computacionales rigurosos para espacios afines, baricentros,
el grupo afín, isometrías euclidianas y descomposición en valores singulares (SVD).
"""

from .affine_space import AffinePoint, Vector, AffineSpace, AffineFrame
from .barycentric import (
    BarycentricCoordinates,
    Simplex,
    barycentric_to_cartesian,
    cartesian_to_barycentric,
    is_in_convex_hull
)
from .affine_group import AffineTransform, AffineGroupElement
from .isometries import (
    EuclideanIsometry,
    HyperplaneReflection,
    cartan_dieudonne_decomposition,
    classify_isometry_2d
)
from .svd_geometry import (
    GeometricSVD,
    analyze_geometric_transformation,
    ellipse_axes_from_svd
)

__all__ = [
    "AffinePoint",
    "Vector",
    "AffineSpace",
    "AffineFrame",
    "BarycentricCoordinates",
    "Simplex",
    "barycentric_to_cartesian",
    "cartesian_to_barycentric",
    "is_in_convex_hull",
    "AffineTransform",
    "AffineGroupElement",
    "EuclideanIsometry",
    "HyperplaneReflection",
    "cartan_dieudonne_decomposition",
    "classify_isometry_2d",
    "GeometricSVD",
    "analyze_geometric_transformation",
    "ellipse_axes_from_svd",
]
