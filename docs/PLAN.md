# Kế hoạch dự án B1Web – Website 3D tham quan khuôn viên ĐH Bách khoa Hà Nội

| | |
|---|---|
| **Giai đoạn 1** | Tham quan xung quanh nhà B1 |
| **Về sau** | Mở rộng ra toàn khuôn viên |
| **Nhóm** | 5 sinh viên, máy Windows và Linux |
| **Repo** | `github.com/LL-ixt/B1Web` |
| **Thời lượng** | 12 tuần (10 tuần làm + 2 tuần đệm/báo cáo) |

> **Tinh thần chung:** làm nhỏ nhưng làm trọn vẹn, và hiểu từng dòng mình viết. Mỗi tuần phải có một bản chạy được trên trình duyệt, dù còn xấu. Tính năng trước chưa xong thì chưa thêm tính năng sau.

---

## Mục lục
1. Hiện trạng
2. Mục tiêu và phạm vi
3. Công nghệ và cài đặt
4. Kiến trúc
5. Cấu trúc thư mục
6. Quy trình Blender → Web
7. Phân vai theo tầng
8. Lộ trình theo sprint
9. Cách làm việc nhóm
10. Làm việc trên cả Windows và Linux
11. Triển khai (deploy)
12. Rủi ro
13. Mở rộng ra toàn khuôn viên
14. Tài liệu học
15. Việc cần làm ngay trong tuần đầu

---

## 1. Hiện trạng

### 1.1 Đã có trong repo `LL-ixt/B1Web`

Repo hiện có 1 commit.

- **Mô hình B1 dựng bằng script Python** trong Blender 5.2. Footprint và chiều cao từng phần lấy từ OpenStreetMap (way `184021007`). Script chạy lại nhiều lần không nhân đôi object.
- **Code đã tách module:** `wings` (cánh nhà), `lobby` (sảnh cong, mái đón xe, thềm), `tower` (tháp thang tròn), `rooftop`, `materials`, `context` (đường, xe, nhà xung quanh – đang tắt), `scene`.
- **4 camera đặt sẵn:** `Cam_Ref`, `Cam_Aerial`, `Cam_Lobby`, `Cam_Porch`. Dùng lại được làm góc nhìn có sẵn trên web.
- **Ảnh tham chiếu, sketch, và `.claude/CLAUDE.md`** ghi lại các quyết định thiết kế (hướng bắc, màu tường, cụm cửa sổ…).
- **File OSM** còn chứa nhà A17, nhà xe B1, phố Tạ Quang Bửu và vài khối nhà trường. Đây là nguồn để dựng môi trường xung quanh.

### 1.2 Vấn đề của repo cần sửa trước khi cả nhóm code

| Vấn đề | Hậu quả | Đã xử lý trong bản chuyển đổi |
|---|---|---|
| Không có `.gitignore`; đã commit `__pycache__/`, `B1.blend1` | Xung đột liên tục khi 5 người cùng đẩy code | Thêm `.gitignore`, bỏ các file rác |
| Chưa dùng Git LFS | Mỗi lần sửa `.blend` repo phình thêm 1,5 MB | `.gitattributes` đưa `.blend`, `.glb`, ảnh vào LFS |
| Tên file có dấu, dấu cách (`sảnh.png`, `map (3).osm`) | Hỏng tên khi tải zip / clone trên một số máy | Đổi thành `sanh.png`, `map.osm` |
| Đường dẫn `D:\Project III\...` trong script và `CLAUDE.md` | Máy Linux hoặc máy khác ổ đĩa không chạy được | Đường dẫn tương đối, chạy từ gốc repo |
| Cấu trúc chỉ có `blender/` | Chưa có chỗ cho web, backend, tài liệu | Cấu trúc mới (mục 5) |

Các bước chuyển đổi nằm ở `docs/MIGRATION.md`. Bản repo đã chuyển sẵn nằm trong file zip đi kèm.

### 1.3 Các điểm của mô hình cần xử lý khi đưa lên web

| Vấn đề | Cách xử lý |
|---|---|
| Vật liệu dùng node Noise (`add_grime`); glTF không mang được node procedural | Giai đoạn 1 chấp nhận mất. Muốn giữ thì bake ra texture ở giai đoạn sau |
| Hàng nghìn ô cửa sổ là hình học riêng → nhiều object, web chậm | Gộp mesh theo vật liệu trước khi xuất. Nâng cao: `InstancedMesh` cho cửa sổ lặp lại |
| Gốc tọa độ = tâm B1 (`osm.make_projector`) | Chốt `CAMPUS_ORIGIN` chung (tạm = tâm B1) trước khi làm tòa thứ hai |
| Blender Z-up, Three.js Y-up | Exporter bật `+Y Up`. Quy ước Three.js: `x = đông, y = lên, z = nam` |
| Chưa có mesh va chạm | Thêm vài hộp `COL_*` bọc từng cánh nhà |
| Chỉ có mặt ngoài | Phạm vi giai đoạn 1 là ngoài trời |

