/**
 * TODO (Sprint 4, frontend giao diện + backend): nút "Góp ý" mở form nhỏ.
 *  - Dùng createPanel() trong ui/components/Panel.js.
 *  - Gửi bằng ctx.api.sendFeedback({ name, message, poiId }).
 *  - Nếu ctx.api.online === false: ẩn nút hoặc báo "tạm thời không gửi được".
 */
export class FeedbackFeature {
  init(ctx) { this.ctx = ctx; }
  dispose() {}
}
