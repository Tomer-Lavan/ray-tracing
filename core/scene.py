import numpy as np
from typing import List, Tuple, Optional
from .lights import Light, SpotLight, PointLight, DirectionalLight
from .objects import Sphere, Plane, Cuboid, SceneObject
from .ray import Ray
from .utils import normalize, reflected


class Scene:
    def __init__(self, camera: np.ndarray, ambient: np.ndarray, lights: List[Light],
                 objects: List[SceneObject], screen_size: Tuple[int, int] = (256, 256), max_depth: int = 1):
        self.camera = camera
        self.ambient = ambient
        self.lights = lights
        self.objects = objects
        self.screen_size = screen_size
        self.max_depth = max_depth


def get_color(scene: Scene, ray: Ray, hit_point: np.ndarray, hit_object: SceneObject, level: int,
              max_level: int = 1) -> np.ndarray:
    color = calc_ambient_color(scene, hit_object)

    for light in scene.lights:
        sj = get_shading_factor(light, hit_point, scene.objects)
        diffuse = calc_diffuse_color(hit_point, hit_object, light)
        specular = calc_specular_color(scene, hit_point, hit_object, light)
        color = np.add(color, sj * (diffuse + specular))

    level = level + 1
    if level > max_level:
        return color

    r_ray: Ray = Ray(hit_point, reflected(
        ray.direction, hit_object.compute_normal(hit_point)))
    intersection = r_ray.nearest_intersected_object(scene.objects)
    if intersection:
        dist, obj_hit = intersection
        r_hit = calc_point(dist, r_ray, obj_hit)
        color += hit_object.reflection * \
            get_color(scene, r_ray, r_hit, obj_hit, level, max_level)

    if hit_object.refractive_index > 0:
        refracted_dir = refracted(hit_object, ray, hit_point)
        if refracted_dir is not None and len(refracted_dir):
            t_ray: Ray = Ray(hit_point, refracted_dir)
            intersection = t_ray.nearest_intersected_object(scene.objects)
            if intersection:
                dist, obj_hit = intersection
                t_hit = calc_point(dist, t_ray, obj_hit)
                color += get_color(scene, t_ray, t_hit,
                                   obj_hit, level, max_level)

    return color


def calc_ambient_color(scene: Scene, hit_object: SceneObject) -> np.ndarray:
    return hit_object.ambient * scene.ambient


def calc_diffuse_color(hit_point: np.ndarray, hit_object: SceneObject, light: Light) -> np.ndarray:
    return hit_object.diffuse * light.get_intensity(hit_point) * \
        np.dot(hit_object.compute_normal(hit_point),
               light.get_light_ray(hit_point).direction)


def calc_specular_color(scene: Scene, hit_point: np.ndarray, hit_object: SceneObject, light: Light) -> np.ndarray:
    normal = hit_object.compute_normal(hit_point)
    view_direction = normalize(scene.camera - hit_point)
    light_direction = light.get_light_ray(hit_point).direction

    reflection_direction = reflected(-light_direction, normal)

    specular_intensity = np.dot(view_direction, normalize(
        reflection_direction)) ** (hit_object.shininess/10)
    return hit_object.specular * light.get_intensity(hit_point) * specular_intensity


def calc_point(dist: float, ray: Ray, hit_object: SceneObject) -> np.ndarray:
    point = ray.origin + dist * ray.direction
    return point + hit_object.compute_normal(point) * 1e-2


def get_shading_factor(light: Light, hit_point: np.ndarray, objects: List[SceneObject]) -> float:
    light_ray = light.get_light_ray(hit_point)
    is_object_blocked = light_ray.nearest_intersected_object(objects)
    distance_to_light = light.get_distance_from_light(hit_point)
    if is_object_blocked and is_object_blocked[0] < distance_to_light:
        return 0
    return 1


def refracted(hit_object: SceneObject, ray: Ray, intersection: np.ndarray) -> Optional[np.ndarray]:
    n1 = 1.0
    n2 = hit_object.refractive_index
    normal = hit_object.compute_normal(intersection)
    incident_dir = normalize(ray.direction)
    cos_theta1 = -np.dot(normal, incident_dir)
    sin_theta1 = np.sqrt(1 - cos_theta1 ** 2)

    if sin_theta1 > n2 / n1:
        return None

    cos_theta2 = np.sqrt(1 - (n1 / n2) ** 2 * (1 - cos_theta1 ** 2))
    refraction_dir = (n1 / n2) * incident_dir + \
        (n1 / n2 * cos_theta1 - cos_theta2) * normal

    return normalize(refraction_dir)
