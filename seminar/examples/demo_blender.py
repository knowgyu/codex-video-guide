"""Actual Blender shot: one animated data packet travels to a chip."""
import sys
from pathlib import Path
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'output/video-pipeline-v2/blender'
OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
s=bpy.context.scene
s.render.engine='BLENDER_EEVEE'
s.eevee.taa_render_samples=24
s.render.resolution_x,s.render.resolution_y=1280,720
s.render.resolution_percentage=100
s.render.fps=60
s.frame_start,s.frame_end=1,240
s.render.image_settings.file_format='PNG'
s.world.use_nodes=True
background=next(n for n in s.world.node_tree.nodes if n.type=='BACKGROUND')
background.inputs['Color'].default_value=(.035,.049,.054,1)
background.inputs['Strength'].default_value=.45
s.view_settings.view_transform='AgX'

def material(name,color,metallic=0,roughness=.4):
    m=bpy.data.materials.new(name); m.use_nodes=True
    p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Metallic'].default_value=metallic
    p.inputs['Roughness'].default_value=roughness
    return m

dark=material('Graphite',(.035,.055,.065),.42,.31)
metal=material('Anodised metal',(.18,.26,.28),.72,.3)
floor=material('Matte slate',(.06,.075,.08),.05,.7)
die=material('Ceramic',(.012,.024,.03),.3,.26)
amber=material('Signal amber',(.96,.30,.075),.1,.34)
mint=material('Signal mint',(.04,.65,.50),.12,.3)
white=material('Soft white',(.75,.84,.80),.1,.4)

def box(name,location,dimensions,mat,bevel=.04):
    bpy.ops.mesh.primitive_cube_add(size=1,location=location)
    o=bpy.context.object; o.name=name; o.dimensions=dimensions
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(mat)
    if bevel:
        mod=o.modifiers.new('Edge radius','BEVEL'); mod.width=min(bevel,min(dimensions)*.2); mod.segments=3
    return o

box('Stage',(0,0,-.16),(11,6,.3),floor,.1)
box('Board',(1.1,0,.04),(4.9,3.4,.14),dark,.12)
box('Chip substrate',(1,0,.18),(2,1.85,.18),metal,.07)
box('Chip die',(1,0,.30),(1.72,1.56,.12),die,.06)
for i in range(8):
    for side in (-1,1):
        box(f'Contact {side} {i}',(1+(i-3.5)*.24,side*.91,.21),(.095,.24,.055),amber,.01)
for i in range(6):
    box(f'Board trace {i}',(-.78,-.8+i*.32,.125),(1.8,.025,.014),metal,.004)
for i in range(5):
    box(f'Grid mark {i}',(-3.55+i*.62,0,.055),(.035,1.12,.025),metal,.005)
box('Guide rail',(-2,0,.06),(3.2,.055,.035),white,.01)

# Exact keyframes presented in the film. Blender interpolates between them.
packet=box('Token packet',(-3.25,0,.42),(.56,.56,.56),mint,.1)
packet.location=(-3.25,0,.42)
packet.keyframe_insert(data_path='location',frame=1)
packet.location=(1.0,0,.60)
packet.keyframe_insert(data_path='location',frame=180)
packet.keyframe_insert(data_path='location',frame=240)

def aim(o,target): o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
def area(name,location,power,color,size):
    d=bpy.data.lights.new(name,'AREA'); d.energy=power; d.color=color; d.shape='DISK'; d.size=size
    o=bpy.data.objects.new(name,d); s.collection.objects.link(o); o.location=location; aim(o,(0,0,0))
area('Key softbox',(-2,-4,7),950,(.78,.91,1),6)
area('Warm rim',(4,3,5),1050,(1,.67,.42),4)
area('Fill',(-5,3,4),520,(.38,1,.81),4)
camdata=bpy.data.cameras.new('Camera'); cam=bpy.data.objects.new('Camera',camdata)
s.collection.objects.link(cam); s.camera=cam; camdata.type='ORTHO'; camdata.ortho_scale=9.7
for f,loc,scale in [(1,(5,-9,7),9.7),(240,(4.1,-7.5,6),8.8)]:
    cam.location=loc; aim(cam,(-.35,0,.25)); camdata.ortho_scale=scale
    cam.keyframe_insert(data_path='location',frame=f)
    cam.keyframe_insert(data_path='rotation_euler',frame=f)
    camdata.keyframe_insert(data_path='ortho_scale',frame=f)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'token-shot.blend'))
if '--still' in sys.argv:
    s.frame_set(120); s.render.filepath=str(OUT/'test-120.png'); bpy.ops.render.render(write_still=True)
else:
    (OUT/'frames').mkdir(exist_ok=True); s.render.filepath=str(OUT/'frames/frame_'); bpy.ops.render.render(animation=True)
