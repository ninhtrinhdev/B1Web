-- Lược đồ CSDL. Sửa ở đây rồi chạy lại `npm run seed` (seed xóa và tạo lại toàn bộ).
CREATE TABLE IF NOT EXISTS buildings (
  id           TEXT PRIMARY KEY,          -- 'b1', 'c1'...
  name         TEXT NOT NULL,
  description  TEXT,
  model        TEXT NOT NULL,             -- đường dẫn .glb trong web/public
  lat          REAL NOT NULL,
  lon          REAL NOT NULL,
  rotation_deg REAL NOT NULL DEFAULT 0,
  placeholder  TEXT,                      -- JSON [w,h,d]
  views        TEXT,                      -- JSON ["Cam_Ref", ...]
  enabled      INTEGER NOT NULL DEFAULT 1,
  sort_order   INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS pois (
  id          TEXT PRIMARY KEY,
  building_id TEXT NOT NULL REFERENCES buildings(id) ON DELETE CASCADE,
  title       TEXT NOT NULL,
  text        TEXT,
  image       TEXT,
  x REAL NOT NULL, y REAL NOT NULL, z REAL NOT NULL,  -- tọa độ cục bộ của tòa nhà (Three.js)
  updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS feedback (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  name       TEXT,
  message    TEXT NOT NULL,
  poi_id     TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS visits (
  day   TEXT PRIMARY KEY,                 -- '2026-11-02'
  count INTEGER NOT NULL DEFAULT 0
);
