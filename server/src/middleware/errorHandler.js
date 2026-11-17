/** Lỗi nào chưa bắt ở route thì về đây: log ra console, trả JSON gọn cho client. */
export function errorHandler(err, _req, res, _next) {
  const status = err.status ?? 500;
  if (status >= 500) console.error(err);
  res.status(status).json({ error: status >= 500 ? 'Lỗi máy chủ' : err.message });
}

export function httpError(status, message) {
  return Object.assign(new Error(message), { status });
}
