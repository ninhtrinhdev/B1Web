import { httpError } from '../middleware/errorHandler.js';

/** Kiểm tra chuỗi bắt buộc, cắt khoảng trắng, giới hạn độ dài. */
export function requireText(value, field, max = 2000) {
  if (typeof value !== 'string' || !value.trim()) throw httpError(400, `Thiếu ${field}`);
  if (value.length > max) throw httpError(400, `${field} dài quá ${max} ký tự`);
  return value.trim();
}

export function optionalText(value, field, max = 2000) {
  return value == null || value === '' ? null : requireText(value, field, max);
}
