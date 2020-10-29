import json
import os
import webbrowser
import csv

from threading import Thread
from typing import Dict, List

from .basics import Environment, Object, Light, Viewpoint, Render, Material


def process(o: Object) -> Dict:
    if o.material is not None:
        o.material = o.material.__dict__
    return o.__dict__


def reconstruct(o: Dict) -> Object:
    if o.get('material') is not None:
        mat = Material(**(o.get('material')))
        o.update({'material': mat})
    return Object(**o)


class Config:
    def __init__(self,
                 environment: Environment,
                 render: Render,
                 objects: List[Object],
                 lights: List[Light],
                 viewpoints: List[Viewpoint]):
        assert environment is not None, "environment cant be None!"
        assert objects != [], "objects is empty!"
        assert lights != [], "lights is empty!"
        assert viewpoints != [], "viewpoints is empty!"
        if render is not None:
            assert render.output_dir_path != "", "Output directory path not specified!"

        self.environment = environment
        self.objects = objects
        self.lights = lights
        self.viewpoints = viewpoints
        self.render = render


class ConfigIO:
    @staticmethod
    def json_dumps(instance: Config, path: str):
        config = {
            "environment": instance.environment.__dict__,
            "objects": [process(obj) for obj in instance.objects],
            "lights": [light.__dict__ for light in instance.lights] if instance.lights is not None else None,
            "viewpoints": [viewpoint.__dict__ for viewpoint in instance.viewpoints] if instance.lights is not None else None,
            "render": instance.render.__dict__ if instance.render is not None else None
        }

        if path is not None:
            with open(path, "w") as fw:
                fw.write(json.dumps(config, indent=4, sort_keys=True))

        print(config)

    @staticmethod
    def json_loads(path: str):
        with open(path, "r") as fr:
            config = json.load(fr)

        config = {
            "environment": Environment(**config.get("environment")),
            "objects": [reconstruct(o) for o in config.get("objects")],
            "lights": [Light(**li) for li in config.get("lights")] if config.get("lights") is not None else None,
            "viewpoints": [Viewpoint(**v) for v in config.get("viewpoints")] if config.get("viewpoints") is not None else None,
            "render": Render(**config.get("render")) if config.get("render") is not None else None
        }

        return Config(**config)


class DataGenFunctsInterface:

    def create_environment(self, e: Environment):
        """
        Creates an evironment for object normalicing
        :param e: the Environment
        :return:
        """
        pass

    def create_viewpoints(self, vs: List[Viewpoint], preview: bool):
        """
        Create the viewpoints of the camera
        :param vs: a list of Viewpoints objects.
        :param preview: if true, returns only 1 coord.
        :return:
        """
        pass

    def create_light(self, li: Light):
        """
        Create a light based on params of light
        :param li: Light
        :return: None
        """
        pass

    def load_object(self, o: Object, size_env: int):
        """
        Load an object into scene
        :param o: the object
        :param size_env: the size of the scene
        :return: reference to the object.
        """
        pass

    def create_camera(self):
        """
        This method creates a camera
        :return: reference to the camera.
        """
        pass

    def move_camara_to(self, camera, coords):
        """
        This move a camara to an specified coordinations
        :param camera: the camera
        :param coords: coordinates.
        :return:
        """
        pass

    def render(self, path: str, render_style: str, texture: str, object_loaded):
        """
        This method renders the image based on input render style.
        This should be one of RenderManager.Kind variables.
        :param path: to save the render
        :param render_style: Style to apply.
        :param object_loaded: Object to apply the style.
        :param texture: object texture
        :return: None
        """
        pass

    def clear_lights(self):
        """
        This method should remove all lights.
        """
        pass

    def load_material(self, object_loaded, material: Material):
        """
        This method loads all the materials.
        :param object_loaded: Object to apply the material.
        :param material: Material to apply.
        """
        pass

    def set_render_resolution(self, r: Render):
        """
        This method allows to change the render resolution.
        :param r: Render config params.
        """
        pass

    def define_texture(self, o: Object):
        """
        This method returns a texture to show in the object.
        :param o: Object config params
        """
        pass

    def get_light_params(self, light: Light):
        """
        Returns light location and color
        :param light: Light config params
        """
        pass

    def export_normalized_object(self, path):
        """
        Save the object normalized.
        :param path: output params.
        """
        pass

    def clear_objects(self):
        """
        Clear the scene objects.
        """
        pass


class DatasetsGenerator(Thread):
    def __init__(self, config: Config, functs: DataGenFunctsInterface, preview: bool):
        super(DatasetsGenerator, self).__init__()

        self.config = config
        self.functs = functs
        self.preview = preview

    def run(self):

        # self.functs.create_environment(self.config.environment)
        os.makedirs(self.config.render.output_dir_path)
        
        if self.config.render.styles != []:
            # Create the headers for saving lights in csv. 
            lights_list = [
                (f"light_{i}-x", f"light_{i}-y", f"light_{i}-z", f"light_{i}-r", f"light_{i}-g", f"light_{i}-b")
                for i, _ in enumerate(self.config.lights)
            ]
            lights_list = [item for sublist in lights_list for item in sublist]
            # Create the csv headers.
            data_csv_list = [['index', 'object', 'view-x', 'view-y', 'view-z', *lights_list, ], ]
            
            csv_path = os.path.join(self.config.render.output_dir_path, f"data.csv")
            csv_file = open(csv_path, "w", newline="")
            writer = csv.writer(csv_file)
            writer.writerows(data_csv_list)

        index = 0

        for obj in self.config.objects:

            # Load the object and store the reference.
            object_loaded = self.functs.load_object(obj, size_env=self.config.environment.dimension)
            object_loaded.select_set(True)

            # Create an object folder
            obj_path = os.path.join(self.config.render.output_dir_path, obj.name)
            os.makedirs(obj_path)

            # Export normalized object
            if obj.normalize:
                self.functs.export_normalized_object(path=os.path.join(obj_path, f"normalized.obj"))

            if self.config.render.styles == []:
                self.functs.clear_objects()
                continue

            camera = self.functs.create_camera()
            viewpoints = self.functs.create_viewpoints(self.config.viewpoints, self.preview)
            # Iterate over viewpoint
            for _, viewpoint in enumerate(viewpoints):
                # Iterate over each viewpoint coordinate
                for coords in viewpoint:
                    data_csv_list_item = [index, obj.name, *coords]
                    # Move the camera to the coordinates
                    self.functs.move_camara_to(camera, coords)
                    # Create the lights
                    for _, light in enumerate(self.config.lights):
                        li = self.functs.create_light(light)
                        li.data.energy = 1500
                        light_params = self.functs.get_light_params(li)
                        data_csv_list_item += light_params
                    # Create the folder for saving the model renders.
                    path_render_index = os.path.join(obj_path, f"{index}")
                    os.makedirs(path_render_index)
                    # Render the scene.
                    self.functs.set_render_resolution(self.config.render)
                    self.functs.render(
                        path=path_render_index,
                        render_style="",
                        texture="",
                        object_loaded=object_loaded
                    )
                    # Clear the lights
                    self.functs.clear_lights()
                    # Append the new row for csv saving.
                    writer.writerow(data_csv_list_item)
                    data_csv_list.append(data_csv_list_item)
                    # Update index
                    index += 1
                # Todo: make UI progress bar.
            self.functs.clear_objects()
        # Open output folder to see the results.
        webbrowser.open('file:///' + os.path.abspath(self.config.render.output_dir_path))
        
        if self.config.render.styles != []:
            csv_file.close()