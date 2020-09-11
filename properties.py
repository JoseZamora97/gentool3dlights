from bpy.props import (
    StringProperty,
    BoolProperty,
    IntProperty,
    FloatProperty,
    FloatVectorProperty,
    IntVectorProperty,
    EnumProperty
)
from bpy.types import PropertyGroup

from .gentool.basics import Material, Light, Viewpoint

class Properties(PropertyGroup):
    """
    Property group of the addon. Contanains all GUI controllers.
    """
    # Scene panel properties:
    scene_dimension: IntProperty(
        name="Scene dimension",
        description="Scene is a 3D cube where the objects will apears. This can be used to normalize objects",
        default=1,
        min=1
    )

    # Model properties:
    input_model: StringProperty(
        name="Input file",
        description="Choose a 3D model to import",
        default="*.obj",
        maxlen=1024,
        subtype='FILE_PATH'
    )

    normalize: BoolProperty(
        name="Normalize",
        description="If checked, this will scale the model to fit into the scene cube, and will translate the object into center",
        default=True,
    )

    # Light properties:
    light_kind: EnumProperty(
        name="Kind",
        description="Choose the kind of light for the generation",
        items=[
            (Light.Kind.STATIC_LIGHT, 'Static Light',
             """Generate a static light at location specified in "Light location" property and with the color specified in "Light color" property""",
             '', 0),
            (Light.Kind.DYNAMIC_LIGHT, 'Dynamic Light',
             """Generate a dynamic light with random location but with the specified color in "Light color" property""",
             '', 1),
            (Light.Kind.RAINBOW_STATIC_LIGHT, 'Rainbow Static Light',
             """Generate a static light at location specified in "Light location" property and with random color""", '',
             2),
            (Light.Kind.RAINBOW_DYNAMIC_LIGHT, 'Rainbow Dynamic Light',
             """Generate a dynamic light at random location and with random color""", '', 3)
        ],
        default=Light.Kind.DYNAMIC_LIGHT
    )

    light_color: IntVectorProperty(
        name="Fixed color",
        description="Specify a fixed light RGB color, with values from 0 to 255.",
        default=[0, 0, 0],
        min=0,
        max=255
    )

    light_range_location: FloatProperty(
        name="Range Location",
        description="""Max range for the generation of the location of light source. For example, if you choose 5 the light coordinates will be generated from -5 to 5""",
        default=5,
        min=0
    )

    light_energy: IntProperty(
        name="Max energy",
        description="""Max range for the generation of the energy of light source. For example, if you choose 5 the light energy will be generated from 0 to 5""",
        default=5,
        min=0
    )

    light_location: FloatVectorProperty(
        name="Location",
        description="""Specify fixed light location. If "Fixed Location" is not checked this will not apply""",
        default=[0.0, 0.0, 0.0],
        min=0.0
    )

    # Camera settings:
    camera_kind: EnumProperty(
        name="Kind",
        description="Choose the kind of light for the generation",
        items=[
            (Viewpoint.Kind.STATIC_CAMERA, 'Static', 'Generate the camera in a fixed location', '', 0),
            (Viewpoint.Kind.DYNAMIC_CAMERA, 'Dynamic', 'Generate the camera at random location', '', 1),
            (Viewpoint.Kind.OBJECT_PATH, 'Spheric path',
             'Generate the camera to follow the vertices produced in a sphere', '', 2)
        ],
        default=Viewpoint.Kind.DYNAMIC_CAMERA
    )

    camera_location: FloatVectorProperty(
        name="Camera Location",
        description="""Specify fixed camera location.""",
        default=[0.0, 0.0, 0.0],
        min=0.0
    )

    camera_range_location: FloatProperty(
        name="Range Location",
        description="""Max range for the generation of the location of the camera. For example, if you choose 5 the camera coordinates will be generated from -5 to 5""",
        default=5,
        min=0
    )

    amount_shoots: IntProperty(
        name="Shoots",
        description="""Amount of shoots to make for rendering. 100 means this camara will render
        100 images for each style selected in 'RenderManager Settings'. In case "Spheric path"
        was selected, this number will be equal the "Vertical Segments" times the 
        "Horizontal Segments" """,
        default=100,
        min=0,
    )

    camera_size: FloatProperty(
        name="Sphere size",
        description="""Set a value to the diameter in case "Spheric path" was selected""",
        default=2,
        min=0
    )

    camera_v_segments: IntProperty(
        name="Vertical segments",
        description="Amount of vertical divisions of the sphere",
        default=10,
        min=0
    )

    camera_h_segments: IntProperty(
        name="Horizontal segments",
        description="Amount of horizontal divisions of the sphere",
        default=10,
        min=0
    )

    render_resolution_x: IntProperty(
        name="Width",
        description="Sets the width of the output images in pixels",
        default=128,
        min=0
    )

    render_resolution_y: IntProperty(
        name="Height",
        description="Sets the height of the output images in pixels",
        default=128,
        min=0
    )

    render_output_folder_path: StringProperty(
        name="Output directory",
        description="Choose a directory where output will appears",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
    )

    # Json file input
    input_presets_file: StringProperty(
        name="Input config file",
        description="Configuration file for scene creation and customization",
        default="*.json",
        maxlen=1024,
        subtype='FILE_PATH'
    )

    # Generator panel settings
    choice_render: EnumProperty(
        name="Config from",
        description="Choose the generator input, if you choose GUI the generator will take the established properties, if you choose FILE, the generator will take the properties of a file in *.json format",
        items=[
            ('GUI', 'Gui', '', '', 0),
            ('FILE', 'File', '', '', 1)
        ],
        default='GUI'
    )