### 1.4 Còn thiếu

Bản tham khảo "những thứ cần cài và chức năng website mẫu" **chưa có** trong repo và file zip. Plan này dùng bộ chức năng phổ biến của các web tham quan 3D. Khi có bản đó, đối chiếu lại mục 2 và 3.

---

## 2. Mục tiêu và phạm vi

**Mục tiêu sản phẩm:** người dùng mở link, thấy nhà B1 trong khuôn viên. Họ có thể xoay ngắm hoặc đi bộ quanh nhà, bấm vào các điểm để đọc thông tin, xem nhanh vài góc đẹp, và gửi góp ý. Quản trị viên sửa được nội dung thông tin mà không cần sửa code.

**Mục tiêu học tập:** mỗi thành viên nắm được chuỗi *Blender → glTF → Three.js → API → CSDL*. Mỗi người làm chủ một tầng và đọc hiểu được các tầng còn lại. Cả nhóm làm việc chung bằng Git và Pull Request.

| Mức | Frontend | Backend | Làm khối |
|---|---|---|---|
| **Must** (MVP) | Nạp B1 + màn hình tải · Xoay quanh (orbit) · Ánh sáng, bầu trời, bóng · Hotspot + bảng thông tin · Nút góc nhìn có sẵn | API đọc tòa nhà và điểm thông tin · CSDL SQLite + dữ liệu mẫu · Test cơ bản | B1 xuất `.glb` đạt ngân sách hiệu năng · Đặt `POI_*` và `Cam_*` |
| **Should** | Đi bộ góc nhìn người có va chạm · Chuyển cảnh mượt · Minimap · Dùng được trên điện thoại · Form góp ý | API thêm/sửa/xóa điểm thông tin (có token quản trị) · API góp ý · Trang quản trị | Mesh va chạm `COL_*` · Khối đơn giản cho nhà xe B1, A17, đường từ OSM |
| **Could** | Tour tự động có chú thích · Ngày/đêm · Âm thanh nền | Thống kê lượt xem trên trang quản trị · Chống spam góp ý | Cây, ghế, xe (đối tượng lặp lại) · Bake texture vết bẩn |
| **Won't** (giai đoạn 1) | Bên trong tòa nhà · Nhiều tòa nhà · VR | Tài khoản người dùng, đăng nhập nhiều vai trò | Mô hình các tòa khác |

---

## 3. Công nghệ và cài đặt

### 3.1 Lựa chọn và lý do

| Tầng | Công nghệ | Vì sao |
|---|---|---|
| Làm khối | Blender 5.2 + Python (script sẵn có) | Nhóm đã dựng B1 bằng script; giữ nguyên |
| Định dạng 3D | glTF 2.0 nhị phân (`.glb`) nén Draco | Chuẩn của web 3D, Three.js đọc trực tiếp |
| Frontend | **Three.js thuần + Vite + JavaScript**, UI bằng HTML/CSS | Ít lớp trừu tượng, đọc code là thấy renderer, scene, camera, vòng lặp (xem `docs/decisions/001-…`) |
| Backend | **Node.js + Express 5** | Cùng ngôn ngữ JavaScript với frontend, hỗ trợ nhau được |
| CSDL | **SQLite** qua `node:sqlite` có sẵn trong Node | CSDL là một file, không cài máy chủ CSDL, không cần trình biên dịch C++ trên Windows (xem `docs/decisions/002-…`) |
| Kiểm thử backend | `node:test` có sẵn | Không cài thêm thư viện |

Frontend luôn có dữ liệu tĩnh dự phòng trong `web/public/data`. Vì vậy **frontend không phải chờ backend**: tuần đầu đã chạy được, và bản deploy chỉ có frontend vẫn hoạt động.

### 3.2 Cài đặt cho từng máy

