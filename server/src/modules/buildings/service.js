/** Đổi dòng CSDL thành đúng hình dạng JSON frontend đang đọc (web/public/data/buildings/b1.json). */
export function getBuilding(db, id) {
  const b = db.prepare('SELECT * FROM buildings WHERE id = ?').get(id);
  if (!b) return null;
  const pois = db.prepare('SELECT * FROM pois WHERE building_id = ? ORDER BY id').all(id);
  return {
    id: b.id,
    name: b.name,
    model: b.model,
    origin: { lat: b.lat, lon: b.lon },
    rotationDeg: b.rotation_deg,
    placeholder: { size: JSON.parse(b.placeholder ?? 'null') },
    description: b.description,
    pois: pois.map((p) => ({ id: p.id, title: p.title, position: [p.x, p.y, p.z], text: p.text, image: p.image })),
    views: JSON.parse(b.views ?? '[]'),
  };
}
