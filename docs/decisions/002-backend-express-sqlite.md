# 002 – Backend dùng Node.js + Express + SQLite (node:sqlite)
**Bối cảnh:** nhóm muốn có backend để học, dữ liệu nhỏ (vài tòa nhà, vài chục điểm thông tin, góp ý).
**Quyết định:**
- Node.js + Express: cùng ngôn ngữ JavaScript với frontend, các thành viên hỗ trợ nhau được.
- SQLite qua `node:sqlite` có sẵn trong Node ≥ 22.13: CSDL là một file, không cài máy chủ CSDL,
  không cần trình biên dịch C++ (thư viện `better-sqlite3` hay gặp lỗi cài trên Windows).
- Frontend luôn có dữ liệu tĩnh dự phòng trong `web/public/data` → không phụ thuộc backend để chạy.
**Hệ quả:** `node:sqlite` còn gắn nhãn experimental, Node in cảnh báo khi chạy. Chấp nhận vì dự án học tập.
Nếu cần, chuyển sang PostgreSQL ở giai đoạn sau – chỉ phải sửa `server/src/db/` và các `service.js`.
