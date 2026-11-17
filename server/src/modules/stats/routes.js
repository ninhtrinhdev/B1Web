import { Router } from 'express';
import { requireAdmin } from '../../middleware/requireAdmin.js';

export function statsRoutes(db) {
  const r = Router();
  r.post('/visit', (_req, res) => {
    db.prepare(`INSERT INTO visits (day, count) VALUES (date('now'), 1)
                ON CONFLICT(day) DO UPDATE SET count = count + 1`).run();
    res.status(204).end();
  });
  r.get('/', requireAdmin, (_req, res) => {
    res.json(db.prepare('SELECT day, count FROM visits ORDER BY day DESC LIMIT 60').all());
  });
  return r;
}
