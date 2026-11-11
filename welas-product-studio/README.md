# Welas Product Studio

A private workspace for planning, producing, and launching Welas Early Learning resources:
curriculum volumes, supporting products, production stages, file deliverables, marketplace
listings, weekly priorities, and reusable templates.

## Run it

```bash
npm install
```

```bash
npm run dev
```

Then open http://localhost:3000. For a production run, use `npm run build` followed by `npm start`.

Requires Node.js 22.13 or newer (it uses Node's built-in SQLite).

## Where things live

| Path | What it is |
|---|---|
| `app/page.tsx` | The whole interface |
| `app/data.ts` | Stages, statuses, marketplaces, checklists, templates, and the 13 starter volumes — edit these lists to match your process |
| `app/api/products/route.ts` | Loads and saves product records |
| `lib/store.ts` | SQLite storage |
| `app/globals.css` | Styles |

## Your data

Saved products are written to `data/welas.db` (set `WELAS_DB` to use another location). That
folder is not committed to git, so back it up yourself — or use the download button in the top
bar to export every record as JSON.

Each record carries a revision number. If the same product is saved from two tabs, the second
save is refused instead of silently overwriting the first.

The app has no sign-in. Run it on your own computer or behind something that handles access;
don't put it on the open internet as is.

## Tests

```bash
npm test
```
