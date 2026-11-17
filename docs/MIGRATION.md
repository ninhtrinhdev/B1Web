# Chuyển repo B1Web sang cấu trúc mới (làm MỘT lần, trước khi cả nhóm code)

Người làm: chủ repo (`LL-ixt`). Mất khoảng 30 phút. Lệnh chạy được trên cả PowerShell và bash.

## Đã thay đổi những gì so với repo cũ
| Cũ | Mới |
|---|---|
| `blender/b1/`, `blender/B1.blend`, `blender/build_b1.py`, `blender/_backup/` | `blender/buildings/b1/...` |
| `blender/render_views.py` | `blender/tools/render_views.py` |
| `map (3).osm` | `blender/data/map.osm` |
| ảnh `.jpg`, `sảnh.png`, `cửa kính.png` ở gốc | `blender/buildings/b1/ref/` (`sanh.png`, `cua-kinh.png`) |
| `blender/B1.blend1`, `blender/b1/__pycache__/` | bỏ (đã chặn trong `.gitignore`) |
| `.gitattributes` chỉ có `text=auto` | thêm chuẩn hóa LF + Git LFS cho `.blend`, `.glb`, ảnh |
| Đường dẫn `D:\Project III\...` trong `build_b1.py`, `.claude/CLAUDE.md` | đường dẫn tương đối, mặc định đọc `blender/data/map.osm` |
| — | thêm `web/`, `server/`, `docs/`, `.editorconfig`, `.vscode/`, `.prettierrc`, `.nvmrc` |

Code dựng model (`b1/*.py`) **giữ nguyên**, chỉ đổi chỗ để.

## Các bước
```bash
git clone https://github.com/LL-ixt/B1Web.git
cd B1Web
git lfs install
git checkout -b chore/restructure

git rm -r -q .        # bỏ theo dõi + xóa mọi file (thư mục .git không bị đụng tới)
```
Giải nén `B1Web-restructured.zip`, chép **toàn bộ nội dung bên trong** thư mục `B1Web/` của zip vào repo,
nhớ chép cả file ẩn: `.gitignore`, `.gitattributes`, `.editorconfig`, `.prettierrc`, `.nvmrc`, `.claude/`, `.vscode/`.

> Nếu `B1.blend` trên máy bạn mới hơn bản trong repo thì chép đè vào `blender/buildings/b1/B1.blend`.
> (Bản `B1.blend` gửi kèm riêng khác bản trong repo – hãy kiểm tra bản nào là mới nhất.)

```bash
git add -A
git status            # phải thấy nhiều dòng "renamed:" -> Git hiểu là di chuyển, giữ lịch sử
git lfs ls-files      # phải liệt kê .blend, .jpg, .png -> đã vào LFS
```

## Kiểm tra trước khi commit
```bash
blender -b blender/buildings/b1/B1.blend -P blender/buildings/b1/build_b1.py      # in ra cây collection như cũ
blender -b blender/buildings/b1/B1.blend -P blender/tools/render_views.py -- Cam_Ref
```
So `blender/renders/Cam_Ref.png` với ảnh cũ – phải giống nhau.
```bash
cd web && npm install && npm run dev                  # thấy khối hộp tạm, xoay được
cd ../server && npm install && npm test               # 6 test pass
```

## Commit và mở Pull Request
```bash
git commit -m "chore: chuyển sang cấu trúc dự án mới (web, server, docs, LFS)"
git push -u origin chore/restructure
```
Mở PR trên GitHub, cả nhóm xem qua rồi merge vào `main`. Sau đó tạo nhánh `dev` từ `main`.
Vào *Settings → Collaborators* mời 4 bạn còn lại; *Settings → Branches* bật bảo vệ `main` (bắt buộc PR).

Ghi chú: các file nhị phân trong commit đầu tiên vẫn nằm trong lịch sử Git thường (không phải LFS).
Repo còn nhỏ nên không sao; **không** cần viết lại lịch sử.
