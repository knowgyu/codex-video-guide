"""Project the actual Blender packet centre through its animated camera."""
import json
from pathlib import Path
import bpy
from bpy_extras.object_utils import world_to_camera_view

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'output/video-pipeline-v2/blender'
s=bpy.context.scene
packet=bpy.data.objects['Token packet']
rows=[]
for frame in range(1,241):
    s.frame_set(frame); bpy.context.view_layer.update()
    position=packet.matrix_world.translation.copy()
    p=world_to_camera_view(s,s.camera,position)
    rows.append({'frame':frame,'seconds':(frame-1)/60,'world':[round(v,6) for v in position],
                 'pixel':[round(p.x*1280,3),round((1-p.y)*720,3)],'depth':round(p.z,6)})
(OUT/'markers.json').write_text(json.dumps({'width':1280,'height':720,'fps':60,'samples':rows},indent=2)+'\n',encoding='utf-8')
print('EXPORTED_MARKERS',len(rows))
