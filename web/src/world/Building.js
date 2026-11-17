import * as THREE from 'three';
import { latLonToWorld } from './geo.js';

/** Một tòa nhà: đọc data JSON, nạp .glb, đặt đúng vị trí trên bản đồ khuôn viên. */
export class Building {
  constructor(data) {
    this.data = data;
    this.id = data.id;
    this.root = new THREE.Group();
    this.root.name = `Building_${data.id}`;
    this.colliders = [];   // mesh COL_* – dùng cho đi bộ
    this.cameras = {};     // Cam_* từ Blender – dùng cho tour
    this.poiAnchors = {};  // POI_* từ Blender
  }

  async load(assets) {
    try {
      const gltf = await assets.loadGLTF(this.data.model);
      this.root.add(gltf.scene);
      gltf.scene.traverse((o) => {
        if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; }
        if (o.name.startsWith('COL_')) { o.visible = false; this.colliders.push(o); }
        if (o.name.startsWith('POI_')) this.poiAnchors[o.name] = o;
      });
      gltf.cameras.forEach((c) => { this.cameras[c.name] = c; });
    } catch (err) {
      console.warn(`[${this.id}] chưa có model, dùng khối tạm.`, err.message);
      const [w, h, d] = this.data.placeholder?.size ?? [20, 20, 20];
      const box = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), new THREE.MeshStandardMaterial({ color: 0xdddddd }));
      box.position.y = h / 2;
      box.castShadow = true;
      this.root.add(box);
      this.colliders.push(box);
    }
    const { lat, lon } = this.data.origin;
    this.root.position.copy(latLonToWorld(lat, lon));
    this.root.rotation.y = THREE.MathUtils.degToRad(this.data.rotationDeg ?? 0);
    return this;
  }
}
