// import { PointerLockControls } from 'three/addons/controls/PointerLockControls.js';

/**
 * TODO (Sprint 2): đi bộ góc nhìn thứ nhất.
 * Gợi ý từng bước:
 *  1. PointerLockControls: click vào canvas -> khóa chuột, nhìn quanh.
 *  2. Đọc phím W/A/S/D (+Shift chạy) -> vector di chuyển theo hướng camera, tốc độ config.WALK.
 *  3. Giữ camera ở y = config.WALK.eyeHeight (đất phẳng nên chưa cần raycast xuống).
 *  4. Va chạm: raycast ngang theo hướng đi vào ctx.world.colliders, chạm < 0.5 m thì dừng.
 *  5. Mobile: joystick ảo (giai đoạn sau).
 */
export class WalkMode {
  constructor(ctx) { this.ctx = ctx; this.enabled = false; }
  enable() { this.enabled = true; console.info('WalkMode: chưa làm'); }
  disable() { this.enabled = false; }
  update(_dt) {}
}
