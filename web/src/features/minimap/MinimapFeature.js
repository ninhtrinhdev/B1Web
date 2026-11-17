/**
 * TODO (Sprint 4): bản đồ nhỏ góc màn hình.
 *  - Cách dễ: ảnh nền chụp từ trên xuống (thêm Cam_Top trong Blender, render orthographic)
 *    + một chấm đỏ là vị trí camera.
 *  - Vị trí camera -> pixel: dùng world x/z và kích thước vùng ảnh.
 *  - Click lên bản đồ -> bus.emit('camera:flyTo', ...).
 */
export class MinimapFeature {
  init(ctx) { this.ctx = ctx; }
  update(_dt) {}
  dispose() {}
}
