# Quy ước dự án

## 1. Tên file và thư mục
- Chỉ dùng chữ **không dấu**, số, `-`, `_`. Không dấu cách, không ngoặc. Ví dụ: `sanh.png`, `map.osm`.
  (Tên có dấu bị hỏng khi tải zip / clone trên một số máy: `sảnh.png` → `s#U1ea3nh.png`.)
- Nội dung tiếng Việt bên trong file thì thoải mái (file lưu UTF-8).
- Web: file class `PascalCase.js`, file tiện ích `camelCase.js`, thư mục `kebab-case`.

## 2. Làm việc trên cả Windows và Linux
| Chuyện | Quy tắc |
|---|---|
| Chữ hoa/thường | Linux (và GitHub Pages, máy chủ deploy) phân biệt `App.js` ≠ `app.js`, Windows thì không. Import phải gõ **đúng y** tên file. Đổi hoa/thường tên file dùng `git mv`, không đổi trong Explorer |
| Xuống dòng | Đã chốt LF bằng `.gitattributes`, `.editorconfig`, `.vscode/settings.json`. Không tắt |
| Đường dẫn trong lệnh | Chạy từ thư mục gốc repo, đường dẫn tương đối, dấu `/`. Không ghi `D:\...` hay `/home/...` vào code hay tài liệu |
| Đường dẫn trong code | Python: `os.path.join`; Node: `path.join` / `new URL(..., import.meta.url)`. Không nối chuỗi bằng `\` |
| Lệnh shell | Không viết lệnh riêng của bash hay PowerShell trong `package.json`. Lệnh nào khác nhau thì ghi cả hai bản trong README |
| Phiên bản | Node.js LTS (≥ 22.13), Blender 5.2 – **cả nhóm cùng phiên bản** |
| Biến môi trường | Đặt trong `server/.env` (Node tự đọc), không dùng `export` / `$env:` |

## 3. Đặt tên trong Blender (web đọc theo tên)
| Tiền tố | Ý nghĩa | Web xử lý |
|---|---|---|
| `B1_...` | Mesh hiển thị của nhà B1 | Hiển thị |
| `COL_...` | Mesh va chạm đơn giản (hộp) | Ẩn, dùng cho đi bộ |
| `POI_...` | Empty đánh dấu điểm thông tin | Gắn hotspot |
| `Cam_...` | Camera góc nhìn đẹp | Nút góc nhìn / tour |

Mỗi tòa nhà xuất **một** file: `web/public/models/buildings/<id>/<id>.glb`, `<id>` viết thường (`b1`, `c1`).

## 4. Hệ tọa độ
- Blender: x = đông, y = bắc, z = lên, đơn vị mét.
- Three.js (sau khi xuất glTF +Y up): x = đông, y = lên, z = **nam**.
- Gốc toàn khuôn viên = `CAMPUS_ORIGIN` trong `web/src/app/config.js`. Không đổi sau khi đã có nhiều tòa.

## 5. Git
- Nhánh: `main` (luôn chạy được, deploy từ đây) ← `dev` ← `feature/<ten-ngan>`, `fix/<ten>`, `model/<ten>`.
- Commit: `feat: …`, `fix: …`, `docs: …`, `model: …`, `api: …`, `refactor: …`, `test: …`.
- Vào `dev` qua Pull Request, ít nhất 1 người khác duyệt. Mỗi PR nhỏ (dưới ~300 dòng code).
- File `.blend`: chỉ **một người** sửa tại một thời điểm, báo trước trong nhóm. Ưu tiên sửa script Python rồi chạy lại.
- Không commit: `.env`, `server/data/*.db`, `node_modules/`, `*.blend1`, `__pycache__/` (đã có trong `.gitignore`).

## 6. Code
- Frontend: feature **không import** feature khác, phối hợp qua `ctx.bus`. Gọi backend chỉ qua `ctx.api`.
- Backend: module trong `server/src/modules/` không import lẫn nhau; dùng chung thì để ở `db/`, `middleware/`, `shared/`.
- Đổi API → sửa `docs/API.md` trước.
- Backend: mỗi API mới có ít nhất một test trong `server/tests/`.
