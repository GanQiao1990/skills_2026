# Metrics vs experimental validation for scientific 公众号 framing

Use this reference when adapting papers for Chinese public-facing writing and the framing risks overstating what a benchmark metric means.

## Core rule
Do not let a model-evaluation metric masquerade as physical validation.

## Benchmark / model-evaluation metrics
These quantify prediction quality or ranking quality under a benchmark protocol. They are important, but they are not themselves experimental evidence.

Common examples:
- DockQ — complex-structure quality metric against a reference complex structure
- LDDT / pLDDT — local structure quality metric / confidence proxy
- ipTM / pTM — predicted interface/global structural confidence
- pass rate — fraction of benchmark cases exceeding a threshold
- perplexity — language-model token prediction quality
- AUC / AUROC / F1 / accuracy / top-k hit rate — standard supervised metrics

Recommended wording:
- "复合体预测质量评价指标"
- "benchmark 评价指标"
- "模型效果量化指标"
- "结构预测成绩单"

Avoid wording like:
- "这是物理模型"
- "这等于实验验证"
- "这已经证明真实生物学成立"

## Stronger physical / experimental evidence
When the user asks for a title or angle around 可验证 / 物理现实 / 实验验证, prefer these anchors if the paper contains them:
- cryo-EM / X-ray / NMR structure validation
- BLI / SPR / ITC binding assays
- competition / epitope assays
- selectivity against homologs or off-target panels
- cell-based functional assays
- animal experiments / in vivo efficacy

Recommended wording:
- "被结构实验反向验证"
- "被亲和力与功能实验验证"
- "进入实验可验证阶段"
- "不仅能预测，而且能被实验检验"

## Framing pattern
Bad:
- "DockQ 证明这个模型已经进入物理现实。"

Better:
- "DockQ 显示模型在复合体 benchmark 上预测质量较高；而 cryo-EM、BLI 和细胞功能实验则把部分结果推进到了更接近物理现实的验证层。"

## Title selection heuristic
If a paper has one subsystem that actually carries the verifiable breakthrough, foreground that subsystem in the title.

Example:
- Prefer "ESMFold2 的真正突破..." over a vague umbrella title about all ESM components when the strongest evidence chain is concentrated in ESMFold2.
