/** Panel cạnh phải – dùng cho info-panel, hướng dẫn, cài đặt. */
export function createPanel(parent, { title = '' } = {}) {
  const el = document.createElement('aside');
  el.className = 'panel';
  el.hidden = true;
  el.innerHTML = `<header class="panel__head"><h2></h2><button class="panel__close" aria-label="Đóng">×</button></header>
    <div class="panel__body"></div>`;
  const h2 = el.querySelector('h2');
  h2.textContent = title;
  el.querySelector('.panel__close').onclick = () => { el.hidden = true; };
  parent.appendChild(el);
  return {
    el,
    body: el.querySelector('.panel__body'),
    open(t) { if (t) h2.textContent = t; el.hidden = false; },
    close() { el.hidden = true; },
  };
}
