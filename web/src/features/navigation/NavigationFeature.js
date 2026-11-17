import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { WalkMode } from './WalkMode.js';

/**
 * Điều hướng: 2 chế độ.
 *  - orbit: xoay quanh, nhìn tổng thể (đã chạy)
 *  - walk : đi bộ góc nhìn người, WASD + chuột (TODO trong WalkMode.js)
 * Nghe 'nav:mode' để đổi, 'camera:flyTo' để tới góc nhìn (TODO: chuyển cảnh mượt).
 */
export class NavigationFeature {
  init(ctx) {
    const { engine, bus, config } = ctx;
    this.orbit = new OrbitControls(engine.camera, engine.renderer.domElement);
    this.orbit.target.set(...config.CAMERA.target);
    this.orbit.enableDamping = true;
    this.orbit.maxPolarAngle = Math.PI * 0.49; // không cho chui xuống dưới đất
    this.orbit.minDistance = 5;
    this.orbit.maxDistance = 400;

    this.walk = new WalkMode(ctx);
    this.mode = 'orbit';

    this.off = [
      bus.on('nav:mode', (m) => this.setMode(m)),
      bus.on('camera:flyTo', ({ position, target }) => {
        // TODO: tween bằng gsap hoặc dùng damp() trong shared/math.js
        engine.camera.position.copy(position);
        this.orbit.target.copy(target);
      }),
    ];
  }

  setMode(m) {
    this.mode = m;
    this.orbit.enabled = m === 'orbit';
    if (m === 'walk') this.walk.enable();
    else this.walk.disable();
  }

  update(dt) {
    if (this.mode === 'orbit') this.orbit.update();
    else this.walk.update(dt);
  }

  dispose() { this.off.forEach((f) => f()); this.orbit.dispose(); this.walk.disable(); }
}
