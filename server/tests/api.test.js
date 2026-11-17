import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { openDb } from '../src/db/connection.js';
import { seed } from '../src/db/seed.js';
import { createApp } from '../src/app.js';

let server, base;
before(async () => {
  const db = openDb(':memory:');
  seed(db);
  server = createApp(db).listen(0);
  await new Promise((ok) => server.once('listening', ok));
  base = `http://localhost:${server.address().port}/api`;
});
after(() => server.close());

test('health', async () => {
  const res = await fetch(`${base}/health`);
  assert.equal(res.status, 200);
});

test('campus liệt kê b1', async () => {
  const data = await (await fetch(`${base}/campus`)).json();
  assert.ok(data.buildings.includes('b1'));
});

test('building b1 có đúng hình dạng frontend cần', async () => {
  const b = await (await fetch(`${base}/buildings/b1`)).json();
  assert.equal(b.id, 'b1');
  assert.equal(typeof b.origin.lat, 'number');
  assert.ok(Array.isArray(b.pois));
});

test('tòa nhà không tồn tại -> 404', async () => {
  assert.equal((await fetch(`${base}/buildings/zz`)).status, 404);
});

test('gửi góp ý rỗng -> 400', async () => {
  const res = await fetch(`${base}/feedback`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: '' }),
  });
  assert.equal(res.status, 400);
});

test('xem góp ý không có token -> 401', async () => {
  assert.equal((await fetch(`${base}/feedback`)).status, 401);
});
