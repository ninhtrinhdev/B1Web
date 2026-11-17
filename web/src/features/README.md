# features/ – module chức năng

Mỗi thư mục = 1 chức năng, có 1 file `XxxFeature.js` export class với:
```js
init(ctx)    // ctx = { config, bus, engine, assets, api, world, uiRoot }
update(dt)   // tùy chọn, gọi mỗi khung hình
dispose()    // gỡ sự kiện, xóa DOM
```
Không import feature khác. Cần phối hợp → phát/nghe sự kiện trên `ctx.bus` (danh sách ở `core/EventBus.js`).
CSS riêng của feature để cạnh nó (`hotspots.css`) và import trong file JS.

| Feature | Trạng thái | Phụ trách |
|---|---|---|
| loading | chạy được (bản tối thiểu) | |
| navigation | orbit chạy được, walk = TODO | |
| hotspots | TODO | |
| info-panel | TODO | |
| tour | TODO | |
| minimap | TODO | |
| feedback | TODO (cần backend) | |
