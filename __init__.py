import bpy


from .operators import OP_OT_ClearScene
from .operators import OP_OT_GenerateDataset
from .panels import PL_PT_file
from .panels import PL_PT_generator
from .panels import PL_PT_gui
from .panels import PL_PT_root
from .properties import Properties


bl_info = {
    "name": "3D Multiview Lights Datasets Generation Tool",
    "author": "Jose Zamora",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Machine Learning Datasets"
}

classes = (
    Properties,
    OP_OT_ClearScene,
    PL_PT_root,
    PL_PT_gui,
    PL_PT_file,
    PL_PT_generator,
    OP_OT_GenerateDataset,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.tool = bpy.props.PointerProperty(type=Properties)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.tool


if __name__ == "__main__":
    register()
