import * as THREE from 'three';
import { CONFIG } from '../app/config.js';

// Cùng công thức với blender/b1/osm.py -> make_projector, để Blender và web khớp nhau.
const KY = 110574.0;
const kx = (lat0) => 111320.0 * Math.cos((lat0 * Math.PI) / 180);

/** lat/lon -> Vector3 Three.js (x = đông, y = 0, z = nam), tính từ CAMPUS_ORIGIN. */
export function latLonToWorld(lat, lon, origin = CONFIG.CAMPUS_ORIGIN) {
  const east = (lon - origin.lon) * kx(origin.lat);
  const north = (lat - origin.lat) * KY;
  return new THREE.Vector3(east, 0, -north);
}

/** Ngược lại, dùng cho minimap / hiện tọa độ. */
export function worldToLatLon(v, origin = CONFIG.CAMPUS_ORIGIN) {
  return { lat: origin.lat - v.z / KY, lon: origin.lon + v.x / kx(origin.lat) };
}
