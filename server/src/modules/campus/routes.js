import { Router } from 'express';

/** GET /api/campus -> { name, buildings: ['b1', ...] } (cùng hình dạng web/public/data/campus.json) */
export function campusRoutes(db) {
  const r = Router();
  r.get('/', (_req, res) => {
    const ids = db.prepare('SELECT id FROM buildings WHERE enabled = 1 ORDER BY sort_order').all().map((b) => b.id);
    res.json({ name: 'Đại học Bách khoa Hà Nội', buildings: ids });
  });
  return r;
}
