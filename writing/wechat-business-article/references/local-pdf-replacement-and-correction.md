# Local PDF replacement and correction pattern

Use this when the user says the previously used paper/source was wrong and they replaced the file locally, often under the same filename.

## Trigger signs
- "you got the wrong paper"
- "we replaced the right paper as ..."
- repeated absolute path pasted several times
- request to rewrite the article after a local file swap
- user proposes a new title/theme after correcting the source

## Required correction behavior
1. Invalidate prior source identity
   - Do not trust the old URL, DOI, title, or abstract just because they were already extracted.
   - Same filename does not imply same paper.

2. Re-identify from the local file itself
   - Pull metadata title/author.
   - Read page 1 title/authors/abstract.
   - Extract a fresh text layer and rebuild the evidence chain from the actual PDF.

3. Reframe the article from the corrected evidence base
   - Do not recycle old-paper narrative structure if it changes the scientific claim.
   - Rebuild headline claim, proof chain, and caveats from scratch.

4. Handle malformed repeated path strings gracefully
   - If the user pasted something like `/a/b.pdf/a/b.pdf/a/b.pdf` but it clearly points to one real local PDF, normalize to the intended path and proceed without a clarification round.

5. When the user proposes the title/theme
   - First judge whether the framing matches the paper’s real evidence.
   - If yes, preserve the user’s angle and rewrite toward it.
   - Fix obvious typo-level mistakes silently when confidence is high, e.g. `白质语言模型` -> `蛋白质语言模型`.
   - Prefer a slightly hedged scientific title when the framing is strong but not absolute, e.g. turn a hard claim into a question-led title.

## Recommended public-facing framing for this failure mode
- Start by acknowledging the correction plainly.
- Make the new article about the corrected paper, not about your prior mistake.
- Use the evidence chain that is strongest in the corrected PDF, even if it differs substantially from the earlier draft.

## Useful evidence types for 'can this model be validated?' angles
- structural agreement with experiment (RMSD, cryo-EM/X-ray)
- binding measurements (BLI/SPR/Kd)
- epitope competition or selectivity vs homologs
- cell-based functional readouts (IC50, rescue, reporter assays)
- scaling relationships tied to physical prediction metrics
