import { Router } from 'express';
import { requireAdmin } from '../../middleware/requireAdmin.js';

/**
 * TODO (Sprint 3-4, backend): thêm / sửa / xóa điểm thông tin – chỉ quản trị viên.
 *   POST   /api/pois        body { id, buildingId, title, text, image, position:[x,y,z] }
 *   PUT    /api/pois/:id    body như trên (trừ id)
 *   DELETE /api/pois/:id
 * Gợi ý: viết hàm truy vấn trong pois/service.js, kiểm tra đầu vào bằng shared/validate.js,
 * viết test trong tests/ trước khi nối với trang admin.
 */
export function poiRoutes(_db) {
  const r = Router();
  r.use(requireAdmin);
  r.use((_req, res) => res.status(501).json({ error: 'Chưa làm' }));
  return r;
}
