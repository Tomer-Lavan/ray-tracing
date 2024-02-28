sceneJSONFormat = """
{
    "camera": [x, y, z],
    "ambient": [r, g, b],
    "lights": [
        {
            "type": "directional" | "point" | "spot",
            "intensity": [r, g, b],
            "position": [x, y, z],
            # Only for point and spot lights
            "direction": [x, y, z],  # Only for directional and spot lights
            "kc": value,  # Only for point and spot lights
            "kl": value,  # Only for point and spot lights
            "kq": value,  # Only for point and spot lights
        },
        # More lights can be added here
    ],
    "objects": [
        {
            "type": "sphere",
            "center": [x, y, z],
            "radius": value,
            "ambient": [r, g, b],
            "diffuse": [r, g, b],
            "specular": [r, g, b],
            "shininess": value,
            "reflection": value,
            "refractive_index": value,  # Optional
        },
        {
            "type": "plane",
            "normal": [x, y, z],
            "point": [x, y, z],
            "ambient": [r, g, b],
            "diffuse": [r, g, b],
            "specular": [r, g, b],
            "shininess": value,
            "reflection": value,
        },
        {
            "type": "rectangle",
            "a": [x, y, z],
            "b": [x, y, z],
            "c": [x, y, z],
            "d": [x, y, z],
            "ambient": [r, g, b],
            "diffuse": [r, g, b],
            "specular": [r, g, b],
            "shininess": value,
            "reflection": value,
        },
        {
            "type": "cuboid",
            "a": [x, y, z],
            "b": [x, y, z],
            "c": [x, y, z],
            "d": [x, y, z],
            "e": [x, y, z],
            "f": [x, y, z],
            "ambient": [r, g, b],
            "diffuse": [r, g, b],
            "specular": [r, g, b],
            "shininess": value,
            "reflection": value,
        },
        # More objects can be added here
    ]
}
"""


scene_example = """    
    sphere_a = Sphere([-0.5, 0.2, -1], 0.5)
    sphere_a.set_material([1, 0, 0], [1, 0, 0], [0.3, 0.3, 0.3], 100, 1)
    sphere_b = Sphere([-0.8, 0, -0.5], 0.3)
    sphere_b.set_material([0, 0.5, 0.5], [0, 0.4, 0.8], [0.3, 0.3, 0.6], 300, 0.3)
    plane = Plane([0, 1, 0], [0, -0.3, 0])
    plane.set_material([0.2, 0.2, 0.2], [0.2, 0.2, 0.2], [1, 1, 1], 1000, 0.5)
    background = Plane([0, 0, 1], [0, 0, -5])
    background.set_material([0.0, 0.2, 0.6], [0.5, 0.8, 0.8], [0.2, 0.2, 0.2], 1000, 0.5)

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

    # Set materials for the cuboid
    cuboid1.set_material([0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, 0.5], 100, 0.5)
    cuboid1.apply_materials_to_faces()
    cuboid2.set_material([0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, 0.5], 100, 0.5)
    cuboid2.apply_materials_to_faces()
    cuboid3.set_material([0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, 0.5], 100, 0.5)
    cuboid3.apply_materials_to_faces()
    objects = [sphere_b, plane, background, cuboid1, cuboid2, cuboid3]
    light = PointLight(intensity=np.array([1, 1, 1]), position=np.array([1, 1.5, 1]), kc=0.1, kl=0.1, kq=0.1)
    light_c = SpotLight(intensity=np.array([1, 0, 0]), position=np.array([0, 0, 1]), direction=([0, 0, 1]),
                        kc=0.1, kl=0.1, kq=0.1)
    lights = [light, light_c]
    ambient = np.array([0.14, 0.2, 0.32])
    camera = np.array([0, 0, 1])
    return camera, ambient, lights, objects"""


prompt = f"Based on the user abstract description of a 3D scene, generate a JSON for the scene configuration\
        required by the API that resemble to the description of the scene.If the description is missing scene details\
        complete them by your choice, take in consideration that lights needs to aim to objects,\
        camera needs to aim to objects and be in distance from objects and if not said otherwise \
        locate objects with space between them. The JSON response need to be clean \
        and in a format for using python json.loads(), \
        meaning no spaces and \. Answer only with a JSON.\n\nScene JSON Format: {sceneJSONFormat}\n\n\
        This is also an example for a scene with a cubid pyramid and a sphere: {scene_example}"
