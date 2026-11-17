import * as THREE from 'three';

/** Renderer + scene + camera + vòng lặp. Không chứa gì riêng của dự án. */
export class Engine {
  constructor(container, cam) {
    this.container = container;
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(cam.fov, 1, cam.near, cam.far);
    this.camera.position.set(...cam.start);

    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // giới hạn để máy yếu không lag
    this.renderer.shadowMap.enabled = true;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    container.appendChild(this.renderer.domElement);

    this.clock = new THREE.Clock();
    this._updaters = [];
    window.addEventListener('resize', () => this.resize());
    this.resize();
  }

  onUpdate(fn) { this._updaters.push(fn); }

  resize() {
    const w = this.container.clientWidth || window.innerWidth;
    const h = this.container.clientHeight || window.innerHeight;
    this.camera.aspect = w / h;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(w, h);
  }

  start() {
    this.renderer.setAnimationLoop(() => {
      const dt = Math.min(this.clock.getDelta(), 0.1); // chặn dt lớn khi đổi tab
      this._updaters.forEach((fn) => fn(dt));
      this.renderer.render(this.scene, this.camera);
    });
  }
}
