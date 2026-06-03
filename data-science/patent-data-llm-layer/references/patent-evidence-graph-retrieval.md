# Patent evidence-graph retrieval pattern

Use this when a patent QA/reporting system retrieves whole documents reasonably well but produces weakly grounded answers.

## Trigger
- Patent search returns plausible records, but summaries are generic or hallucination-prone.
- The user wants explicit evidence citations, not just a source list.
- You need to compare an old retrieval path vs a new one on a fixed query set.

## Core upgrade pattern
1. Keep the existing document-level sparse retrieval as candidate generation.
2. Enrich candidates with full compact fields from Parquet or the richer storage layer.
3. Split each patent into evidence chunks:
   - title -> one chunk
   - abstract -> sentence-aware overlapping chunks
   - main claim -> sentence-aware overlapping chunks
4. Build a lightweight graph over chunks:
   - adjacent chunks within the same field are neighbors
   - title chunk links to the first abstract/claim chunks
   - optionally reward a chunk when neighbors also contain query terms
5. Score chunks independently, then propagate chunk scores back to patent scores.
6. Feed the LLM an evidence graph context, not just concatenated abstracts.

## Why this works
- Patent-level ranking often overweights generic but popular words.
- Chunk-level scoring lets a narrowly relevant claim or abstract passage rescue a patent that would otherwise rank low.
- Explicit chunk IDs give the LLM a stable citation handle.

## Recommended context shape
For each patent:
- patent number
- title
- applicant
- year
- IPC
- top 1-3 evidence chunks with:
  - chunk_id
  - field label (标题 / 摘要 / 主权项)
  - score
  - text
  - optional neighbor IDs

Example citation format in prompts/output:
`[证据: CN202410340174.6 | CN202410340174.6::title::0 | 标题]`

## Prompt rules that improved grounding
Use a system prompt that says:
- answer only from the provided evidence graph
- every key claim must carry a citation in the fixed schema
- do not invent patent numbers, applicants, chunk IDs, or unstated mechanism details
- if evidence is insufficient, explicitly say so
- avoid expanding from general domain knowledge when the evidence does not support it

## Evaluation script pattern
Ship a simple CLI evaluator that outputs JSON with:
- query
- old_top_ids
- new_top_ids
- overlap
- new_only_ids
- evidence_chunk_count
- top_evidence: chunk_id, patent number, field, score, text preview

Also compute summary metrics across the query set:
- avg_old_results
- avg_new_results
- avg_overlap
- avg_evidence_chunks

## Query-set lesson
For retrieval evaluation, natural-language user questions may be too loose. Keep a retrieval-friendly keyword query set (e.g. `GLP-1R 激动剂`, `NarL 硝酸盐 调控`) even if the front-end still accepts natural-language questions.

## Common pitfall
If top evidence chunks are mostly titles, the chunk scorer may still be too lexical. Add more weight to abstract/claim chunks when title-only hits are broad and generic.
