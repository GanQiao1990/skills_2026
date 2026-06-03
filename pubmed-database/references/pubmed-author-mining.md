# PubMed Author-Based Literature Mining Patterns

Reusable patterns for systematic PubMed literature mining by author, extracted from session analysis of 910+ papers.

## Key Pitfalls

### 1. Author Name Format (CRITICAL)
PubMed uses **last-name-first** format. Common mistake:
- ❌ `"Liming Liu"[Author]` → returns cardiac surgeons, wrong field
- ✅ `"Liu Liming"[Author]` → returns the metabolic engineering researcher

Always verify name format by fetching a known PMID first:
```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=KNOWN_PMID&retmode=xml" | grep -i "LastName\|ForeName"
```

### 2. Author Disambiguation via Affiliation
For common names, add affiliation filter:
```
"Liu Liming"[Author] AND "Jiangnan University"[Affiliation]
"Lee Sang Yup"[Author] AND "KAIST"[Affiliation]
```

### 3. Rate Limits
- Without API key: 3 requests/second
- With API key: 10 requests/second
- Always sleep 0.35s between requests without key
- Fetch in batches of 50 PMIDs (efetch max)

## Reusable Workflow: Author Research Summary

### Step 1: Search with Disambiguation
```python
# esearch with affiliation filter for common names
query = '"AuthorName"[Author]'
if affiliation:
    query += f' AND "{affiliation}"[Affiliation]'
```

### Step 2: Batch Fetch All Papers
```python
# efetch in batches of 50
batch_size = 50
for i in range(0, len(pmids), batch_size):
    batch = pmids[i:i+batch_size]
    # fetch XML, parse article metadata + abstracts
```

### Step 3: Parse Article XML
Key fields to extract:
- PMID, Title, Authors (LastName + ForeName)
- Journal, Year, Abstract (with Labels)
- DOI, Keywords

### Step 4: Export Multi-Format
- CSV: One row per paper, all fields, UTF-8-sig for Excel
- Markdown: Structured report with year distribution, journals, keywords
- JSON: Raw data for programmatic access

## CSV Export Pattern
```python
import csv
fieldnames = ["author", "pmid", "title", "authors", "journal", "year",
              "abstract", "doi", "keywords", "link"]
with open(path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
```

## Strategy Extraction Patterns

### Gene Name Extraction
```python
# Common E. coli gene names: 3-5 lowercase letters
gene_pattern = re.compile(r'\b([a-z]{3,5}[A-Z]?)\b')
```

### Manipulation Context
```python
knockout_words = {'deletion', 'knockout', 'knocked out', 'deleted', 'disrupted', 'Δ'}
overexpress_words = {'overexpression', 'overexpressed', 'amplified', 'enhanced expression'}
```

### Production Titer Extraction
```python
titer_pattern = re.compile(r'(\d+\.?\d*)\s*(g/L|g·L⁻¹|g l⁻¹)\b', re.IGNORECASE)
```

## Amino Acid Biosynthesis Gene Reference

### Knockout Targets (competition blocking)
- ldhA (lactate), pta-ackA (acetate), adhE (ethanol), pflB (formate)
- frdABCD (succinate), sucA (TCA), ppc (OAA)

### Regulatory Derepression
- trpR (Trp), tyrR (Tyr), argR (Arg), thrR (Thr), metJ (Met)

### Overexpression Targets (precursor supply)
- aroG/F/H (DAHP synthase), thrA (Asp kinase), lysC (Asp kinase III)
- pntAB/sthA (NADPH), zwf/gnd (PPP)

### Transporters
- lysE (Lys), rhtA (Thr), brnQ (BCAA), yddG (aromatic AA)
