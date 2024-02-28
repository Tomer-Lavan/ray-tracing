# core/__init__.py
from .utils import normalize, reflected
from .lights import LightSource, DirectionalLight, PointLight, SpotLight
from .objects import Object3D, Plane, Rectangle, Cuboid, Sphere
from .ray import Ray
from .scene import Scene, get_color
