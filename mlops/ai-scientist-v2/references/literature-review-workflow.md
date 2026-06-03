# Literature Review Workflow — AI-Scientist-v2 + Semantic Scholar

## Overview

Using AI-Scientist-v2's Semantic Scholar integration to build comprehensive literature reviews for any research domain. This pattern was used to create a 301-paper review of protein hallucination/diffusion design methods.

## Workflow Steps

### 1. Create Topic Description

Write a markdown file defining the research scope (see `ai_scientist/ideas/protein_hallucination_design.md` as template):

```markdown
# Title: [Your Topic]
## Keywords
keyword1, keyword2, keyword3
## TL;DR
One-paragraph overview
## Abstract
Full scope description
## Key Research Questions
1. Question one
2. Question two
## Relevant Methods and Baselines
- Method A: description
- Method B: description
## Evaluation Dimensions
- Metric 1
- Metric 2
```

### 2. Multi-Query Search

Search with multiple keyword angles to maximize coverage. Each angle catches different papers:

```python
from ai_scientist.tools.semantic_scholar import search_for_papers
import time, json

queries = [
    ("core method name 1 description", "标签: 方法1"),
    ("core method name 2 description", "标签: 方法2"),
    ("application area keywords", "标签: 应用"),
    ("evaluation benchmark keywords", "标签: 评估"),
    ("recent year specific terms 2024 2025", "标签: 最新"),
]

all_papers = {}
for query, label in queries:
    results = search_for_papers(query, result_limit=15)
    if results:
        for p in results:
            pid = p.get('paperId', '')
            if pid and pid not in all_papers:
                all_papers[pid] = {
                    'title': p.get('title', ''),
                    'year': p.get('year'),
                    'venue': p.get('venue', ''),
                    'citationCount': p.get('citationCount', 0) or 0,
                    'url': p.get('url', ''),
                    'category': label,
                }
    time.sleep(1.1)  # Rate limit

sorted_papers = sorted(all_papers.values(),
    key=lambda x: x['citationCount'], reverse=True)
```

### 3. Fetch Abstracts for Key Papers

For the most important papers, fetch full abstracts via direct API:

```python
import requests, os

def get_paper_details(paper_id):
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}"
    params = {'fields': 'title,abstract,year,venue,citationCount,authors'}
    headers = {'X-API-KEY': os.environ.get('S2_API_KEY', '')}
    resp = requests.get(url, params=params, headers=headers)
    time.sleep(1.1)
    return resp.json() if resp.status_code == 200 else None

# Fetch details for top 20 papers
key_details = {}
for p in sorted_papers[:20]:
    details = get_paper_details(p['paperId'])
    if details:
        key_details[p['paperId']] = details
```

### 4. Structure the Review

Organize into sections:
- Method Taxonomy (classify papers by approach)
- Core Methods (detailed analysis of top 5-8 methods)
- Supporting Techniques (inverse folding, oracles, evaluation tools)
- Application Areas (binders, enzymes, symmetric assemblies, etc.)
- Evaluation Metrics & Benchmarks
- Experimental Validation Status
- Research Gaps & Opportunities
- Key References (sorted by citation count)

### 5. Save Outputs

```bash
# Save in AI-Scientist-v2 ideas directory
ai_scientist/ideas/<topic>_literature_review.md  # Full review
ai_scientist/ideas/<topic>_papers_raw.json       # Raw paper metadata

# Also save to project directory if relevant
/project/path/<topic>_literature_review.md
/project/path/<topic>_papers_raw.json
```

## Tips

- **Search breadth**: Use 10-15 different query angles. Each catches ~60-70% of relevant papers; overlap is expected and desirable.
- **Deduplication**: Always deduplicate by `paperId`, not title (same paper may appear under different titles).
- **Rate limiting**: S2 API allows 1 req/s with API key. Build in `time.sleep(1.1)` between calls.
- **False positives**: Semantic Scholar returns broad matches. Manually filter out irrelevant papers (e.g., non-protein "hallucination" papers).
- **Citation count context**: A 2025 paper with 10 citations may be more important than a 2022 paper with 50. Weight by recency + relevance, not just citations.

## Output Template

```markdown
# [Topic] — 文献综述

**生成时间**: YYYY-MM-DD
**数据来源**: Semantic Scholar API (N篇论文)

## 目录
1. 综述概要
2. 方法分类学
3. 核心方法详细分析
4. 配套技术
5. 应用方向
6. 评估指标与基准
7. 实验验证现状
8. 研究空白与机会
9. 关键参考文献
```
