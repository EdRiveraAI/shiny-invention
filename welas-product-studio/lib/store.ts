import {DatabaseSync} from 'node:sqlite';
import {mkdirSync} from 'node:fs';
import {dirname, resolve} from 'node:path';

export type Row = {id: string; payload: string; revision: number};
export type SaveResult = {ok: true; revision: number} | {ok: false; error: string};

export const CONFLICT = 'This product changed since you opened it. Reload to see the latest version, then try again.';

/** Product records stored as JSON payloads, guarded by a per-record revision counter. */
export function openStore(file: string) {
  if (file !== ':memory:') mkdirSync(dirname(resolve(file)), {recursive: true});
  const db = new DatabaseSync(file);
  db.exec('CREATE TABLE IF NOT EXISTS products (id TEXT PRIMARY KEY, payload TEXT NOT NULL, revision INTEGER NOT NULL, updated_at TEXT NOT NULL)');
  const all = db.prepare('SELECT id, payload, revision FROM products ORDER BY rowid');
  const insert = db.prepare('INSERT OR IGNORE INTO products (id, payload, revision, updated_at) VALUES (?, ?, 1, ?)');
  const update = db.prepare('UPDATE products SET payload = ?, revision = revision + 1, updated_at = ? WHERE id = ? AND revision = ?');
  return {
    list: () => all.all().map(r => ({...r})) as Row[],
    /** `revision` is the revision the caller last saw; 0 means "I believe this is new". */
    save(id: string, payload: string, revision: number): SaveResult {
      const now = new Date().toISOString();
      const changed = revision === 0 ? insert.run(id, payload, now).changes : update.run(payload, now, id, revision).changes;
      return changed ? {ok: true, revision: revision + 1} : {ok: false, error: CONFLICT};
    },
    close: () => db.close(),
  };
}

let shared: ReturnType<typeof openStore> | undefined;
export const store = () => (shared ??= openStore(process.env.WELAS_DB || 'data/welas.db'));
