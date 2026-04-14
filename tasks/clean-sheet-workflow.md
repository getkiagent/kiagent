# Spec: Clean Sheet — n8n Workflow

**Zweck:** "Lead Pipeline" Sheet bereinigen — URLs normalisieren, Testzeilen löschen, Duplikate entfernen, Ergebnis zurückschreiben.  
**Trigger:** Manuell (On-Demand), mit optionalem `dry_run`-Flag.  
**Sheet:** `1OReC3rBa6bMImrw96dbTryW5LlB0SYWnbpn_t7x0-u0` → Tab "Lead Pipeline"

---

## Node-Reihenfolge

```
[1] Manual Trigger
      ↓
[2] Read All Rows          (Google Sheets)
      ↓
[3] Clean & Deduplicate    (Code)
      ↓
[4] IF: Dry Run?
      ├── true  → [5] Log Summary Only     (Code)
      └── false → [6] Clear Sheet          (Google Sheets)
                        ↓
                  [7] Write Cleaned Rows   (Google Sheets)
                        ↓
[8] Final Summary          (Code)   ← beide Branches laufen hier rein
```

---

## Node-Details

---

### [1] Manual Trigger

**Type:** `n8n-nodes-base.manualTrigger`  
**Zweck:** Workflow von Hand starten. Dry-run-Flag wird als Input-Field gesetzt.

**Konfiguration:**
- Field: `dry_run` (Boolean, Default: `true`)

> Warum Default `true`: Verhindert versehentliches Schreiben beim ersten Ausführen.

---

### [2] Read All Rows

**Type:** `n8n-nodes-base.googleSheets`  
**Operation:** `read`  
**Sheet:** GetKiAgent Lead Pipeline → Tab "Lead Pipeline"  
**Options:** `headerRow: true` (erste Zeile = Header, jeder Output-Item ist eine Datenzeile als Key-Value-Objekt)

**Output:** Ein Item pro Datenzeile. Felder: `url`, `status`, `score`, `tier`, `company_name`, `category`, `country`, `contact_email`, `pain_signals`, `speed_to_lead_signals`, `automation_opportunity`, `recommended_action`, `contact_options`, `confidence`, `uncertainty_notes`, `score_rationale`, `analyzed_at`.

---

### [3] Clean & Deduplicate

**Type:** `n8n-nodes-base.code` (Run Once for All Items)  
**Zweck:** Alle Bereinigungsschritte in einem Durchlauf.

```js
// ── Helpers ──────────────────────────────────────────────────────────────────

function normalizeUrl(raw) {
  if (!raw || !raw.trim()) return "";
  let url = raw.trim().toLowerCase();

  // Ensure https:// prefix
  if (!url.startsWith("http://") && !url.startsWith("https://")) {
    url = "https://" + url;
  }
  // http → https
  url = url.replace(/^http:\/\//, "https://");

  // Strip www.
  url = url.replace(/^(https:\/\/)www\./, "$1");

  // Strip trailing slash
  url = url.replace(/\/+$/, "");

  return url;
}

function getScore(item) {
  const raw = item.score || item["score"] || "";
  const n = parseFloat(String(raw).trim());
  return isNaN(n) ? 0 : n;
}

// ── Collect all rows ──────────────────────────────────────────────────────────

const rows = $input.all().map(i => ({ ...i.json }));
const rowsBefore = rows.length;

let removedEmpty = 0;
let removedTest = 0;
let removedDuplicates = 0;
const urlChanges = [];

// ── Step 1: Normalize URLs ────────────────────────────────────────────────────

for (const row of rows) {
  const raw = (row.url || "").trim();
  const normed = normalizeUrl(raw);
  if (normed !== raw) {
    urlChanges.push({ old: raw, new: normed });
    row.url = normed;
  }
}

// ── Step 2: Remove rows with empty URL ────────────────────────────────────────

const afterEmpty = rows.filter(r => (r.url || "").trim() !== "");
removedEmpty = rows.length - afterEmpty.length;

// ── Step 3: Remove test rows ──────────────────────────────────────────────────

const TEST_COMPANY_NAMES = ["PROBE WRITE 3"];
const TEST_CATEGORIES    = ["test"];

const afterTest = afterEmpty.filter(r => {
  const company  = (r.company_name || "").trim().toUpperCase();
  const category = (r.category || "").trim().toLowerCase();
  const isTest =
    TEST_COMPANY_NAMES.map(n => n.toUpperCase()).includes(company) ||
    TEST_CATEGORIES.includes(category);
  return !isTest;
});
removedTest = afterEmpty.length - afterTest.length;

// ── Step 4: Deduplicate by normalized URL (keep higher score) ─────────────────

const seen   = new Map();   // normalizedUrl → index in deduped[]
const deduped = [];

for (const row of afterTest) {
  const key = (row.url || "").trim();
  if (!key) {
    deduped.push(row);
    continue;
  }

  if (!seen.has(key)) {
    seen.set(key, deduped.length);
    deduped.push(row);
  } else {
    const existingIdx  = seen.get(key);
    const existingScore = getScore(deduped[existingIdx]);
    const newScore      = getScore(row);

    if (newScore > existingScore) {
      // Replace: new row has higher score
      deduped[existingIdx] = row;
    }
    // Either way: this is a duplicate
    removedDuplicates++;
  }
}

// ── Step 5: Remove trailing completely-empty rows ─────────────────────────────

while (deduped.length > 0) {
  const last = deduped[deduped.length - 1];
  const allEmpty = Object.values(last).every(v => v === "" || v === null || v === undefined);
  if (allEmpty) deduped.pop();
  else break;
}

// ── Build output ──────────────────────────────────────────────────────────────

const rowsAfter    = deduped.length;
const totalRemoved = rowsBefore - rowsAfter;
const dryRun       = !!$('Manual Trigger').first().json.dry_run;

return [{
  json: {
    dry_run:            dryRun,
    rows_before:        rowsBefore,
    rows_after:         rowsAfter,
    total_removed:      totalRemoved,
    removed_empty:      removedEmpty,
    removed_test:       removedTest,
    removed_duplicates: removedDuplicates,
    url_changes_count:  urlChanges.length,
    url_changes:        urlChanges.slice(0, 20),   // max 20 im Log
    cleaned_rows:       deduped,                   // full data for write-back
  }
}];
```

