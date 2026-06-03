# NarL 项目：基于本地 PPTX 对齐 proposal / scientific thought 的写法

适用场景：当用户要求“based on 本地 .pptx 优化 proposal / summary”，尤其在 `/home/qiao/qiao_design/narl_project` 下处理 `proposal_nbt_binder_platform_*` 一类文件时。

## 先做什么
1. 先提取 PPTX 文字内容，不要只凭已有 proposal 改写。
2. 先识别 PPT 的主线与页面层次，再去改 markdown 文件。
3. 对项目级写作任务，优先写入项目根目录 `DEBUG.md`，不要把记录散落到子目录。

## 本次会话提炼出的 PPT 主线
PPT 的总主线是：
设计 → 筛选 → 调控 → 感知

### 研究背景建议顺序
1. 蛋白 de novo 设计正逐步成为生物学/医学中的主流工具
   - 计算能力提升
   - AlphaFold2 / RoseTTAFold 等模型发展
   - 新结构、组装体、binder 三类经典问题已接近解决
2. 现有蛋白设计方法仍有共同瓶颈：要么慢，要么易错
   - diffusion / BindCraft：慢、算力重、候选压缩差
   - ProteinHunter / RSO / HalluDesign：快，但容易出现模型偏好、自证偏差或跨模型不稳定
3. 合成生物学传统调控方式的不足
   - 静态粗放
   - 难随状态精准响应
   - 泄漏表达高、串扰强、跨底盘移植性差
4. 由此引出：需要基于 de novo 设计的 protein-level regulatory elements

## proposal 中应如何落地
### 总体定位
不要只写成“binder 工程平台”，要更明确落在：
- de novo 蛋白设计方法
- 高效筛选策略
- 功能元件设计
- 合成生物学应用控制系统

### 部署层拆分规则
在研究逻辑/技术路线里，不要把这两项揉成一句：
- 精氨酸胁迫下的 S/T/Y 磷酸化调控
- NarQ–NarL 介导的生长—生产动态控制

应拆成两个独立编号部分，再把 ppGpp 放到单独反馈层。

### scientific thought summary 的写法
summary 不应只是 proposal 的压缩复制版；应显式加入“研究背景与概念切入”段，回答三件事：
1. 为什么 de novo 设计现在成立
2. 为什么现有方法还不够
3. 为什么传统合成生物学调控不够，因此需要 protein-level programmable elements

## 可直接复用的短句
- 蛋白 de novo 设计正逐步从结构生物学中的概念验证工具，转变为生物学与医学中可广泛调用的功能元件生成平台。
- 当前领域真正困难的已不是获得更多候选，而是以较低成本获得少量真正值得进入湿实验、并能进一步部署为细胞内功能元件的高质量设计。
- 对合成生物学而言，传统调控方式仍主要依赖静态过表达、基因敲除或固定强度的转录调节，普遍存在调控粗放、泄漏高、串扰强和可移植性不足等局限。
- 本项目的整体逻辑遵循“设计 → 筛选 → 调控 → 感知”的主线。