| Công cụ | Windows | Linux (Ubuntu/Debian) |
|---|---|---|
| **Node.js LTS ≥ 22.13** | Bộ cài từ nodejs.org (hoặc `nvm-windows`) | `nvm` (`nvm install --lts`); không dùng bản `apt` vì thường cũ |
| **Git + Git LFS** | Git for Windows (đã có LFS) | `sudo apt install git git-lfs` |
| | Sau khi cài, mỗi máy chạy `git lfs install` một lần | |
| **Blender 5.2** (cả nhóm cùng bản) | Bộ cài `.msi`, thêm vào PATH | Bản `.tar.xz` từ blender.org, thêm vào PATH (hoặc snap) |
| **VS Code** | Bộ cài | `.deb` hoặc snap |
| Tiện ích VS Code | Mở repo, VS Code tự gợi ý theo `.vscode/extensions.json`: Prettier, ESLint, glTF Tools, EditorConfig, Python, Live Share | |
| Trình duyệt | Chrome hoặc Edge mới (để dùng DevTools) | Chrome hoặc Chromium mới |

Thư viện npm được cài tự động bằng `npm install` theo `package.json`:

- **Frontend:** `three`, `vite`, `lil-gui`.
- **Backend:** `express`, `cors`.
- **Thêm khi cần:** `gsap` (chuyển cảnh camera, Sprint 3), `three-mesh-bvh` (va chạm nhanh, chỉ khi raycast thường bị chậm).

Công cụ không cần cài:

- glTF Viewer (`gltf-viewer.donmccurdy.com`) để kiểm tra file `.glb`.
- `npx @gltf-transform/cli inspect file.glb` để xem số liệu model.

---

## 4. Kiến trúc

### 4.1 Toàn hệ thống

```
 ┌──────── LÀM KHỐI ────────┐        ┌────────────── FRONTEND (trình duyệt) ──────────────┐
 │ map.osm + ảnh tham chiếu │        │                                                    │
 │          │               │  .glb  │  Three.js: nạp model, ánh sáng, điều hướng,        │
 │ Script Python (Blender)  ├───────►│  hotspot, bảng thông tin, minimap, góp ý           │
 │          │               │        │                     │                              │
 │       B1.blend           │        │              ApiClient (core)                      │
 └──────────────────────────┘        │         │                       │ backend tắt?     │
                                     └─────────┼───────────────────────┼──────────────────┘
                                         HTTP /api               dữ liệu tĩnh dự phòng
                                               │                  web/public/data/*.json
                                     ┌─────────▼──────── BACKEND ─────────┐      ▲
                                     │ Express: campus, buildings, pois,  │      │ npm run seed
                                     │ feedback, stats                    │──────┘ (nạp mẫu ban đầu)
                                     │          │                         │
                                     │   SQLite (server/data/tour.db)     │
                                     └────────────────────────────────────┘
```

### 4.2 Frontend chia tầng

```
 app/        App.js đăng ký feature · config.js hằng số
   │  ctx = { config, bus, engine, assets, api, world, uiRoot }
 features/   MODULE CHỨC NĂNG: loading · navigation · hotspots · info-panel · tour · minimap · feedback
   │  phát/nghe sự kiện qua EventBus, dùng component chung
 world/  ui/  shared/      DÙNG CHUNG: tọa độ geo, ánh sáng, tòa nhà · Panel · math, debug
   │
 core/       NỀN MÓNG: Engine (renderer, scene, camera, vòng lặp) · EventBus · AssetLoader · ApiClient
```

### 4.3 Backend chia tầng

```
 app.js               gắn các module vào /api/...
 modules/<ten>/       MODULE CHỨC NĂNG: routes.js (đường dẫn, kiểm tra đầu vào) + service.js (truy vấn CSDL)
   campus · buildings · pois · feedback · stats
 db/ middleware/ shared/   DÙNG CHUNG: kết nối + schema + seed · requireAdmin, errorHandler · validate
```

### 4.4 Năm nguyên tắc giữ dự án không rối khi mở rộng

1. **Phụ thuộc chỉ đi xuống.** Tầng trên dùng tầng dưới, không có chiều ngược lại. Các module chức năng không import lẫn nhau, ở cả frontend lẫn backend.
2. **Feature frontend nói chuyện qua EventBus.** Ví dụ: Hotspot phát `poi:click`, InfoPanel nghe `poi:click`. Hai người làm song song mà không đụng file của nhau.
3. **Chốt hợp đồng API trước (contract-first).** `docs/API.md` là thỏa thuận giữa frontend và backend. Muốn đổi dữ liệu thì sửa file này trong PR trước, rồi mới code.
4. **Dữ liệu tách khỏi code.** Danh sách tòa nhà, điểm thông tin và góc nhìn nằm trong CSDL (lúc đầu là JSON). Thêm nhà C1 không phải sửa code.
5. **Mọi lời gọi backend đi qua `ApiClient`.** Backend tắt thì tự dùng dữ liệu tĩnh. Feature không tự gọi `fetch`.

Mỗi feature frontend có cùng một "hình dạng":

