# NarL 启动子级文献证据：支持范围与可安全外推的边界

本参考文件用于处理以下类型问题：
- 用户给出 `yeaR-yoaG`、`ogt`、`napF`、`dmsA` 等 NarL/FNR/NarP 启动子文献；
- 用户追问这些启动子级证据是否足以支持“增强 NarL-P 促进氨基酸合成/增产”；
- 需要把启动子级直接证据与代谢/产量层外推严格分层。

## 一、启动子级直接支持

### `yeaR-yoaG`
强支持：
- NarL-P 可在无需 FNR 共激活时直接激活；
- 结合位点中心约 `-43.5`；
- 与 nitrate/nitrite/NO 诱导背景有关。

核心文献：
- Lin HY et al. 2007. J Bacteriol. PMID: 17720788. DOI: 10.1128/JB.00953-07.
- Squire DJP et al. 2009. Biochem J. PMID: 19245365. DOI: 10.1042/BJ20090183.

### `ogt`
强支持：
- NarL 直接激活；
- 位点约在 `-44.5` 与 `-77.5`；
- 单个位点衍生体也可被 NarL 激活；
- `ogt` 编码 O6-alkylguanine DNA alkyltransferase，属于 DNA repair 模块。

核心文献：
- Squire DJP et al. 2009. PMID: 19245365.
- Ruanto R et al. 2020. Biochem J. PMID: 32662815. DOI: 10.1042/BCJ20200408.

### `napF`
强支持：
- 低 nitrate 适应型周质 nitrate reductase 系统；
- 主体是 `Fnr + NarP` 激活；
- NarL 对其表现为 antagonize / antagonistic effect。

核心文献：
- Darwin AJ et al. 1998. J Bacteriol. PMID: 9696769. DOI: 10.1128/JB.180.16.4192-4198.1998.
- Potter LC et al. 2003. J Bacteriol. PMID: 13129959. DOI: 10.1128/JB.185.19.5862-5870.2003.

### `dmsA / dmsABC`
强支持：
- `dmsABC` 在厌氧下由 Fnr 激活，在 nitrate 存在时由 NarL 抑制；
- NarL-P 在与 Fnr/RNAP 识别区重叠的 97 bp 区域形成 footprint；
- 机制上可视为多分子占位干扰 Fnr/RNAP 进入。

核心文献：
- Bearson SMD et al. 2002. BMC Microbiol. PMID: 12079504. DOI: 10.1186/1471-2180-2-13.
- Williams SB et al. 2000. Mol Microbiol. PMID: 11115116. DOI: 10.1046/j.1365-2958.2000.02172.x.

## 二、只能间接支持的内容

这些文献可间接支持：
- NarL-P 重排 nitrate-responsive respiratory hierarchy；
- NarL-P 接入 NO/RNS 应答与 DNA repair；
- NarL-P 压制替代电子受体呼吸支路；
- 这些变化可能改善后期 redox context、stress buffering 与生理稳定性。

但这些文献**不能直接证明**：
- NarL-P 直接激活氨基酸生物合成主通路基因；
- 增强 NarL-P 本身就直接提高氨基酸通量；
- NarL-P 越高越好。

## 三、默认收口表述

最安全表述：
“这些启动子级文献不能直接证明 NarL-P 直接促进氨基酸生物合成，但它们强烈支持 NarL-P 会重排 nitrate-responsive respiration、stress buffering 和替代呼吸支路控制；因此可将 NarL-P 视为后期动态控制器，从而间接支持氨基酸生产改善的机制假设。”

禁用强表述：
- “增强 NarL-P 可直接促进氨基酸合成”
- “NarL-P 直接激活氨基酸主通路”
- “NarL-P 越强越增产”
- “这些启动子文献已经证明 NarL 增产”
