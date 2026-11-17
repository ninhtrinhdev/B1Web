/**
 * Lớp DUY NHẤT trong frontend gọi backend. Feature không tự gọi fetch tới server.
 * Nếu backend không chạy (hoặc bản deploy chỉ có frontend), tự dùng JSON tĩnh trong public/data
 * -> frontend làm việc được ngay từ Sprint 1, không phải chờ backend.
 * Hợp đồng API: docs/API.md
 */
export class ApiClient {
  constructor(config) {
    this.base = config.API_URL;
    this.staticBase = config.STATIC_DATA_URL;
    this.online = true;
  }

  async _get(path, staticPath) {
    if (this.online) {
      try {
        const res = await fetch(`${this.base}${path}`);
        if (res.ok) return await res.json();
        throw new Error(`HTTP ${res.status}`);
      } catch (err) {
        console.warn(`[api] ${path} lỗi (${err.message}) -> dùng dữ liệu tĩnh`);
        this.online = false;
      }
    }
    const res = await fetch(`${this.staticBase}${staticPath}`);
    if (!res.ok) throw new Error(`Không tải được ${staticPath}`);
    return res.json();
  }

  getCampus() { return this._get('/campus', '/campus.json'); }
  getBuilding(id) { return this._get(`/buildings/${id}`, `/buildings/${id}.json`); }

  async _post(path, body) {
    if (!this.online) return { ok: false, offline: true };
    const res = await fetch(`${this.base}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    return { ok: res.ok, data: await res.json().catch(() => null) };
  }

  sendFeedback({ name, message, poiId }) { return this._post('/feedback', { name, message, poiId }); }
  trackVisit() { return this._post('/stats/visit', {}).catch(() => {}); }
}