```js
export class XxxFeature {
  init(ctx) {}    // tạo DOM, đăng ký sự kiện
  update(dt) {}   // (tùy chọn) chạy mỗi khung hình
  dispose() {}    // dọn dẹp
}
```

---

## 5. Cấu trúc thư mục

Bản đã chuyển đổi trong zip đi kèm **chạy được ngay**. Phần frontend đã build thử thành công, phần backend đã chạy và qua đủ 6 test.

```
B1Web/
├── README.md                    chạy nhanh
├── .gitignore .gitattributes    rác không commit · LF + Git LFS
├── .editorconfig .prettierrc .nvmrc   đồng bộ định dạng giữa Windows và Linux
├── .vscode/                     setting + tiện ích gợi ý cho cả nhóm
├── .claude/CLAUDE.md            ghi chú thiết kế mô hình B1 (đã sửa đường dẫn)
│
├── docs/                        TÀI LIỆU
│   ├── PLAN.md                  file này
│   ├── MIGRATION.md             chuyển repo cũ sang cấu trúc mới
│   ├── CONVENTIONS.md           quy ước: tên file, đa nền tảng, Blender, tọa độ, Git, code
│   ├── API.md                   hợp đồng API frontend ↔ backend
│   ├── meetings/                biên bản họp (TEMPLATE.md)
│   └── decisions/               001 Three.js thuần · 002 Express + SQLite
│
├── blender/                     ── LÀM KHỐI ──
│   ├── data/map.osm             dữ liệu bản đồ dùng chung
│   ├── shared/                  code Python dùng chung (để trống, dùng khi làm tòa thứ 2)
│   ├── buildings/
│   │   └── b1/
│   │       ├── B1.blend  build_b1.py
│   │       ├── b1/              package dựng: wings, lobby, tower, rooftop, materials...
│   │       ├── ref/             ảnh tham chiếu, sketch
│   │       └── _backup/
│   ├── tools/                   export_glb.py (xuất web) · render_views.py
│   └── renders/                 ảnh render kiểm tra
│
├── web/                         ── FRONTEND ──
│   ├── index.html               trang tham quan
│   ├── admin/                   trang quản trị nội dung (/admin/)
│   ├── vite.config.js           proxy /api → localhost:3000, 2 trang
│   ├── public/
│   │   ├── models/buildings/b1/b1.glb    ← mỗi tòa một thư mục
│   │   ├── models/props/  textures/  hdri/  images/pois/
│   │   └── data/campus.json  data/buildings/b1.json   dữ liệu mẫu + dự phòng
│   └── src/
│       ├── main.js
│       ├── app/                 App.js · config.js
│       ├── core/                Engine · EventBus · AssetLoader · ApiClient
│       ├── world/               geo · Lighting · Ground · Building · World
│       ├── features/            loading ✓ · navigation (orbit ✓, walk) · hotspots · info-panel
│       │                        tour · minimap · feedback
│       ├── ui/components/       Panel
│       ├── shared/              math · debug (mở bằng ?debug)
│       └── styles/
│
└── server/                      ── BACKEND ──
    ├── .env.example             PORT, DB_PATH, ADMIN_TOKEN, CORS_ORIGIN
    ├── src/
    │   ├── index.js  app.js  config.js
    │   ├── db/                  connection · schema.sql · seed.js
    │   ├── middleware/          requireAdmin · errorHandler
    │   ├── shared/              validate
    │   └── modules/             campus ✓ · buildings ✓ · pois (TODO) · feedback ✓ · stats ✓
    ├── tests/api.test.js        6 test
    └── data/                    tour.db (không commit)
```

(✓ là phần đã chạy được, còn lại là khung có ghi chú TODO từng bước.)

**Phân biệt "dùng chung" và "chức năng"** bằng một câu hỏi: *nếu xóa thư mục này, chức năng khác có bị hỏng không?*

- Có → đó là phần dùng chung: `core`, `world`, `ui`, `shared` ở frontend; `db`, `middleware`, `shared` ở backend; `blender/data`, `blender/shared`, `blender/tools`.
- Không → đó là module chức năng.

---

## 6. Quy trình Blender → Web

### 6.1 Quy ước tên object

Web đọc object theo tên:

| Tiền tố | Ý nghĩa | Web xử lý |
|---|---|---|
| `B1_...` | Mesh hiển thị | Hiển thị, đổ bóng |
| `COL_...` | Hộp va chạm đơn giản | Ẩn, dùng cho chế độ đi bộ |
| `POI_...` | Empty đánh dấu điểm thông tin | Gắn hotspot |
| `Cam_...` | Camera góc nhìn | Nút góc nhìn / tour |

`web/src/world/Building.js` đã tự nhận diện các tiền tố này.

