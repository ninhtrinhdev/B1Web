import GUI from 'lil-gui';

/** Bảng chỉnh thông số khi mở URL có ?debug */
export function setupDebug({ world, bus }) {
  const gui = new GUI({ title: 'Debug' });
  gui.add(world.lights.sun, 'intensity', 0, 6).name('Nắng');
  gui.add(world.lights.hemi, 'intensity', 0, 3).name('Trời');
  gui.add({ walk: () => bus.emit('nav:mode', 'walk') }, 'walk').name('Thử chế độ đi bộ');
  gui.add({ orbit: () => bus.emit('nav:mode', 'orbit') }, 'orbit').name('Về chế độ xoay');
  return gui;
}
