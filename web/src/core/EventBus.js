/**
 * Bảng tin chung: feature A "emit", feature B "on" – hai bên không cần biết nhau.
 * Danh sách sự kiện đang dùng (cập nhật khi thêm):
 *   load:progress {loaded,total}   load:done
 *   world:ready  world            building:loaded  building
 *   poi:click   poi              camera:flyTo {position,target}
 *   nav:mode    'orbit'|'walk'
 *   api:offline                    (backend không phản hồi, đang dùng dữ liệu tĩnh)
 */
export class EventBus {
  constructor() { this.map = new Map(); }
  on(name, fn) {
    if (!this.map.has(name)) this.map.set(name, new Set());
    this.map.get(name).add(fn);
    return () => this.map.get(name).delete(fn); // gọi hàm trả về để hủy đăng ký
  }
  emit(name, payload) { this.map.get(name)?.forEach((fn) => fn(payload)); }
}
