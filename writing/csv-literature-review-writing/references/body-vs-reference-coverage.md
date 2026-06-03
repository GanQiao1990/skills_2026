# Body coverage vs reference-table coverage

Session lesson from revising a 300-paper Chinese review on de novo protein design hallucination.

Core failure mode:
- A draft can truthfully say it is "based on 300 papers"
- The reference table can list all 300 papers
- Yet the narrative body may only cite a subset
- This creates a credibility gap: bibliography completeness is mistaken for argumentative completeness

Minimal audit recipe:
1. Count CSV rows = N
2. Extract unique reference numbers from the body only (everything before the reference section)
3. Extract unique reference numbers from the reference table
4. Verify both counts equal N
5. Print missing numbers from the body and map them back to titles/categories before revising prose

Why this matters:
- Users often notice under-integration faster than missing bibliography rows
- In review writing, the complaint may be phrased as "why did you only use 50 papers?" even when the bibliography is much larger
- The real issue is usually that the body argument still relies on a representative subset rather than fully absorbing the evidence pool

Recommended fix pattern:
- Do not just append missing references randomly
- Add them where they sharpen the argument:
  - method-history paragraphs
  - boundary/exception paragraphs
  - application-specific evidence chains
  - evaluation/benchmark caveats
- Use the missing papers to correct blind spots in the narrative, not merely to satisfy counting

For this user:
- Prefer publication-grade Chinese markdown
- Organize review logic as an expert roadmap:
  problem framing -> method evolution -> application layers -> evidence calibration -> future directions
- Avoid a flat model/tool catalog tone
