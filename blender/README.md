# blender/ – làm khối

| Thư mục | Nội dung |
|---|---|
| `data/` | Dữ liệu dùng chung: `map.osm` (sau này tải lại OSM cho cả khuôn viên) |
| `shared/` | Code Python dùng chung mọi tòa nhà – để trống ở giai đoạn 1 |
| `buildings/b1/` | Riêng B1: `B1.blend`, `build_b1.py`, package `b1/`, ảnh tham chiếu `ref/` |
| `buildings/<id>/` | Tòa nhà tiếp theo, cùng cấu trúc |
| `tools/` | `export_glb.py` (xuất cho web), `render_views.py` (render kiểm tra) |
| `renders/` | Ảnh render |

Lệnh (chạy từ thư mục gốc repo, Windows và Linux như nhau):
```bash
blender -b blender/buildings/b1/B1.blend -P blender/buildings/b1/build_b1.py
blender -b blender/buildings/b1/B1.blend -P blender/tools/render_views.py -- Cam_Ref Cam_Aerial
blender -b blender/buildings/b1/B1.blend -P blender/tools/export_glb.py -- B1_Building web/public/models/buildings/b1/b1.glb
```
Ghi chú thiết kế mô hình B1: `.claude/CLAUDE.md`. Quy ước tên object (`COL_`, `POI_`, `Cam_`): `docs/CONVENTIONS.md`.

Khi bắt đầu tòa thứ hai: chuyển `osm.py, geom.py, meshkit.py, materials.py` sang `shared/`, và sửa
`osm.make_projector` dùng gốc cố định `CAMPUS_ORIGIN` thay vì tâm từng tòa (xem `docs/PLAN.md` mục 13).
