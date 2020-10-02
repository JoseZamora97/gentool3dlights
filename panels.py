from bpy.types import Panel

from .operators import OP_OT_ClearScene, OP_OT_GenerateDataset


class ToolPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GenTool3DLights"


class PL_PT_root(ToolPanel, Panel):
    """
    Root holder of the Addon GUI.
    """
    bl_label = "3D Multiview Lights Generator"
    bl_idname = "PL_PT_root"

    @classmethod
    def poll(cls, _):
        return True

    def draw(self, _):
        pass


class PL_PT_gui(ToolPanel, Panel):
    """
    GUI Configurator holder.
    """
    bl_label = "Sampler (vBeta)"
    bl_idname = "PL_PT_gui"
    bl_parent_id = "PL_PT_root"

    def draw(self, context):
        layout = self.layout
        tool = context.scene.tool

        # Scene Options
        layout.separator()
        layout.label(text="Scene option:")
        row = layout.row()
        row.prop(tool, "scene_dimension")

        # Model Options
        layout.separator()
        layout.label(text="Model options:")
        layout.prop(tool, "input_model")
        layout.prop(tool, "normalize")

        # Light options
        layout.separator()
        layout.label(text="Light options:")
        layout.prop(tool, 'light_kind')
        layout.prop(tool, 'light_color')
        layout.prop(tool, 'light_location')
        layout.prop(tool, 'light_range_location')
        layout.prop(tool, 'light_energy')

        # Camera options
        layout.separator()
        layout.label(text="Camera options:")
        row = layout.row()
        row.prop(tool, 'camera_kind')
        row.prop(tool, 'amount_shoots')
        layout.prop(tool, 'camera_location')
        layout.prop(tool, 'camera_range_location')
        row = layout.row()
        row.prop(tool, 'camera_size')
        row.prop(tool, 'camera_h_segments')
        row.prop(tool, 'camera_v_segments')

        # Render Manager options
        layout.separator()
        layout.label(text="Render options:")
        layout.prop(tool, 'render_resolution_x')
        layout.prop(tool, 'render_resolution_y')
        layout.prop(tool, 'render_output_folder_path')

        layout.separator()
        layout.operator(OP_OT_ClearScene.bl_idname)


class PL_PT_file(ToolPanel, Panel):
    """
    Generator settings holder.
    """
    bl_label = "Import .json config"
    bl_idname = "PL_PT_file"
    bl_parent_id = "PL_PT_root"

    def draw(self, context):
        layout = self.layout
        tool = context.scene.tool
        layout.prop(tool, "input_presets_file")


class PL_PT_generator(ToolPanel, Panel):
    """
    Generator settings holder.
    """
    bl_label = "Generator"
    bl_idname = "PL_PT_generator"
    bl_parent_id = "PL_PT_root"

    def draw(self, context):
        layout = self.layout
        tool = context.scene.tool

        layout.prop(tool, "choice_render")
        layout.separator()
        layout.operator(OP_OT_GenerateDataset.bl_idname)
