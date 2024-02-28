import numpy as np
from typing import List, Optional, Tuple
from .utils import normalize
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .objects import SceneObject


class Ray:
    def __init__(self, origin: np.ndarray, direction: np.ndarray):
        self.origin = origin
        self.direction = normalize(direction)

    def nearest_intersected_object(self, objects: List["SceneObject"]) -> Optional[Tuple[float, "SceneObject"]]:
        closest_intersection = None

        for obj in objects:
            intersection = obj.intersect(self)
            if intersection:
                dist, hit_obj = intersection
                if closest_intersection is None or dist < closest_intersection[0]:
                    closest_intersection = (dist, hit_obj)

        return closest_intersection
