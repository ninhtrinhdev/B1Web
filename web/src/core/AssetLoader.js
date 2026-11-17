import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';

/** Nạp model/JSON, báo tiến độ qua bus, nhớ đệm để không tải 2 lần. */
export class AssetLoader {
  constructor(bus) {
    this.manager = new THREE.LoadingManager();
    this.manager.onProgress = (_url, loaded, total) => bus.emit('load:progress', { loaded, total });
    this.manager.onLoad = () => bus.emit('load:done');
    const draco = new DRACOLoader(this.manager);
    // Bộ giải nén Draco lấy từ CDN; muốn chạy offline thì chép
    // node_modules/three/examples/jsm/libs/draco/ vào public/draco/ và đổi đường dẫn.
    draco.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.7/');
    this.gltf = new GLTFLoader(this.manager).setDRACOLoader(draco);
    this.cache = new Map();
  }

  loadGLTF(url) {
    if (!this.cache.has(url)) this.cache.set(url, this.gltf.loadAsync(url));
    return this.cache.get(url);
  }

  async loadJSON(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Không tải được ${url} (${res.status})`);
    return res.json();
  }
}
