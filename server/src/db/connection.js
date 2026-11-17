import { DatabaseSync } from 'node:sqlite';
import { readFileSync, mkdirSync } from 'node:fs';
import { dirname } from 'node:path';

const SCHEMA = new URL('./schema.sql', import.meta.url);

/** Mở (hoặc tạo) file SQLite và bảo đảm đủ bảng. ':memory:' dùng cho test. */
export function openDb(path) {
  if (path !== ':memory:') mkdirSync(dirname(path), { recursive: true });
  const db = new DatabaseSync(path);
  db.exec('PRAGMA foreign_keys = ON;');
  db.exec(readFileSync(SCHEMA, 'utf8'));
  return db;
}
