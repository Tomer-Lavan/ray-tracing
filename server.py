from flask import Flask, request, jsonify, send_file
from openai import OpenAI
import numpy as np
import io
import json
from dotenv import load_dotenv
import os
from matplotlib import pyplot as plt
from core import *
from renders import render_scene, fast_render_scene
from prompt import prompt
import logging
from typing import Tuple, List
from core.lights import Light
from core.objects import SceneObject

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

app = Flask(__name__)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


@app.route('/', methods=['POST'])
def get_scene():
    try:
        req = request.json
        logging.info("Asking GPT for scene...")
        gpt_response = ask_gpt4_for_scene(req['message'])
        scene_data = json.loads(gpt_response)
        logging.info("Parsing GPT Response...")
        camera, ambient, lights, objects = parse_scene_data(scene_data)
        logging.info("Parsing Success")
        logging.info("Rendering image...")
        image = render_scene(camera, ambient, lights, objects, (256, 256), 3)
        logging.info("Rendering Success")
        return send_image(image)
    except Exception as e:
        logging.error(f"Error in get_scene: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/fast', methods=['POST'])
def get_scene_fast():
    try:
        req = request.json
        logging.info("Asking GPT for Scene...")
        gpt_response = ask_gpt4_for_scene(req['message'])
        scene_data = json.loads(gpt_response)
        logging.info("Parsing GPT Response...")
        camera, ambient, lights, objects = parse_scene_data(scene_data)
        logging.info("Parsing Success")
        logging.info("Rendering image...")
        image = fast_render_scene(
            camera, ambient, lights, objects, (256, 256), 3)
        logging.info("Rendering Success")
        return send_image(image)
    except Exception as e:
        logging.error(f"Error in get_scene_fast: {e}")
        return jsonify({"error": str(e)}), 500


def ask_gpt4_for_scene(description: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt},
                      {"role": "user", "content": f"Description: {description}"}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error in ask_gpt4_for_scene: {e}")
        raise


def parse_scene_data(scene_data: dict) -> Tuple[np.ndarray, np.ndarray, List[Light], List[SceneObject]]:
    try:
        camera = np.array(scene_data['camera'])
        ambient = np.array(scene_data['ambient'])
        lights = []
        for light_data in scene_data['lights']:
            if light_data['type'] == 'directional':
                lights.append(DirectionalLight(
                    np.array(light_data['intensity']), np.array(light_data['direction'])))
            elif light_data['type'] == 'point':
                lights.append(PointLight(np.array(light_data['intensity']), np.array(
                    light_data['position']), light_data['kc'], light_data['kl'], light_data['kq']))
            elif light_data['type'] == 'spot':
                lights.append(SpotLight(np.array(light_data['intensity']), np.array(light_data['position']), np.array(
                    light_data['direction']), light_data['kc'], light_data['kl'], light_data['kq']))

        objects = []
        for obj_data in scene_data['objects']:
            if obj_data['type'] == 'sphere':
                obj = Sphere(np.array(obj_data['center']), obj_data['radius'])
            elif obj_data['type'] == 'plane':
                obj = Plane(np.array(obj_data['normal']),
                            np.array(obj_data['point']))
            elif obj_data['type'] == 'rectangle':
                obj = Rectangle(np.array(obj_data['a']), np.array(
                    obj_data['b']), np.array(obj_data['c']), np.array(obj_data['d']))
            elif obj_data['type'] == 'cuboid':
                obj = Cuboid(np.array(obj_data['a']), np.array(obj_data['b']), np.array(
                    obj_data['c']), np.array(obj_data['d']), np.array(obj_data['e']), np.array(obj_data['f']))
            obj.set_material(np.array(obj_data['ambient']), np.array(obj_data['diffuse']), np.array(
                obj_data['specular']), obj_data['shininess'], obj_data['reflection'], obj_data.get('refractive_index', 0))
            if obj_data['type'] == 'cuboid':
                obj.apply_materials_to_faces()
            objects.append(obj)

        return camera, ambient, lights, objects
    except Exception as e:
        logging.error(f"Error in parse_scene_data: {e}")
        raise


def send_image(image):
    try:
        bytes_io = io.BytesIO()
        plt.imsave(bytes_io, image, format='png')
        bytes_io.seek(0)
        return send_file(bytes_io, mimetype='image/png')
    except Exception as e:
        logging.error(f"Error in send_image: {e}")
        raise


if __name__ == '__main__':
    app.run(debug=True)
