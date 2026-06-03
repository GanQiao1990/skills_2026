# Literature-to-Proposal Integration Workflow

Using AI-Scientist-v2's Semantic Scholar tool for systematic proposal research.

## When to use

- User has a research proposal that needs literature strengthening
- Need to identify competitors, gaps, and supporting evidence
- Want to find the latest 2024-2026 publications in a field

## Workflow

### Step 1: Extract key topics from the proposal

Read the proposal and identify 8-14 search queries covering:
- Core technical approaches (e.g. "de novo protein design metabolic engineering")
- Key biological systems (e.g. "NtrB NtrC nitrogen responsive")
- Methodology keywords (e.g. "circular permutation protein switch")
- Named researchers (e.g. "Liming Liu Corynebacterium glutamicum")
- Application domains (e.g. "amino acid fermentation")

### Step 2: Run searches via Semantic Scholar

```python
import sys, time, json
sys.path.insert(0, "/path/to/AI-Scientist-v2")
from dotenv import load_dotenv
load_dotenv("/path/to/.env", override=True)
from ai_scientist.tools.semantic_scholar import SemanticScholarSearchTool

tool = SemanticScholarSearchTool()
queries = [
    ("search query 1", "label 1"),
    ("search query 2", "label 2"),
    # ...
]

all_results = {}
for query, label in queries:
    papers = tool.search_for_papers(query)
    if papers:
        for i, p in enumerate(papers[:5]):
            title = p.get("title", "?")
            year = p.get("year", "?")
            cites = p.get("citationCount", 0)
            authors = ", ".join([a.get("name","?") for a in p.get("authors",[])][:3])
            abstract = (p.get("abstract","") or "")[:150]
            print(f"  [{i+1}] ({year}, {cites} cites) {title}")
    all_results[label] = papers
    time.sleep(1.1)  # respect 1 req/sec rate limit
```

### Step 3: Analyze results into categories

Organize papers into:
1. **Direct competitors** — same mechanism, different application
2. **Strong support** — validates the proposal's direction
3. **Method tools** — enables the proposal's approach
4. **Background context** — establishes the field

For each, assess:
- How similar is it to the proposal?
- What's the key difference?
- Does it strengthen or threaten the proposal?

### Step 4: Write competitive landscape section

Structure as:
- **Most direct competitor**: Cite + clearly differentiate (molecular vs systems level)
- **Supporting breakthroughs**: Latest findings that validate the approach
- **Technology window**: Why NOW is the right time
- **Method maturity**: What tools are now available
- **Gap confirmation**: What remains unaddressed

### Step 5: Integrate citations throughout the proposal

Don't just add a references section. Weave citations into:
- **Background** paragraph — field-level validation
- **Research approach** section — timing justification
- **Expected results** section — comparison benchmarks
- **Innovation points** — differentiation from existing work

### Step 6: Add DOIs/journal details to key references

```
Author et al. (Year) Title. *Journal* Volume: Pages. DOI: xxx. N cites.
```

## Output template

```markdown
## Competition Landscape & Differentiation

**Most direct competitor**: [Citation] — [mechanism]. KEY DIFFERENCE: [X focuses on
molecular-level Y, this proposal focuses on systems-level Z].

**Supporting breakthrough**: [Citation] — [finding]. SUPPORTS: [proposal's direction
for Q1/Q2].

**Technology window**: [Multiple citations] — [tools/methods now mature].

**Gap confirmed**: No existing work integrates [A] + [B] + [C] into [D].
```

## Pitfalls

1. **Don't just list papers** — analyze them for competitive threat vs support
2. **Don't ignore 2025-2026 preprints** — they may be the closest competitors
3. **Rate limit is 1 req/sec** — the tool enforces this automatically
4. **Abstracts may be empty** — some papers have no abstract in S2
5. **Citation counts lag** — 2025-2026 papers will have low counts, don't dismiss them
