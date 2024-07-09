import bpy
import bmesh
import random

print("\n\n\n\n\n\n\n\n\n")

bl_info = {
    "name" : "ColorPainter",
    "description" : "Randomized collor apply",
    "author" : "Drwalin",
    "version" : (0, 0, 1),
    "blender" : (4, 1, 1),
    "location" : "View3D",
    "warning" : "",
    "support" : "COMMUNITY",
    "doc_url" : "",
    "category" : "3D View"
}

import bpy
from bpy.types import Operator
from bpy.types import Panel

class TLA_OT_operator(Operator):
    """ tooltip goes here """
    bl_idname = "color_painter.random"
    bl_label = "I'm a Skeleton Operator"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "EDIT_MESH"


    def GetRandomColor(self, context):
        ts = context.tool_settings;
        ups = ts.unified_paint_settings;
        ptr = ups if ups.use_unified_color else ts.image_paint.brush;
        c = ptr.color.copy();
        c.h += context.scene.HueVariation * (random.random()*2.0 - 1.0);
        c.s += context.scene.SaturationVariation * (random.random()*2.0 - 1.0);
        c.v += context.scene.LuminosityVariation * (random.random()*2.0 - 1.0);
        return (c.r, c.g, c.b, 1);

    def execute(self, context):
        if context.mode != "EDIT_MESH":
            return {'FINISHED'}
        
        for obj in bpy.context.selected_editable_objects:
            #bm = bmesh.new();
            #bm.from_mesh(obj.data);
            bm = bmesh.from_edit_mesh(obj.data);
            
            print("Mesh next: ", obj)
            
            color = None;
            for i,j in enumerate(bm.faces.layers.color):
                if j.name == 'Color':
                    color = j;
            if color == None:
                color = bm.faces.layers.color.new('Color')
            
            for j,f in enumerate(bm.faces):
                if f.select:
                    f[color] = self.GetRandomColor(context)
            
            bmesh.update_edit_mesh(bpy.context.object.data)
     
            bm.free()
        return {'FINISHED'}

class TLA_PT_sidebar(Panel):
    """Display test button"""
    bl_label = "color_painter.ui"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ColorPainter"

    def draw(self, context):
        col = self.layout.column(align=True)

        row = col.row(align=True)

        ts = context.tool_settings
        ups = ts.unified_paint_settings
        ptr = ups if ups.use_unified_color else ts.image_paint.brush
        col.box().prop(ptr, 'color')

        col.prop(context.scene, "HueVariation")
        col.prop(context.scene, "SaturationVariation")
        col.prop(context.scene, "LuminosityVariation")
        
        col.box()
        
        col.box().operator(TLA_OT_operator.bl_idname, text="Apply random colors")

 
classes = [
    TLA_OT_operator,
    TLA_PT_sidebar,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.HueVariation = bpy.props.FloatProperty(
        name='HueVariation',
        default=0.05,
        min=0.0,
        max=1.0
    )
    bpy.types.Scene.SaturationVariation = bpy.props.FloatProperty(
        name='SaturationVariation',
        default=0.05,
        min=0.0,
        max=1.0
    )
    bpy.types.Scene.LuminosityVariation = bpy.props.FloatProperty(
        name='LuminosityVariation',
        default=0.05,
        min=0.0,
        max=1.0
    )
        
def unregister():
    del bpy.types.Scene.my_float
    del bpy.types.Scene.my_bool
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == '__main__':
    register()

