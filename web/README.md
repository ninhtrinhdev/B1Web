# web/ – frontend

```
index.html              trang tham quan
admin/                  trang quản trị nội dung (mở /admin/ khi chạy dev)
public/                 file tĩnh, phục vụ nguyên trạng
  models/buildings/<id>/  model .glb của từng tòa nhà
  models/props/           cây, ghế, xe... dùng lại nhiều lần
  textures/  hdri/        ảnh vật liệu, ảnh bầu trời
  images/pois/            ảnh minh họa cho bảng thông tin
  data/                   JSON tĩnh: dữ liệu mẫu + dự phòng khi backend tắt
src/
  main.js                 điểm vào
  app/                    LẮP RÁP: App.js (đăng ký feature), config.js
  core/                   DÙNG CHUNG – NỀN MÓNG: Engine, EventBus, AssetLoader, ApiClient
  world/                  DÙNG CHUNG – THẾ GIỚI: geo, ánh sáng, mặt đất, Building, World
  features/<ten>/         MODULE CHỨC NĂNG, gỡ ra không làm hỏng chỗ khác
  ui/components/          DÙNG CHUNG – GIAO DIỆN: Panel...
  shared/                 DÙNG CHUNG – TIỆN ÍCH: math, debug
  styles/                 CSS chung, biến màu
```

## Chạy
```bash
npm install
npm run dev          # http://localhost:5173  (backend không bắt buộc)
```
Muốn có dữ liệu từ backend: mở terminal khác, chạy server (xem `server/README.md`). Vite tự chuyển `/api/...` sang `localhost:3000`.

Mọi lời gọi backend đi qua `src/core/ApiClient.js`. Backend tắt → tự dùng `public/data`, web vẫn chạy.