**Output:** Ein einzelnes Item mit allen Statistiken + `cleaned_rows` Array.

---

### [4] IF: Dry Run?

**Type:** `n8n-nodes-base.if`  
**Condition:** `{{ $json.dry_run }}` equals `true`

| Branch | Weiter zu |
|--------|-----------|
| true   | [5] Log Summary Only |
| false  | [6] Clear Sheet |

---

### [5] Log Summary Only *(Dry-Run Branch)*

**Type:** `n8n-nodes-base.code` (Run Once for All Items)  
**Zweck:** Gibt aus, was geändert würde — ohne zu schreiben.

```js
const d = $input.first().json;

console.log("=== DRY-RUN: Clean Sheet ===");
console.log(`Rows before : ${d.rows_before}`);
console.log(`Rows after  : ${d.rows_after}`);
console.log(`Total removed: ${d.total_removed}`);
console.log(`  – empty URL : ${d.removed_empty}`);
console.log(`  – test rows : ${d.removed_test}`);
console.log(`  – duplicates: ${d.removed_duplicates}`);
console.log(`URL changes   : ${d.url_changes_count}`);
if (d.url_changes && d.url_changes.length > 0) {
  for (const c of d.url_changes) {
    console.log(`  "${c.old}" → "${c.new}"`);
  }
}
console.log("=== No changes written ===");

return [{ json: { ...d, write_status: "dry_run_skipped" } }];
```

---

### [6] Clear Sheet *(Write Branch)*

**Type:** `n8n-nodes-base.googleSheets`  
**Operation:** `clear`  
**Sheet:** GetKiAgent Lead Pipeline → Tab "Lead Pipeline"  
**Range:** `A1:Z10000` (gesamtes Sheet leeren inkl. Header)

> Wichtig: Löscht alles. Node [7] schreibt Header + Daten neu.

---

### [7] Write Cleaned Rows *(Write Branch)*

**Type:** `n8n-nodes-base.code` + `n8n-nodes-base.googleSheets` — **zwei aufeinanderfolgende Nodes.**

#### [7a] Prepare Rows for Write

**Type:** `n8n-nodes-base.code` (Run Once for All Items)  
**Zweck:** `cleaned_rows` Array in einzelne Items umwandeln (Google Sheets `append` erwartet ein Item pro Zeile).

```js
const d = $input.first().json;
const rows = d.cleaned_rows || [];

// Pass stats through on first item so Final Summary can read them
return rows.map((row, idx) => ({
  json: {
    ...row,
    _stats: idx === 0 ? {
      rows_before:        d.rows_before,
      rows_after:         d.rows_after,
      total_removed:      d.total_removed,
      removed_empty:      d.removed_empty,
      removed_test:       d.removed_test,
      removed_duplicates: d.removed_duplicates,
      url_changes_count:  d.url_changes_count,
    } : null,
  }
}));
```

