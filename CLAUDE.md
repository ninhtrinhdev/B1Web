# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Tổng quan
Website 3D tham quan khuôn viên ĐH Bách khoa Hà Nội. Giai đoạn 1 chỉ có nhà B1 và khu vực xung quanh. Kế hoạch đầy đủ: `docs/PLAN.md`. Hợp đồng API: `docs/API.md`. Quy ước: `docs/CONVENTIONS.md`.

Ba tầng, mỗi tầng một thư mục: `blender/` (làm khối 3D, Python) → xuất `.glb` → `web/` (Three.js + Vite) ↔ `server/` (Express + SQLite). Chi tiết mô hình B1 (tên object, camera, hướng bắc, cụm cửa sổ) nằm trong `.claude/CLAUDE.md`; đọc file đó trước khi sửa `blender/`.

## Lệnh thường dùng

Mọi lệnh chạy từ thư mục con tương ứng, trừ lệnh Blender (chạy từ thư mục gốc repo, đường dẫn tương đối, dấu `/`).

**Frontend (`web/`)**
```bash
npm install
npm run dev        # http://localhost:5173, tự mở trình duyệt; /api/* proxy sang localhost:3000
npm run build      # build hai trang: index.html và admin/index.html → web/dist
npm run preview    # xem bản đã build
```

**Backend (`server/`)** — Node ≥ 22.13
```bash
cp .env.example .env          # PowerShell: Copy-Item .env.example .env
npm install
npm run seed                  # tạo server/data/tour.db từ web/public/data/*.json
npm run dev                   # node --watch, http://localhost:3000/api/health
npm start                     # không watch
npm test                      # toàn bộ test (node:test)
node --test tests/api.test.js                                  # một file
node --test --test-name-pattern="<tên test>" tests/api.test.js  # một test theo tên
```

**Blender (từ thư mục gốc repo)**
```bash
blender -b blender/buildings/b1/B1.blend -P blender/buildings/b1/build_b1.py
blender -b blender/buildings/b1/B1.blend -P blender/tools/export_glb.py -- B1_Building web/public/models/buildings/b1/b1.glb
```
Chưa có `web/public/models/buildings/b1/b1.glb` thì web hiện khối hộp tạm đúng vị trí B1.

**Lint/format:** repo không có script lint. `.prettierrc` (printWidth 120, singleQuote, LF) và `.editorconfig` là chuẩn định dạng; Prettier và ESLint chỉ cài qua tiện ích VS Code, không có trong `package.json`.

## Kiến trúc (đọc nhiều file mới thấy)

**Frontend: lắp ráp qua `App` + `ctx`.** `web/src/main.js` tạo `App` (`web/src/app/App.js`). `App` là nơi duy nhất biết mọi feature: nó tạo lõi (`Engine`, `EventBus`, `AssetLoader`, `ApiClient`, `World`), gom vào một object `ctx` và gọi `init(ctx)` cho từng feature trong mảng `FEATURES`. Muốn tắt một tính năng thì bỏ dòng tương ứng trong `FEATURES`.

**Feature không nói chuyện trực tiếp với nhau.** Mỗi feature (`web/src/features/<ten>/`) có `init(ctx)`, `update(dt)` tùy chọn và `dispose()`. Giao tiếp qua `ctx.bus` (`EventBus`, pub/sub). Danh sách sự kiện được ghi trong comment đầu file `web/src/core/EventBus.js`, cập nhật khi thêm sự kiện mới. Ví dụ: `HotspotFeature` phát `poi:click`, `InfoPanelFeature` nghe.

**Dữ liệu có hai nguồn, cùng một hình dạng.** `ApiClient` (`web/src/core/ApiClient.js`) là cửa duy nhất gọi backend. Khi backend không phản hồi, nó phát `api:offline` và đọc `web/public/data/*.json`. Vì vậy hình dạng JSON tĩnh phải giống hệt response API (`GET /campus`, `GET /buildings/:id`). Khi đổi dữ liệu, sửa `docs/API.md` trước, rồi cả hai phía.

**Nạp model.** `World` (`web/src/world/World.js`) lấy dữ liệu tòa nhà qua `ApiClient`, nạp `.glb` qua `AssetLoader` và dựng `Building`. `Building.js` nhận diện object theo tiền tố `B1_`, `COL_`, `POI_`, `Cam_` đã đặt trong Blender. Tiền tố là hợp đồng giữa Blender và web, xem `docs/CONVENTIONS.md` mục 3.

**Hệ tọa độ** khác nhau giữa Blender và Three.js: Blender Z-up (x đông, y bắc), Three.js Y-up (x đông, y lên, z nam). Exporter có bật +Y Up. Gốc tọa độ là `CAMPUS_ORIGIN` trong `web/src/app/config.js`.

**Backend: `createApp(db)` tách khỏi `listen`.** `server/src/app.js` tạo app Express mà không mở cổng, nhờ đó test gọi thẳng được. Mỗi module trong `server/src/modules/<ten>/` gồm `routes.js` (đường dẫn, kiểm tra đầu vào) và `service.js` (truy vấn CSDL). Module không import nhau; phần dùng chung ở `db/`, `middleware/`, `shared/`. Lỗi trả về luôn có dạng `{ "error": "..." }` qua `middleware/errorHandler.js`. Route có `requireAdmin` (header `Authorization: Bearer <ADMIN_TOKEN>`) là các API ghi.

**CSDL:** SQLite qua `node:sqlite`, file `server/data/tour.db` (không commit). Schema ở `server/src/db/schema.sql`, dữ liệu mẫu nạp bằng `npm run seed`. Đây là chỗ dễ mất dữ liệu khi deploy trên gói miễn phí (ổ đĩa tạm); xem `docs/PLAN.md` mục 11.

**Trạng thái API:** nhiều route còn TODO. `/api/pois` hiện chỉ là khung: `requireAdmin` rồi trả `501`. `PUT /buildings/:id` cũng chưa có. `docs/API.md` ghi trạng thái từng route; POI chỉ đọc được qua `GET /buildings/:id`.

## Quy ước dễ sai
- Tên file: không dấu, không dấu cách. Linux phân biệt hoa/thường; đổi tên chỉ bằng `git mv`.
- Không ghi đường dẫn tuyệt đối (`D:\...`, `/home/...`) vào code, tài liệu hay `package.json`.
- Mỗi API mới phải có test trong `server/tests/`.
- Đổi API: sửa `docs/API.md` trong PR trước.
- File `.blend` chỉ một người sửa tại một thời điểm. Ưu tiên sửa script Python rồi chạy lại.
