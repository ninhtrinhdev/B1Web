import './loading.css';

/** Màn hình chờ, nghe load:progress / world:ready. */
export class LoadingFeature {
  init({ bus, uiRoot }) {
    this.el = document.createElement('div');
    this.el.className = 'loading';
    this.el.innerHTML = '<p>Đang tải khuôn viên…</p><div class="loading__bar"><span></span></div>';
    uiRoot.appendChild(this.el);
    const bar = this.el.querySelector('span');
    this.off = [
      bus.on('load:progress', ({ loaded, total }) => { bar.style.width = `${(loaded / total) * 100}%`; }),
      bus.on('world:ready', () => this.el.classList.add('is-done')),
    ];
  }
  dispose() { this.off.forEach((f) => f()); this.el.remove(); }
}
