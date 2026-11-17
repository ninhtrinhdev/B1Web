// Nạp dữ liệu mẫu từ web/public/data vào CSDL. Lúc đầu nguồn dữ liệu vẫn là các file JSON
// để frontend chạy được khi chưa có backend. Có trang quản trị rồi thì sửa qua API.
import { readFileSync, existsSync, rmSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { join, dirname } from 'node:path';
import { config } from '../config.js';
import { openDb } from './connection.js';

const DATA = join(dirname(fileURLToPath(import.meta.url)), '..', '..', '..', 'web', 'public', 'data');
const read = (p) => JSON.parse(readFileSync(join(DATA, p), 'utf8'));

export function seed(db) {
  db.exec('DELETE FROM pois; DELETE FROM buildings;');
  const insB = db.prepare(`INSERT INTO buildings (id, name, description, model, lat, lon, rotation_deg, placeholder, views, sort_order)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`);
  const insP = db.prepare('INSERT INTO pois (id, building_id, title, text, image, x, y, z) VALUES (?, ?, ?, ?, ?, ?, ?, ?)');
  read('campus.json').buildings.forEach((id, i) => {
    const b = read(`buildings/${id}.json`);
    insB.run(b.id, b.name, b.description ?? null, b.model, b.origin.lat, b.origin.lon, b.rotationDeg ?? 0,
      JSON.stringify(b.placeholder?.size ?? null), JSON.stringify(b.views ?? []), i);
    for (const p of b.pois ?? []) insP.run(p.id, b.id, p.title, p.text ?? null, p.image ?? null, ...p.position);
  });
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  if (existsSync(config.dbPath)) rmSync(config.dbPath);
  const db = openDb(config.dbPath);
  seed(db);
  const n = db.prepare('SELECT COUNT(*) AS n FROM buildings').get().n;
  console.log(`Đã tạo ${config.dbPath}: ${n} tòa nhà.`);
}
