import { Router } from 'express';
import { getBuilding } from './service.js';
import { httpError } from '../../middleware/errorHandler.js';

export function buildingRoutes(db) {
  const r = Router();
  r.get('/:id', (req, res) => {
    const b = getBuilding(db, req.params.id);
    if (!b) throw httpError(404, 'Không có tòa nhà này');
    res.json(b);
  });
  // TODO (Sprint 4): PUT /:id (requireAdmin) – sửa tên, mô tả
  return r;
}
