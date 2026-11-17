/**
 * TODO (Sprint 3-4): góc nhìn có sẵn + tour tự động.
 *  - Nghe 'building:loaded' -> lấy building.cameras (Cam_Ref, Cam_Aerial... xuất từ Blender).
 *  - Thanh nút "Toàn cảnh / Sảnh / Mái đón xe" -> bus.emit('camera:flyTo', {...}).
 *  - Tour: lần lượt bay qua danh sách điểm, dừng vài giây, hiện chú thích.
 */
export class TourFeature {
  init(ctx) { this.ctx = ctx; }
  dispose() {}
}
