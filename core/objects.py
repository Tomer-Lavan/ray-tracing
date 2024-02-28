import numpy as np
from .utils import normalize
from .ray import Ray
from typing import Tuple, Union, Optional


class Object3D:
    def set_material(self, ambient: np.ndarray, diffuse: np.ndarray, specular: np.ndarray, shininess: float,
                     reflection: float, refractive_index: float = 0):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.reflection = reflection
        self.refractive_index = refractive_index


class Plane(Object3D):
    def __init__(self, normal: np.ndarray, point: np.ndarray):
        self.normal = np.array(normal)
        self.point = np.array(point)

    def intersect(self, ray: Ray) -> Optional[Tuple[float, 'Plane']]:
        denom = np.dot(self.normal, ray.direction)
        if abs(denom) < 1e-6:
            return None
        t = np.dot(self.point - ray.origin, self.normal) / denom
        if t > 0:
            return t, self
        return None

    def compute_normal(self, hit_point: np.ndarray) -> np.ndarray:
        return self.normal


class Rectangle(Object3D):
    """
        A rectangle is defined by a list of vertices as follows:
        a _ _ _ _ _ _ _ _ d
         |               |  
         |               |  
         |_ _ _ _ _ _ _ _|
        b                 c
        This function gets the vertices and creates a rectangle object
    """

    def __init__(self, a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray):
        """
            ul -> bl -> br -> ur
        """
        self.abcd = [np.asarray(v) for v in [a, b, c, d]]
        self.normal = self.compute_normal()

    def compute_normal(self, point: np.ndarray = None) -> np.ndarray:
        bc = self.abcd[2] - self.abcd[1]
        ba = self.abcd[0] - self.abcd[1]
        return normalize(np.cross(bc, ba))

    def intersect(self, ray: Ray) -> Optional[Tuple[float, 'Plane']]:
        rectangle_plane = Plane(self.normal, self.abcd[0])
        intersection = rectangle_plane.intersect(ray)
        if intersection:
            dist, hit_obj = intersection
            hit_point = ray.origin + dist * ray.direction
            is_point_in_rec = self.check_point_in_rectangle(hit_point)
            if is_point_in_rec:
                return dist, self

        return None

    def check_point_in_rectangle(self, point: np.ndarray) -> bool:
        for i in range(len(self.abcd)):
            v1 = self.abcd[i] - point
            v2 = self.abcd[(i+1) % 4] - point
            if np.dot(self.normal, np.cross(v1, v2)) <= 0:
                return False
        return True


class Cuboid(Object3D):
    def __init__(self, a, b, c, d, e, f):
        """ 
              g+---------+f
              /|        /|
             / |  E C  / |
           a+--|------+d |
            |Dh+------|B +e
            | /  A    | /
            |/     F  |/
           b+--------+/c
        """
        g = list(np.array(a) + (np.array(f)-np.array(d)))
        h = list(np.array(b) + (np.array(e)-np.array(c)))
        A = Rectangle(a, b, c, d)
        B = Rectangle(d, c, e, f)
        C = Rectangle(g, h, e, f)
        D = Rectangle(a, b, h, g)
        E = Rectangle(g, a, d, f)
        F = Rectangle(h, b, c, e)
        self.face_list = [A, B, C, D, E, F]

    def apply_materials_to_faces(self):
        for t in self.face_list:
            t.set_material(self.ambient, self.diffuse,
                           self.specular, self.shininess, self.reflection)

    def intersect(self, ray: Ray):
        closest_intersection = None

        for rectangle in self.face_list:
            intersection = rectangle.intersect(ray)
            if intersection:
                dist, obj = intersection
                if closest_intersection is None or dist < closest_intersection[0]:
                    closest_intersection = (dist, rectangle)

        return closest_intersection


class Sphere(Object3D):
    def __init__(self, center: np.ndarray, radius: float):
        self.center = center
        self.radius = radius
        self.normal = self.center

    def intersect(self, ray: Ray) -> Optional[Tuple[float, 'Sphere']]:
        b = 2 * np.dot(ray.direction, ray.origin - self.center)
        c = np.linalg.norm(ray.origin - self.center) ** 2 - self.radius ** 2
        discriminant = b ** 2 - 4 * c
        if discriminant > 0:
            dist1 = (-b + np.sqrt(discriminant)) / 2
            dist2 = (-b - np.sqrt(discriminant)) / 2
            if dist1 > 0 and dist2 > 0:
                min_dist = min(dist1, dist2)
                return min_dist, self

        return None

    def compute_normal(self, intersection: np.ndarray) -> np.ndarray:
        return normalize(intersection - self.center)


SceneObject = Union[Sphere, Plane, Cuboid]
