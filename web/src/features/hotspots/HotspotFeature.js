/**
 * TODO (Sprint 3): điểm thông tin (POI) trên model.
 *  - Nghe 'building:loaded' -> đọc building.data.pois (+ building.poiAnchors từ Blender).
 *  - Tạo nút HTML cho mỗi POI; mỗi khung hình chiếu vị trí 3D -> màn hình (Vector3.project),
 *    hoặc dùng CSS2DRenderer trong three/addons.
 *  - Ẩn nút khi ở sau camera / quá xa.
 *  - Click -> bus.emit('poi:click', poi).
 */
export class HotspotFeature {
  init(ctx) { this.ctx = ctx; }
  update(_dt) {}
  dispose() {}
}