### 6.2 Mỗi lần cập nhật model

Tất cả lệnh chạy từ thư mục gốc repo.

1. Dựng lại model: `blender -b blender/buildings/b1/B1.blend -P blender/buildings/b1/build_b1.py`
2. Lần đầu: thêm collection `B1_Collision` gồm các hộp `COL_*`, và các Empty `POI_*` ở sảnh, mái đón xe, tháp thang.
3. Gộp mesh theo vật liệu để giảm số object (nên viết thành một bước trong script).
4. Xuất file: `blender -b blender/buildings/b1/B1.blend -P blender/tools/export_glb.py -- B1_Building web/public/models/buildings/b1/b1.glb`
5. Kiểm tra trong glTF Viewer: đúng hướng, đúng vật liệu, dung lượng hợp lý.
6. Mở web với `?debug`, xem FPS, rồi commit cả `.blend` lẫn `.glb`.

`export_glb.py` viết theo API exporter glTF của Blender nhưng **chưa được chạy thử** trên máy nhóm. Việc chạy thử là của bạn làm khối ở Sprint 0.

### 6.3 Ngân sách hiệu năng

Các con số dưới đây là mục tiêu. Đo thực tế rồi điều chỉnh.

| Chỉ số | Mục tiêu |
|---|---|
| `b1.glb` (đã nén Draco) | dưới 5 MB |
| Tam giác cả cảnh | dưới 500 nghìn |
| Draw call (`renderer.info.render.calls`) | dưới 150 |
| FPS trên laptop card onboard | khoảng 50–60 |
| Tải lần đầu qua 4G | dưới 10 giây |
| API `GET /buildings/:id` | dưới 100 ms |

---

## 7. Phân vai theo tầng

Chia theo tầng (làm khối, frontend, backend) cho rõ trách nhiệm. Frontend có nhiều việc nhất nên có 3 người. Mỗi người còn có một **cặp đôi ở tầng khác** để hiểu chỗ hai tầng nối với nhau, và để có người thay khi ai đó bận.

| Vai | Tầng | Làm chính | Cặp đôi | Thư mục phụ trách |
|---|---|---|---|---|
| **TV1 – Trưởng nhóm + Frontend lõi** | Frontend | Chia task, chủ trì họp, review PR. Giữ `core/`, `app/`, `world/`: ánh sáng, bầu trời, mặt đất, nạp tòa nhà. Deploy frontend | Cả nhóm | `web/src/core`, `app`, `world`, `docs/` |
| **TV2 – Làm khối 3D** (chủ repo) | Làm khối | Hoàn thiện B1; mesh va chạm, POI, camera; xuất và tối ưu `.glb`; khối nhà xung quanh từ OSM | TV3 | `blender/`, `web/public/models` |
| **TV3 – Frontend 3D tương tác** | Frontend | Orbit, chế độ đi bộ, va chạm, chuyển cảnh camera, tour | TV2 | `features/navigation`, `features/tour` |
| **TV4 – Frontend giao diện** | Frontend | Hotspot, bảng thông tin, minimap, form góp ý, trang quản trị, giao diện điện thoại | TV5 | `features/hotspots`, `info-panel`, `minimap`, `feedback`, `web/admin`, `ui/`, `styles/` |
| **TV5 – Backend + dữ liệu** | Backend | API, CSDL, xác thực quản trị, góp ý, thống kê, test, deploy backend. Giữ `docs/API.md`. Phụ trách nội dung điểm thông tin (kiểm chứng nguồn) | TV4 | `server/`, `docs/API.md`, `web/public/data` |

Chỗ nối giữa các tầng cần hai người cùng ngồi làm:

- **TV2 ↔ TV3:** mesh va chạm, vị trí camera, hướng tọa độ.
- **TV4 ↔ TV5:** hình dạng dữ liệu POI, API quản trị, form góp ý.
- **TV1 ↔ TV5:** `ApiClient`, cấu hình CORS, deploy.

Quy tắc chung cho cả 5 người:

- Ở Sprint 0, ai cũng **tự làm một bài Three.js nhỏ và một API Express nhỏ**, kể cả bạn làm khối. Nhờ vậy ai cũng đọc được code của các tầng khác.
- Mỗi tuần, mỗi người **review ít nhất một PR của tầng khác**.

---

## 8. Lộ trình theo sprint (2 tuần/sprint)

### Sprint 0 – Tuần 1: Khởi động

