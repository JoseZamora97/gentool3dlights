from bpy.types import Operator

from .gentool.basics import Environment, Object, Material, Viewpoint, Render, Light
from .gentool.translator import ConfigIO, DatasetsGenerator, Config
from .gentool.utils import Cleaner, DataGenApplyFuncts, Message


class OperatorsEnd:
    FINISHED = "FINISHED"
    RUNNING_MODAL = "RUNNING_MODAL"
    CANCELLED = "CANCELLED"
    PASS_THROUGH = "PASS_THROUGH"
    INTERFACE = "INTERFACE"


def create_config_from_gui(properties):
    e = Environment(dimension=properties.scene_dimension)

    o = Object(
        name='sample',
        path=properties.input_model,
        material=None,
        normalize=properties.normalize
    )
    v = Viewpoint(
        kind=properties.camera_kind,
        location=properties.camera_location,
        amount=properties.amount_shoots,
        size=properties.camera_size,
        horizontal_divisions=properties.camera_h_segments,
        vertical_divisions=properties.camera_v_segments,
        max_range=properties.camera_range_location
    )
    i = Light(
        kind=properties.light_kind,
        color=properties.light_color,
        location=properties.light_location,
        max_range=properties.light_range_location,
        max_energy=properties.light_energy
    )

    styles = [Render.Style.NORMAL]

    r = Render(
        resolution_x=properties.render_resolution_x,
        resolution_y=properties.render_resolution_y,
        output_dir_path=properties.render_output_folder_path,
        styles=styles
    )

    return Config(environment=e, render=r, objects=[o], lights=[i], viewpoints=[v])


def generate_renders(config: Config, preview: bool):
    dataset_generator = DatasetsGenerator(
        config=config,
        functs=DataGenApplyFuncts(),
        preview=preview
    )

    dataset_generator.setName('Dataset-Generator')
    dataset_generator.run()  # Convert into Daemon or subprocess


class OP_OT_ClearScene(Operator):
    """
    Clear the scene.
    """
    bl_label = "Clear Scene"
    bl_idname = "object.clear_scene"

    def execute(self, _):
        Cleaner.clear_scene()
        return {OperatorsEnd.FINISHED}


class OP_OT_GenerateDataset(Operator):
    bl_label = "Generate"
    bl_idname = "object.generate_dataset"
    bl_options = {'REGISTER'}

    def execute(self, context):
        tool = context.scene.tool
        input_path = tool.input_presets_file

        config = ConfigIO.json_loads(input_path) if tool.choice_render == 'FILE' \
            else create_config_from_gui(tool)
        generate_renders(config, preview=False)

        return {OperatorsEnd.FINISHED}
