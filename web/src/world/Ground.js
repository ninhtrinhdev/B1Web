import * as THREE from 'three';

export function createGround(scene, size = 600) {
  const mesh = new THREE.Mesh(
    new THREE.PlaneGeometry(size, size),
    new THREE.MeshStandardMaterial({ color: 0x8f8a80, roughness: 0.95 })
  );
  mesh.rotation.x = -Math.PI / 2;
  mesh.receiveShadow = true;
  mesh.name = 'Ground';
  scene.add(mesh);
  return mesh;
}
