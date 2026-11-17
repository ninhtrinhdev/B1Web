export const config = {
  port: Number(process.env.PORT ?? 3000),
  dbPath: process.env.DB_PATH ?? 'data/tour.db',
  adminToken: process.env.ADMIN_TOKEN ?? '',
  corsOrigin: (process.env.CORS_ORIGIN ?? 'http://localhost:5173').split(',').map((s) => s.trim()),
};