| Ai | Việc |
|---|---|
| TV2 | Chuyển repo theo `docs/MIGRATION.md`, mời đủ thành viên, bảo vệ nhánh `main`. Chạy thử `export_glb.py`, ghi số liệu `.glb` đầu tiên (dung lượng, số tam giác, số object) |
| TV1 | Lập bảng task (GitHub Projects), chốt lịch họp, tạo nhánh `dev` |
| Cả nhóm | Cài công cụ (mục 3). Clone repo, chạy được `web` và `server` trên máy mình |
| Cả nhóm | Bài tập cá nhân: scene Three.js có hộp xoay và đèn, nạp một `.glb` mẫu; một API Express trả JSON |

**Xong khi:** 5/5 người chạy được cả hai phần; có bảng task; có `b1.glb` bản đầu, dù còn nặng.

### Sprint 1 – Tuần 2–3: "Thấy B1 trên web"

| Ai | Việc |
|---|---|
| TV2 | Gộp mesh, xóa Cube, đạt ngân sách dung lượng; đặt `POI_*` |
| TV1 | Ánh sáng khớp Blender, bóng đổ, mặt đất; deploy bản đầu lên GitHub Pages |
| TV3 | Tinh chỉnh orbit: giới hạn góc và khoảng cách, không xuyên đất |
| TV4 | Màn hình tải, khung toolbar |
| TV5 | Chốt `docs/API.md` với TV4; schema CSDL; seed từ JSON; hoàn thiện test cho campus và buildings |

**Mốc M1:** có link công khai, mở ra thấy B1 đúng hướng, đúng vị trí, xoay ngắm được.

### Sprint 2 – Tuần 4–5: "Đi bộ quanh B1"

| Ai | Việc |
|---|---|
| TV3 | `WalkMode`: khóa chuột, WASD, chạy, giữ độ cao mắt; nút chuyển orbit ↔ walk |
| TV2 + TV3 | Hộp va chạm `COL_*` và raycast va chạm |
| TV2 | Khối đơn giản cho đường, nhà xe B1, A17 từ OSM |
| TV4 | Hướng dẫn phím điều khiển trên màn hình; bắt đầu `HotspotFeature` |
| TV5 | API `POST/PUT/DELETE /pois` có `requireAdmin`, kèm test |
| TV1 | Frontend đọc dữ liệu từ backend khi dev (proxy), kiểm tra cơ chế dự phòng khi tắt backend |

**Mốc M2:** đi bộ một vòng quanh B1 không xuyên tường; API quản trị POI qua hết test.

### Sprint 3 – Tuần 6–7: "Bấm để tìm hiểu"

| Ai | Việc |
|---|---|
| TV4 | Hoàn thiện `HotspotFeature` và `InfoPanelFeature` |
| TV5 | Viết và kiểm chứng nội dung 3–6 điểm thông tin, ảnh thực tế (cùng cả nhóm đi chụp) |
| TV3 | `TourFeature`: nút góc nhìn từ `Cam_*`, chuyển cảnh mượt |
| TV2 | `Cam_Top` (nhìn thẳng từ trên, orthographic) làm nền minimap |
| TV1 | Tích hợp, sửa lỗi ghép nối, đo hiệu năng lần 1 |

**Mốc M3 – MVP:** đủ toàn bộ mục Must.

### Sprint 4 – Tuần 8–9: "Quản trị, góp ý, điện thoại"

| Ai | Việc |
|---|---|
| TV4 + TV5 | Trang quản trị: nhập token, danh sách POI, thêm/sửa/xóa; xem góp ý |
| TV4 | Form góp ý, minimap, giao diện điện thoại, điều khiển chạm |
| TV5 | Deploy backend (mục 11), cấu hình CORS, chống spam góp ý đơn giản |
| TV3 | Joystick ảo cho chế độ đi bộ trên điện thoại (nếu kịp), tour tự động |
| TV1 + TV2 | Tối ưu theo ngân sách hiệu năng; kiểm thử trên nhiều máy, nhiều trình duyệt |

**Mốc M4:** đủ mục Should, không còn lỗi nghiêm trọng.

### Sprint 5 – Tuần 10–11: Hoàn thiện

- Sửa lỗi, đánh bóng. Chọn 1–2 mục Could nếu còn thời gian.
- Viết tài liệu: README, sơ đồ kiến trúc, hướng dẫn thêm tòa nhà mới.
- Mỗi người viết một trang *"mình đã làm gì, học được gì"* cho báo cáo.

### Tuần 12: Đệm và báo cáo

Không thêm tính năng. Chuẩn bị slide, video demo, tổng duyệt.

### Định nghĩa "xong" cho mỗi task

- Đã merge vào `dev` qua PR có người review.
- Không có lỗi trong console.
- Backend: có test và test pass.
- Đã cập nhật README, `docs/API.md` hoặc danh sách sự kiện EventBus nếu có thay đổi.
- Đã chạy thử trên ít nhất một máy Windows và một máy Linux.

