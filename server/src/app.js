import express from 'express';
import cors from 'cors';
import { config } from './config.js';
import { errorHandler } from './middleware/errorHandler.js';
import { campusRoutes } from './modules/campus/routes.js';
import { buildingRoutes } from './modules/buildings/routes.js';
import { poiRoutes } from './modules/pois/routes.js';
import { feedbackRoutes } from './modules/feedback/routes.js';
import { statsRoutes } from './modules/stats/routes.js';

/** Tạo app nhưng KHÔNG listen – để test gọi thẳng được. */
export function createApp(db) {
  const app = express();
  app.use(cors({ origin: config.corsOrigin }));
  app.use(express.json({ limit: '100kb' }));

  app.get('/api/health', (_req, res) => res.json({ ok: true }));
  app.use('/api/campus', campusRoutes(db));
  app.use('/api/buildings', buildingRoutes(db));
  app.use('/api/pois', poiRoutes(db));
  app.use('/api/feedback', feedbackRoutes(db));
  app.use('/api/stats', statsRoutes(db));

  app.use('/api', (_req, res) => res.status(404).json({ error: 'Không có đường dẫn này' }));
  app.use(errorHandler);
  return app;
}
