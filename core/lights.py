import numpy as np
from .utils import normalize
from .ray import Ray
from typing import Union, List


class LightSource:
    def __init__(self, intensity: float):
        self.intensity = intensity


class DirectionalLight(LightSource):
    def __init__(self, intensity: float, direction: np.ndarray):
        super().__init__(intensity)
        self.direction = normalize(direction)

    def get_light_ray(self, intersection_point: np.ndarray) -> Ray:
        return Ray(intersection_point, self.direction)

    def get_distance_from_light(self):
        return np.inf

    def get_intensity(self):
        return self.intensity


class PointLight(LightSource):
    def __init__(self, intensity: float, position: List[float], kc: float, kl: float, kq: float):
        super().__init__(intensity)
        self.position = np.array(position)
        self.kc = kc
        self.kl = kl
        self.kq = kq

    def get_light_ray(self, intersection: np.ndarray) -> Ray:
        return Ray(intersection, normalize(self.position - intersection))

    def get_distance_from_light(self, intersection: np.ndarray) -> float:
        return np.linalg.norm(intersection - self.position)

    def get_intensity(self, intersection: np.ndarray) -> float:
        d = self.get_distance_from_light(intersection)
        return self.intensity / (self.kc + self.kl*d + self.kq * (d**2))


class SpotLight(LightSource):
    def __init__(self, intensity: float, position: np.ndarray, direction: np.ndarray, kc: float, kl: float, kq: float):
        super().__init__(intensity)
        self.position = position
        self.direction = normalize(direction)
        self.kc = kc
        self.kl = kl
        self.kq = kq

    def get_light_ray(self, intersection: np.ndarray) -> Ray:
        return Ray(intersection, normalize(self.position - intersection))

    def get_distance_from_light(self, intersection: np.ndarray) -> float:
        return np.linalg.norm(intersection - self.position)

    def get_intensity(self, intersection: np.ndarray) -> float:
        light_direction = normalize(self.position - intersection)
        cos_angle = np.dot(light_direction, self.direction)
        intensity = self.intensity * cos_angle / self.calc_fatt(intersection)
        return intensity

    def calc_fatt(self, intersection: np.ndarray) -> float:
        d = self.get_distance_from_light(intersection)
        return self.kc + self.kl*d + self.kq * (d**2)


Light = Union[PointLight, SpotLight, DirectionalLight]
