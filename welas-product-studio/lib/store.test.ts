import test from 'node:test';
import assert from 'node:assert/strict';
import {openStore} from './store.ts';

test('saves a new record at revision 1 and lists it', () => {
  const s = openStore(':memory:');
  assert.deepEqual(s.save('a', '{"t":1}', 0), {ok: true, revision: 1});
  assert.deepEqual(s.list(), [{id: 'a', payload: '{"t":1}', revision: 1}]);
});

test('updates bump the revision', () => {
  const s = openStore(':memory:');
  s.save('a', '1', 0);
  assert.deepEqual(s.save('a', '2', 1), {ok: true, revision: 2});
  assert.equal(s.list()[0].payload, '2');
});

test('a stale revision is rejected and leaves the record untouched', () => {
  const s = openStore(':memory:');
  s.save('a', '1', 0);
  s.save('a', '2', 1);
  assert.equal(s.save('a', 'stale', 1).ok, false);
  assert.equal(s.save('a', 'dupe-create', 0).ok, false);
  assert.equal(s.save('missing', 'x', 3).ok, false);
  assert.deepEqual(s.list(), [{id: 'a', payload: '2', revision: 2}]);
});
