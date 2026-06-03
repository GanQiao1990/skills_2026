# NarL 特定启动子（yeaR-yoaG、ogt、napF、dmsA）文献证据速查

适用场景：
- 用户要求为 NarL 在特定启动子上的机制性表述找“具体文章/数据支撑”；
- 需要把草稿中的强表述改写成有原始文献支持的版本；
- 需要区分“直接支持”“部分支持/系统层推断”“不宜直接写”。

## 一、最关键原始文献

### yeaR-yoaG
1. Lin HY, Bledsoe PJ, Stewart V. 2007. J Bacteriol 189(21):7539-7548.
   PMID: 17720788
   DOI: 10.1128/JB.00953-07
   直接支持：yeaR-yoaG 可由 phospho-NarL 在无 Fnr 参与时激活；NarL 位点中心约 -43.5；启动子对 nitrate/nitrite/NO 相关信号有响应。

2. Squire DJP et al. 2009. Biochem J 420(2):249-257.
   PMID: 19245365
   DOI: 10.1042/BJ20090183
   直接支持：yeaR 由 NarL alone 激活，位点中心约 -43.5；Fis 与 NarL 竞争，降低 yeaR/ogt 表达。

### ogt
1. Squire DJP et al. 2009. Biochem J 420(2):249-257.
   PMID: 19245365
   DOI: 10.1042/BJ20090183
   直接支持：ogt 属于 NarL alone 激活的 promoter；摘要给位点约 -45.5 和 -78.5（作图体系差异常见写成约 -44.5/-77.5）。

2. Ruanto R et al. 2020. Biochem J 477(15):2807-2824.
   PMID: 32662815
   DOI: 10.1042/BCJ20200408
   直接支持：ogt 启动子 NarL 位点在约 -44.5 和 -77.5；单个位点衍生体也可被 NarL 单独激活；激活涉及 NarL 与 RNAP α-CTD 相互作用。

### napF
1. Darwin AJ et al. 1998. J Bacteriol 180(16):4192-4198.
   PMID: 9696769
   DOI: 10.1128/JB.180.16.4192-4198.1998
   直接支持：napF 的 nitrate/nitrite activation 依赖 NarP 而非 NarL；NarL 对该激活具有 antagonistic 作用。

2. Potter LC et al. 2003. J Bacteriol 185(19):5862-5870.
   PMID: 13129959
   DOI: 10.1128/JB.185.19.5862-5870.2003
   直接支持：napF 对应低 nitrate 适应型周质 nitrate reductase；主启动子 P1 由 Fnr(-64.5) 与 phospho-NarP(-44.5) 协同激活；P2 受 phospho-NarP 与 phospho-NarL 抑制。

### dmsA / dmsABC
1. Bearson SMD et al. 2002. BMC Microbiol 2:13.
   PMID: 12079504
   DOI: 10.1186/1471-2180-2-13
   直接支持：dmsABC 在厌氧下受 Fnr 激活，在 nitrate 存在时受 NarL 抑制；NarL-phosphate 在 dmsA 启动子形成 97 bp footprint，重叠 Fnr 与 RNAP 识别区；机制上可干扰 Fnr/RNAP 进入。

2. Williams SB et al. 2000. Mol Microbiol 36(2):433-443.
   PMID: 11115116
   DOI: 10.1046/j.1365-2958.2000.02172.x
   直接支持：dmsA 是 FNR-dependent anaerobic promoter，说明 NarL 抑制发生在 Fnr 驱动的厌氧呼吸背景上。

## 二、推荐的证据分级口径

### 强支持
- yeaR-yoaG 可由 NarL 独立激活，无需 FNR。
- yeaR NarL 位点约 -43.5。
- ogt 是 NarL 直接激活的 DNA repair promoter，位点约 -44.5 与 -77.5。
- napF 主要由 Fnr + NarP 激活，而 NarL 对其起拮抗/抑制作用。
- dmsA/dmsABC 受 Fnr 激活、受 NarL-P 抑制，且 NarL-P footprint 与 Fnr/RNAP 区域重叠。

### 部分支持 / 系统层推断
- 高 nitrate 下，NarL 将 nitrate/nitrite 信号耦联到 NO/RNS 应答、DNA repair 与呼吸层级重排。
- napF 代表低 nitrate 适应策略，而 narGHJI 代表高 nitrate respiration 策略。
- dmsA 抑制会推动电子受体利用层级向 nitrate respiration 倾斜。

### 不宜直接写成既成事实
- “5–20 mM 是这些启动子的统一阈值窗口”
- “毫秒级启动”
- “napF 被彻底关闭 10–25 倍”
- “NarL-P 强行插入 +1/-10 轨道”
- “完全斩断 DMSO 呼吸 / 全电子流完全倒向 narGHJI”

## 三、默认优化写法

推荐总表述：
在 yeaR-yoaG 和 ogt 启动子上，现有原始研究表明 NarL-P 可在无需 FNR 共激活的条件下直接启动转录，其中 yeaR 的 NarL 结合中心位于约 -43.5，而 ogt 启动子具有位于约 -44.5 和 -77.5 的 NarL 靶位点。结合 yeaR-yoaG 的 nitrosative-stress 背景和 ogt 所编码的 O6-alkylguanine DNA alkyltransferase 功能，更稳妥的写法是：NarL 可将 nitrate/nitrite 信号直接耦联到应激防御与 DNA repair 模块，但不宜夸写成已有“毫秒级动力学”证明。

在 napF 启动子上，最直接的经典结论是 Fnr + NarP 协同激活，而 NarL 对其表现为拮抗/抑制；因此当 nitrate 从稀缺走向充足时，调控重心会从周质高亲和 nitrate reduction 策略转向膜结合 nitrate respiration。对 dmsA 而言，NarL-P 在一个与 Fnr 和 RNA polymerase 识别区重叠的 97 bp 区域形成广泛占位，从而显著抑制 Fnr-dependent anaerobic activation，体现不同电子受体之间的层级控制。