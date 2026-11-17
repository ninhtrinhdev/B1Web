import { App } from './app/App.js';

const app = new App({
  viewport: document.getElementById('viewport'),
  uiRoot: document.getElementById('ui'),
});
app.start();
