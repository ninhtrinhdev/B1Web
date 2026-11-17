import { config } from './config.js';
import { openDb } from './db/connection.js';
import { createApp } from './app.js';

const db = openDb(config.dbPath);
createApp(db).listen(config.port, () => {
  console.log(`API chạy ở http://localhost:${config.port}/api/health`);
  if (!config.adminToken) console.warn('Chưa đặt ADMIN_TOKEN trong .env – các API quản trị sẽ luôn bị từ chối.');
});