#### [7b] Append Rows to Sheet

**Type:** `n8n-nodes-base.googleSheets`  
**Operation:** `append`  
**Sheet:** GetKiAgent Lead Pipeline → Tab "Lead Pipeline"  
**Mapping:** autoMapInputData (alle Felder außer `_stats`)  
**Options:** `headerRow: true`

> Der erste Append-Call schreibt automatisch die Header-Zeile, weil `headerRow: true` aktiviert ist und das Sheet leer ist.

---

### [8] Final Summary

**Type:** `n8n-nodes-base.code` (Run Once for All Items)  
**Zweck:** Einheitlicher Abschluss-Log für beide Branches (Dry-Run und Write).

```js
const items = $input.all();

// Stats kommen entweder direkt (Dry-Run) oder über _stats des ersten Rows (Write)
let stats = items[0]?.json;
if (!stats.rows_before && items[0]?.json?._stats) {
  stats = items[0].json._stats;
}

const mode = stats.write_status === "dry_run_skipped" ? "DRY-RUN" : "WRITTEN";

console.log(`=== Clean Sheet: ${mode} ===`);
console.log(`Rows before  : ${stats.rows_before}`);
console.log(`Rows after   : ${stats.rows_after}`);
console.log(`Total removed: ${stats.total_removed}`);
console.log(`  – empty URL : ${stats.removed_empty}`);
console.log(`  – test rows : ${stats.removed_test}`);
console.log(`  – duplicates: ${stats.removed_duplicates}`);
console.log(`URL normalized: ${stats.url_changes_count}`);
console.log("=== Done ===");

return [{ json: { mode, ...stats } }];
```

---

## Duplikat-Logik im Detail

```
Für jede Zeile (nach URL-Normalisierung):
  key = normalisierte URL

  IF key noch nicht gesehen:
    → Zeile in deduped[] aufnehmen
    → seen.set(key, index)

  ELSE (key bereits vorhanden):
    existingScore = score der bereits aufgenommenen Zeile
    newScore      = score der aktuellen Zeile

    IF newScore > existingScore:
      → deduped[existingIdx] ersetzen (neuere/bessere Zeile gewinnt)
    ELSE:
      → aktuelle Zeile verwerfen

    removedDuplicates++
```

**Score-Parsing:** `parseFloat(String(score).trim())`. Leerer String, `null`, oder nicht-numerischer Wert → Score 0. Bei Score-Gleichstand bleibt die zuerst gesehene Zeile.

---

## URL-Normalisierung im Detail

| Input | Output |
|-------|--------|
| `WWW.Example.DE/` | `https://example.de` |
| `http://shop.de` | `https://shop.de` |
| `example.de` | `https://example.de` |
| `https://www.brand.at/` | `https://brand.at` |
| `HTTPS://BRAND.DE` | `https://brand.de` |

Schritte in Reihenfolge:
1. `.trim().toLowerCase()`
2. Falls kein `http://` / `https://` → `https://` voranstellen
3. `http://` → `https://`
4. `https://www.` → `https://`
5. Trailing `/` entfernen

---

## Dry-Run Verhalten

| Schritt | Dry-Run | Live |
|---------|---------|------|
| Sheet lesen | ✓ | ✓ |
| URL normalisieren | ✓ (im Speicher) | ✓ (im Speicher) |
| Zeilen filtern | ✓ (im Speicher) | ✓ (im Speicher) |
| Deduplizieren | ✓ (im Speicher) | ✓ (im Speicher) |
| Sheet leeren | ✗ | ✓ |
| Zeilen zurückschreiben | ✗ | ✓ |
| Statistik ausgeben | ✓ | ✓ |

Das IF-Node prüft `dry_run` aus dem Manual Trigger. Beim ersten Test immer `dry_run: true` setzen.

---

## Offene Punkte vor Implementierung

1. **Clear-Operation**: n8n Google Sheets Node v4.7 unterstützt `clear` — muss beim Bauen verifiziert werden. Fallback: HTTP Request an Sheets API `batchClear`.
2. **Header beim Append**: Wenn `headerRow: true` beim Append nicht automatisch schreibt → manuell einen Header-Row-Item voranstellen in Node [7a].
3. **`_stats` Cleanup**: `_stats` Feld darf nicht ins Sheet geschrieben werden → in Node [7b] Felder explizit mappen oder `_stats` vor dem Append herausfiltern.
