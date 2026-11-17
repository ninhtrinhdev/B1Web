"""Xuất một tòa nhà ra .glb cho web.

    blender -b blender/buildings/b1/B1.blend -P blender/tools/export_glb.py -- B1_Building web/public/models/buildings/b1/b1.glb

Xuất mọi object hiển thị trong collection chỉ định (gồm collection con), kèm camera Cam_*,
empty POI_* và mesh va chạm COL_*.
LƯU Ý: chưa chạy thử trên máy nhóm – mở kết quả bằng https://gltf-viewer.donmccurdy.com để kiểm tra.
- Node Noise (grime) trong materials.py KHÔNG sang được glTF: web chỉ nhận Base Color / Roughness /
  Metallic / Emission / Clearcoat. Muốn giữ vết bẩn thì bake ra texture (việc giai đoạn sau).
"""
import os
import sys

import bpy

args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
COLL = args[0] if len(args) > 0 else 'B1_Building'
OUT = os.path.abspath(args[1] if len(args) > 1 else 'b1.glb')
EXTRA_PREFIX = ('Cam_', 'POI_', 'COL_')

coll = bpy.data.collections.get(COLL)
if coll is None:
    raise SystemExit(f'Không thấy collection {COLL}')

for o in bpy.context.selected_objects:
    o.select_set(False)
picked = [o for o in coll.all_objects if not o.hide_render]
picked += [o for o in bpy.data.objects if o.name.startswith(EXTRA_PREFIX) and o not in picked]
for o in picked:
    o.hide_set(False)
    o.select_set(True)
print(f'Xuất {len(picked)} object từ {COLL} -> {OUT}')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
bpy.ops.export_scene.gltf(
    filepath=OUT,
    export_format='GLB',
    use_selection=True,
    export_yup=True,            # Blender Z-up -> glTF Y-up
    export_apply=True,          # áp dụng modifier
    export_cameras=True,
    export_lights=False,        # ánh sáng dựng lại trên web
    export_extras=True,         # custom property -> userData (dùng cho POI)
    export_draco_mesh_compression_enable=True,
    export_draco_mesh_compression_level=6,
)
print('Xong.')
