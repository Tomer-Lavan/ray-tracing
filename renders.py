from core.scene import *
import matplotlib.pyplot as plt
from multiprocessing import Pool


def render_pixel(args: Tuple[int, int, np.ndarray, Tuple[float, float], np.ndarray, List[SceneObject], Scene]) -> Tuple[int, int, np.ndarray]:
    i, j, pixel, screen, camera, objects, scene = args

    origin = camera
    direction = normalize(pixel - origin)
    ray = Ray(origin, direction)
    color = np.zeros(3)

    intersection = ray.nearest_intersected_object(objects)
    if intersection and intersection[1]:
        dist, hit_object = intersection
        hit_point = calc_point(dist, ray, hit_object)
        color = get_color(scene, ray, hit_point,
                          hit_object, 1, scene.max_depth)

    return i, j, np.clip(color, 0, 1)


def fast_render_scene(camera: np.ndarray, ambient: np.ndarray, lights: List[Light], objects: List[SceneObject],
                      screen_size: Tuple[int, int], max_depth: int):
    width, height = screen_size
    ratio = float(width) / height
    screen = (-1, 1 / ratio, 1, -1 / ratio)
    scene = Scene(camera, ambient, lights, objects, screen_size, max_depth)

    image = np.zeros((height, width, 3))
    args = []

    for i, y in enumerate(np.linspace(screen[1], screen[3], height)):
        for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
            pixel = np.array([x, y, 0])
            args.append((i, j, pixel, screen, camera, objects, scene))

    with Pool() as pool:
        results = pool.map(render_pixel, args)

    for result in results:
        i, j, color = result
        image[i, j] = color

    return image


def render_scene(camera: np.ndarray, ambient: np.ndarray, lights: List[Light], objects: List[SceneObject],
                 screen_size: Tuple[int, int], max_depth: int):
    width, height = screen_size
    ratio = float(width) / height
    screen = (-1, 1 / ratio, 1, -1 / ratio)
    scene = Scene(camera, ambient, lights, objects, screen_size, max_depth)

    image = np.zeros((height, width, 3))

    for i, y in enumerate(np.linspace(screen[1], screen[3], height)):
        for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
            # screen is on origin
            pixel = np.array([x, y, 0])
            origin = camera
            direction = normalize(pixel - origin)
            ray = Ray(origin, direction)
            color = np.zeros(3)

            intersection = ray.nearest_intersected_object(objects)
            if intersection:
                dist, hit_object = intersection
                hit_point = calc_point(dist, ray, hit_object)
                color = get_color(scene, ray, hit_point,
                                  hit_object, 1, scene.max_depth)

            # We clip the values between 0 and 1 so all pixel values will make sense.
            image[i, j] = np.clip(color, 0, 1)

    return image


def get_example_scene() -> Scene:
    sphere_a = Sphere([-0.5, 0.2, -1], 0.5)
    sphere_a.set_material([1, 0, 0], [1, 0, 0], [0.3, 0.3, 0.3], 100, 1)
    sphere_b = Sphere([-0.8, 0, -0.5], 0.3)
    sphere_b.set_material([0, 0.5, 0.5], [0, 0.4, 0.8],
                          [0.3, 0.3, 0.6], 300, 0.3)
    plane = Plane([0, 1, 0], [0, -0.3, 0])
    plane.set_material([0.2, 0.2, 0.2], [0.2, 0.2, 0.2], [1, 1, 1], 1000, 0.5)
    background = Plane([0, 0, 1], [0, 0, -5])
    background.set_material([0.0, 0.2, 0.6], [0.5, 0.8, 0.8], [
                            0.2, 0.2, 0.2], 1000, 0.5)

    cuboid1 = Cuboid(
        [0, 1.25, -3],
        [0, -0.5, -3],
        [1, -0.5, -2.5],
        [1, 1.25, -2.5],
        [2, -0.5, -3.5],
        [2, 1.25, -3.5]
    )
    cuboid2 = Cuboid(
        [-1, 1.25, -3],
        [-1, -0.5, -3],
        [0, -0.5, -2.5],
        [0, 1.25, -2.5],
        [2, -0.5, -3.5],
        [2, 1.25, -3.5]
    )
    cuboid3 = Cuboid(
        [-0.3, 2, -2.9],
        [-0.3, 1.25, -2.9],
        [0.7, 1.25, -2.5],
        [0.7, 2, -2.5],
        [1.2, 1.25, -3.3],
        [1.2, 2, -3.3]
    )

    cuboid1.set_material([0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [
                         0.5, 0.5, 0.5], 100, 0.5)
    cuboid1.apply_materials_to_faces()
    cuboid2.set_material([0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [
                         0.5, 0.5, 0.5], 100, 0.5)
    cuboid2.apply_materials_to_faces()
    cuboid3.set_material([0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [
                         0.5, 0.5, 0.5], 100, 0.5)
    cuboid3.apply_materials_to_faces()
    objects = [sphere_b, plane, background, cuboid1, cuboid2, cuboid3]
    light = PointLight(intensity=np.array([1, 1, 1]), position=np.array(
        [1, 1.5, 1]), kc=0.1, kl=0.1, kq=0.1)
    light_c = SpotLight(intensity=np.array([1, 0, 0]), position=np.array([0, 0, 1]), direction=([0, 0, 1]),
                        kc=0.1, kl=0.1, kq=0.1)
    lights = [light, light_c]
    ambient = np.array([0.14, 0.2, 0.32])
    camera = np.array([0, 0, 1])
    return camera, ambient, lights, objects


if __name__ == '__main__':
    camera, ambient, lights, objects = get_example_scene()

    im = fast_render_scene(camera, ambient, lights, objects, (256, 256), 3)
    plt.imshow(im)
    plt.imsave('scene4.png', im)