---

## 9. Cách làm việc nhóm

- **Họp:** 1 buổi/tuần, khoảng 45 phút, dùng `docs/meetings/TEMPLATE.md`. Hằng ngày nhắn ngắn trong nhóm chat: hôm qua làm gì, hôm nay làm gì, đang vướng gì.
- **Bảng công việc:** GitHub Projects, 4 cột *Cần làm / Đang làm / Chờ review / Xong*. Mỗi task không quá 2 ngày công; lớn hơn thì chia nhỏ. Gắn nhãn tầng `3d`, `frontend`, `backend`.
- **Git:**
  - `main` luôn chạy được ← `dev` ← `feature/<ten>`.
  - Vào `dev` bằng PR, có ít nhất 1 người duyệt.
  - Cuối mỗi sprint gộp `dev` vào `main` và deploy.
  - Chi tiết ở `docs/CONVENTIONS.md`.
- **File `.blend` không merge được như code:**
  - Tại một thời điểm chỉ TV2 sửa. Ai cần thay đổi thì mở issue.
  - Ưu tiên sửa script Python rồi chạy lại, hạn chế sửa tay trong Blender.
- **Đổi dữ liệu giữa frontend và backend:** sửa `docs/API.md` trong PR trước, TV4 và TV5 cùng duyệt.
- **Demo cuối sprint:** mỗi người tự demo phần mình và kể một điều đã học. Đây là cách chắc nhất để cả nhóm hiểu toàn dự án.

---

## 10. Làm việc trên cả Windows và Linux

Mọi công cụ đều đa nền tảng. Những chỗ hay vấp đã được chốt sẵn trong repo và ghi ở `docs/CONVENTIONS.md`. Tóm tắt:

| Chỗ hay vấp | Quy tắc |
|---|---|
| Chữ hoa/thường | Linux và máy chủ deploy phân biệt `App.js` ≠ `app.js`, Windows thì không. Import phải đúng y tên file; đổi hoa/thường bằng `git mv` |
| Tên file | Không dấu, không dấu cách, không ngoặc |
| Xuống dòng | LF, đã chốt bằng `.gitattributes`, `.editorconfig`, `.vscode/settings.json` |
| Lệnh | Chạy từ gốc repo, đường dẫn tương đối, dấu `/`. Không ghi đường dẫn tuyệt đối vào code |
| Biến môi trường | Để trong `server/.env`; Node tự đọc bằng `--env-file-if-exists`, không phụ thuộc shell |
| Phiên bản | Node LTS ≥ 22.13, Blender 5.2 – cả nhóm dùng giống nhau |
| Lệnh duy nhất khác nhau | Chép `.env`: `cp` (Linux) và `Copy-Item` (PowerShell), đã ghi cả hai trong README |

---

## 11. Triển khai (deploy)

| Phần | Nơi đề xuất | Ghi chú |
|---|---|---|
| Frontend | GitHub Pages (miễn phí, cùng chỗ với repo) hoặc Vercel/Netlify | `npm run build` → thư mục `web/dist`. `base: './'` đã đặt sẵn. Đặt `VITE_API_URL` trỏ tới backend |
| Backend | Dịch vụ có gói miễn phí chạy Node.js (Render, Railway, Fly.io…) – **kiểm tra điều kiện gói miễn phí lúc deploy** vì hay thay đổi | Đặt `ADMIN_TOKEN`, `CORS_ORIGIN` trong phần biến môi trường của dịch vụ |

**Lưu ý quan trọng về SQLite:** nhiều gói miễn phí có ổ đĩa tạm, nên khởi động lại là mất file `tour.db`. Có ba cách:

- (a) chọn dịch vụ có ổ đĩa lưu lâu dài;
- (b) chạy lại `npm run seed` mỗi lần khởi động và chấp nhận mất góp ý;
- (c) khi demo, chạy backend trên máy một thành viên.

Dù chọn cách nào, frontend vẫn chạy nhờ dữ liệu tĩnh dự phòng. TV5 quyết định ở Sprint 4 và ghi lại thành `docs/decisions/003-…`.

---

## 12. Rủi ro

