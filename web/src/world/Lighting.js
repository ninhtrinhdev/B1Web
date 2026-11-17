import * as THREE from 'three';

export function createLighting(scene) {
  scene.background = new THREE.Color(0xa9c4e8);
  scene.fog = new THREE.Fog(0xa9c4e8, 300, 1500);
  const hemi = new THREE.HemisphereLight(0xdfeaff, 0x8a8478, 1.2);
  // Hướng nắng theo scene.py của Blender: từ đông-bắc, cao (bắc = -z).
  const sun = new THREE.DirectionalLight(0xffffff, 2.5);
  sun.position.set(45, 160, -55);
  sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -120, right: 120, top: 120, bottom: -120, far: 400 });
  scene.add(hemi, sun);
  return { hemi, sun };
}
