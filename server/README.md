# server/ – backend (Node.js + Express + SQLite)

```
src/
  index.js            khởi động server
  app.js              tạo app Express, gắn các module
  config.js           đọc biến môi trường (.env)
  db/                 DÙNG CHUNG: kết nối SQLite, schema.sql, seed.js (nạp dữ liệu mẫu)
  middleware/         DÙNG CHUNG: requireAdmin (kiểm tra token), errorHandler
  shared/             DÙNG CHUNG: hàm kiểm tra dữ liệu đầu vào
  modules/<ten>/      MODULE CHỨC NĂNG: mỗi thư mục có routes.js (đường dẫn) + service.js (truy vấn)
    campus/  buildings/  pois/  feedback/  stats/
tests/                kiểm thử bằng node:test có sẵn
data/                 file tour.db (không commit)
```
Cùng tư tưởng với frontend: module không import lẫn nhau, phần dùng chung để ở `db/`, `middleware/`, `shared/`.

## Chạy
```bash
cp .env.example .env      # Windows PowerShell: Copy-Item .env.example .env
npm install
npm run seed              # tạo data/tour.db từ web/public/data/*.json
npm run dev               # http://localhost:3000/api/health
npm test
```
Cần Node.js ≥ 22.13 (dùng `node:sqlite` có sẵn, không phải cài trình biên dịch C++ trên Windows).
Node sẽ in cảnh báo `ExperimentalWarning: SQLite...` – bình thường, bỏ qua.

Hợp đồng API: `docs/API.md`.
