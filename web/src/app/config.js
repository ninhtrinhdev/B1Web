// Hằng số dùng chung toàn app. Đổi ở đây, không rải số "ma" trong code.
export const CONFIG = {
  // Gốc tọa độ của CẢ khuôn viên. Tạm đặt = tâm B1 để khớp model Blender hiện tại.
  // Khi mở rộng: chọn 1 điểm giữa trường, chốt lại, không đổi nữa.
  CAMPUS_ORIGIN: { lat: 21.004556536, lon: 105.846622104 },
  // Backend (server/). Khi dev, Vite chuyển /api sang localhost:3000 (xem vite.config.js).
  // Khi deploy frontend và backend ở 2 nơi: đặt VITE_API_URL trong web/.env.production
  API_URL: import.meta.env.VITE_API_URL ?? '/api',
  // Dữ liệu tĩnh dự phòng khi backend chưa chạy / chưa deploy
  STATIC_DATA_URL: 'data',
  // Vị trí đầu lấy gần Cam_Ref trong Blender (x=-36, y_bắc=62 -> z=-62)
  CAMERA: { fov: 55, near: 0.1, far: 3000, start: [-36, 20, -62], target: [0, 10, 0] },
  WALK: { eyeHeight: 1.65, speed: 4.0, runSpeed: 8.0 },
  DEBUG: new URLSearchParams(location.search).has('debug'), // thêm ?debug vào URL
};