| Rủi ro | Dấu hiệu | Phòng / xử lý |
|---|---|---|
| Model quá nặng, web giật | FPS < 30, `.glb` > 10 MB | Gộp mesh, Draco, giảm chi tiết mặt sau; đo ngay từ Sprint 1 |
| Lệch tọa độ Blender ↔ web | Nhà quay sai hướng, POI lơ lửng | Theo `CONVENTIONS.md`; so `Cam_Ref` với `ref.jpg` |
| Frontend chờ backend | Feature treo vì API chưa xong | Dữ liệu tĩnh dự phòng + chốt `API.md` trước |
| Backend thiếu việc lúc đầu, quá tải lúc cuối | TV5 rảnh ở Sprint 0–1 | TV5 phụ trách thêm nội dung và test; trang quản trị dời sang Sprint 4 |
| Ôm đồm tính năng | MVP chưa xong đã làm ngày/đêm | Bám MoSCoW; mục Could chỉ làm sau M3 |
| Xung đột Git, nhất là `.blend` | Mất công sức của nhau | Git LFS, một người giữ `.blend`, PR nhỏ |
| Lỗi chỉ xuất hiện trên một hệ điều hành | "Máy em chạy được mà" | Mục 10; test trên cả hai hệ trước khi coi là xong |
| Lộ `ADMIN_TOKEN` | Token nằm trong commit | `.env` đã bị chặn trong `.gitignore`; lỡ lộ thì đổi token ngay |
| Thông tin POI sai | Mô tả đơn vị, năm xây dựng sai | TV5 kiểm chứng từ trang chính thức của trường, ghi nguồn |
| Bản quyền ảnh, logo | Dùng ảnh mạng không phép | Ưu tiên ảnh nhóm tự chụp; logo trường thì xin phép hoặc không dùng |
| Một thành viên bận/nghỉ | Task treo nhiều ngày | Cặp đôi ở mục 7 tiếp quản |

---

## 13. Mở rộng ra toàn khuôn viên (giai đoạn 2 trở đi)

1. **Chốt gốc tọa độ khuôn viên** (một điểm giữa trường) làm `CAMPUS_ORIGIN`. Sửa `osm.make_projector` để nhận gốc cố định thay vì tâm từng tòa. Phải làm việc này **trước** khi dựng tòa thứ hai.
2. **Tải lại OSM cho cả trường** vào `blender/data/`.
3. **Chuyển code Python dùng chung** (`osm`, `geom`, `meshkit`, `materials`) sang `blender/shared/`. Mỗi tòa mới có thư mục `blender/buildings/<id>/` riêng.
4. **Mỗi tòa một file `.glb`** và một bản ghi trong bảng `buildings`. Frontend không phải sửa code.
5. **Nạp theo khoảng cách (lazy loading)** trong `World.js`: chỉ tải nhà gần camera, nhà ở xa hiển thị bằng khối đơn giản dựng từ footprint OSM.
6. **Thêm module mới khi cần**, mỗi chức năng có cặp frontend và backend:
   - `search` – tìm nhà, tìm phòng;
   - `directions` – chỉ đường giữa hai nhà;
   - `interior` – bên trong một số sảnh;
   - `auth` – tài khoản quản trị viên thật, thay cho token chung.

---

## 14. Tài liệu học

| Tầng | Tài liệu |
|---|---|
| Three.js | three.js Manual – *Fundamentals* (threejs.org/manual) · ví dụ `webgl_loader_gltf`, `misc_controls_pointerlock`, `css2d_label` (threejs.org/examples) · sách miễn phí *Discover three.js* (discoverthreejs.com) |
| Blender → web | Blender Manual – *Import/Export → glTF 2.0* |
| Backend | Express – *Getting started* và *Routing* (expressjs.com) · Node.js docs – `node:sqlite`, `node:test` · SQLite tutorial (sqlitetutorial.net) |
| Web nói chung | MDN – *Fetch API*, *CORS*, *HTTP status codes* |
| Git | *Pro Git* (git-scm.com/book) chương 2–3 · GitHub Docs – *About pull requests* |

---

## 15. Việc cần làm ngay trong tuần đầu

- [ ] Gửi lại bản tham khảo "cần cài gì / chức năng website mẫu" để đối chiếu mục 2–3.
- [ ] Phân vai theo mục 7, điền tên vào `web/src/features/README.md`.
- [ ] Kiểm tra bản `B1.blend` nào là mới nhất (bản gửi riêng khác bản trong repo).
- [ ] TV2 chuyển repo theo `docs/MIGRATION.md`, mời đủ 5 người, bảo vệ nhánh `main`.
- [ ] Cả nhóm cài công cụ, chạy `web` (`npm run dev`) và `server` (`npm test`) trên máy mình.
- [ ] TV2 chạy `export_glb.py`, đặt `b1.glb` vào web, báo số liệu cho cả nhóm.
- [ ] TV5 cùng TV4 đọc và chốt bản đầu `docs/API.md`.
- [ ] Họp tuần đầu, ghi biên bản vào `docs/meetings/`.
