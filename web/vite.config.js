import { defineConfig } from 'vite';
import { resolve } from 'node:path';

export default defineConfig({
  base: './',                       // deploy vào thư mục con (GitHub Pages) vẫn chạy
  server: {
    open: true,
    // Khi dev: mọi request /api/... chuyển sang server Express ở cổng 3000
    proxy: { '/api': 'http://localhost:3000' },
  },
  build: {
    rollupOptions: {
      input: {
        main: resolve(import.meta.dirname, 'index.html'),
        admin: resolve(import.meta.dirname, 'admin/index.html'),
      },
    },
  },
});
