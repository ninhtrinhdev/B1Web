import { Router } from 'express';
import { requireAdmin } from '../../middleware/requireAdmin.js';
import { requireText, optionalText } from '../../shared/validate.js';

export function feedbackRoutes(db) {
  const r = Router();
  // Ai cũng gửi được. TODO: giới hạn số lần gửi theo IP để chống spam.
  r.post('/', (req, res) => {
    const message = requireText(req.body?.message, 'nội dung', 1000);
    const name = optionalText(req.body?.name, 'tên', 100);
    const poiId = optionalText(req.body?.poiId, 'poiId', 100);
    const info = db.prepare('INSERT INTO feedback (name, message, poi_id) VALUES (?, ?, ?)').run(name, message, poiId);
    res.status(201).json({ id: Number(info.lastInsertRowid) });
  });
  r.get('/', requireAdmin, (_req, res) => {
    res.json(db.prepare('SELECT * FROM feedback ORDER BY id DESC LIMIT 200').all());
  });
  return r;
}
