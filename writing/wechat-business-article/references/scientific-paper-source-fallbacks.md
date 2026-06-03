# Scientific paper source fallbacks for 公众号 adaptation

Use this note when a user provides a paper URL but the direct PDF is inaccessible from the current environment.

## Why this matters
For paper-based public writing, the real task is not `download exactly this URL`; the real task is `recover the correct paper and ground every claim in a verified source`. A dead link is often a transport problem, not a research dead end.

## Recommended fallback sequence
1. Confirm the paper identity
   - Extract or recover: title, authors, year, DOI, journal, and PMCID/PMID if available.
   - Do not switch mirrors before you know you are still talking about the same paper.

2. Prefer stable official full-text mirrors
   - DOI landing page or publisher landing page for canonical bibliographic confirmation.
   - Europe PMC / PubMed Central for open biomedical papers.
   - For Europe PMC, two especially useful endpoints are:
     - PDF mirror: `https://europepmc.org/articles/<PMCID>?pdf=render`
     - XML full text: `https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/fullTextXML`

3. Save both human-readable and machine-readable sources when possible
   - `paper.pdf`
   - `paper.xml` or equivalent structured full text

## Writing guidance
- Use the structured XML/full text for extracting abstract claims, table values, section logic, and caveats.
- Use the PDF for archival completeness and visual inspection.
- In the internal brief, document the original dead link and the verified fallback source.
- In the public article, do not mention transport failure unless it is relevant to the user; just keep the claims well grounded.

## Good fit
- PNAS / PMC-accessible biology papers
- User asks for download + summary + public-facing rewrite
- Direct PDF link hangs, times out, or hits anti-bot protection

## Session example pattern
A biohub-hosted PDF URL was inaccessible from the runtime. The paper identity was confirmed by title/DOI/PMCID, then the final assets were recovered from Europe PMC using:
- `?pdf=render` for the PDF
- `fullTextXML` for evidence extraction

This pattern is especially useful when the final deliverable requires exact headline numbers from tables.