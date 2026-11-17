import { CONFIG } from './config.js';
import { Engine } from '../core/Engine.js';
import { EventBus } from '../core/EventBus.js';
import { AssetLoader } from '../core/AssetLoader.js';
import { ApiClient } from '../core/ApiClient.js';
import { World } from '../world/World.js';
import { LoadingFeature } from '../features/loading/LoadingFeature.js';
import { NavigationFeature } from '../features/navigation/NavigationFeature.js';
import { HotspotFeature } from '../features/hotspots/HotspotFeature.js';
import { InfoPanelFeature } from '../features/info-panel/InfoPanelFeature.js';
import { TourFeature } from '../features/tour/TourFeature.js';
import { MinimapFeature } from '../features/minimap/MinimapFeature.js';
import { FeedbackFeature } from '../features/feedback/FeedbackFeature.js';
import { setupDebug } from '../shared/debug.js';

/**
 * App = nơi DUY NHẤT biết toàn bộ các mảnh. Nó tạo phần lõi, rồi đăng ký từng feature.
 * Muốn tắt một chức năng: comment dòng tương ứng trong FEATURES.
 */
const FEATURES = [
  LoadingFeature,
  NavigationFeature,
  HotspotFeature,
  InfoPanelFeature,
  TourFeature,
  MinimapFeature,
  FeedbackFeature,
];

export class App {
  constructor({ viewport, uiRoot }) {
    this.bus = new EventBus();
    this.engine = new Engine(viewport, CONFIG.CAMERA);
    this.assets = new AssetLoader(this.bus);
    this.api = new ApiClient(CONFIG);
    this.world = new World(this.engine.scene, this.assets, this.api, this.bus);
    // ctx là "túi đồ nghề" truyền cho mọi feature
    this.ctx = { config: CONFIG, bus: this.bus, engine: this.engine, assets: this.assets, api: this.api, world: this.world, uiRoot };
    this.features = FEATURES.map((F) => new F());
  }

  async start() {
    for (const f of this.features) f.init(this.ctx);
    this.engine.onUpdate((dt) => this.features.forEach((f) => f.update?.(dt)));
    this.engine.start();
    if (CONFIG.DEBUG) setupDebug(this.ctx);
    await this.world.load();
    this.api.trackVisit();
    this.bus.emit('world:ready', this.world);
  }
}
