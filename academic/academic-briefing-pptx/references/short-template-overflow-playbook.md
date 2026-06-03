# Short-template overflow playbook

Use this note when the user wants a finished PPTX based on a provided template, but the template has only a few slides and tight text boxes.

## Situation pattern
- Source content is a proposal / scientific summary with real logical depth.
- Template has only 3–4 slides with one or two reusable content layouts.
- User still wants a complete deck in that style, not a text outline.

## Reliable workflow
1. Extract the source narrative first.
   - Separate completed work from hypotheses.
   - Identify the pivot mechanism node if one exists.

2. Inventory the template.
   - markitdown for visible text
   - inventory.py for exact shape map

3. Expand the deck by duplication.
   - Reuse cover/content/closing slides with rearrange.py.
   - Keep a clean executive sequence such as:
     1) title
     2) background
     3) research logic
     4) method
     5) strategy/comparison
     6) mechanism pivot
     7) application 1
     8) application 2
     9) application 3
     10) conclusion

4. Write to shape capacity, not to source-document richness.
   - Slide titles: one line if possible.
   - Summary line: one sentence only.
   - Three-column content: 2–3 short lines per column.
   - Bottom conclusion strip: one compact conclusion sentence.

5. If replace.py reports overflow worsening:
   - shorten wording before shrinking font
   - remove connector phrases first
   - compress mixed Chinese/English lines
   - trim repeated modifiers like `进一步` `系统性` `可用于` unless they carry meaning
   - only then shrink font size

6. Acceptable fallback
- If a few low-priority boxes remain slightly tight after compression, save a readable draft and tell the user it is a template-constrained version, then offer a second-pass readability optimization.

## Wording patterns that fit narrow boxes well
- `已完成方法与实验验证`
- `建立 ClpX 相关筛选策略`
- `先机制解析，再精准干预`
- `状态监测，不承担反馈控制`
- `拟动态协调与验证，不表述为已完成重编程`

## Important narrative safeguard
For proposal-stage academic decks, keep these distinctions explicit:
- `已完成 / 已建立 / 已验证`
- `拟探索 / 初步猜想 / 方法设想 / 后续验证`

This protects scientific credibility in senior-expert reporting.
