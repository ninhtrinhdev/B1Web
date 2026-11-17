import { config } from '../config.js';

/** Chặn thao tác sửa dữ liệu nếu thiếu header Authorization: Bearer <ADMIN_TOKEN>. */
export function requireAdmin(req, res, next) {
  const token = (req.get('authorization') ?? '').replace(/^Bearer\s+/i, '');
  if (!config.adminToken || token !== config.adminToken) {
    return res.status(401).json({ error: 'Cần quyền quản trị' });
  }
  next();
}
