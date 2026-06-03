# 超大专利 CSV 面向 LLM 的检索栈（Phase-1）

适用场景：
- 原始数据是超大专利 CSV（10^7 级记录）
- 用户明确要求“压缩后便于检索 / 用于 LLM 交互 / 适配 Moshi、LangGraph、AutoGen”
- 当前轮次更适合先落 sparse + metadata 检索层，而不是强行一次性做完整 dense 向量库

## 默认原则
1. 不覆盖原始 CSV。
2. 先做 retrieval-friendly 衍生层，而不是直接把原始大表喂给 LLM。
3. 优先交付可运行、可查询、可被编排层调用的脚本和数据库。
4. 若 dense embedding 全量构建超出单轮成本，必须明确写成“后续 Phase-2/3”，不要假装已经完成。

## 推荐 Phase-1 结构

### A. LLM-friendly TSV 分片层
从原始大 CSV 生成按申请年份切分的 TSV：
- `by_year/patents_1985.tsv`
- ...
- `by_year/patents_2025.tsv`

推荐保留字段：
- `row_id`
- `line_no`
- `申请号`
- `专利名称`
- `专利类型`
- `申请人`
- `申请人类型`
- `申请年份`
- `公开公告号`
- `公开公告年份`
- `IPC主分类号`
- `发明人`
- `摘要精简`
- `主权项精简`

推荐压缩策略：
- `摘要文本` 截断到 ~220 字符
- `主权项内容` 截断到 ~120 字符
- 长文本统一去掉换行/制表，标准化为空格

用途：
- 作为 LLM 首轮载入候选语料
- 作为 SQLite 进一步建库的数据来源
- 作为回查层，避免第一步就读取原始 10^7 级 CSV

## B. Lean SQLite + FTS5 元数据检索层
推荐数据库：
- `patent_metadata_lean.sqlite`

推荐主表字段：
- `row_id`
- `line_no`
- `app_no`
- `title`
- `patent_type`
- `applicant`
- `applicant_type`
- `application_year`
- `public_no`
- `public_year`
- `ipc_main`
- `inventors`

推荐 FTS5 字段：
- `title`
- `applicant`
- `ipc_main`

说明：
- 第一版故意不把长摘要/长主权项再塞进 SQLite，以控制数据库体积和建库时间
- 精简摘要/主权项保留在 TSV 层，用于命中后的二跳回查

用途：
- 首轮 sparse candidate retrieval
- 按年份、申请人、IPC 主类快速筛选
- 为 LangGraph/AutoGen/Moshi 暴露可调用检索工具

## 推荐查询流程
1. 用户提出问题
2. 先用 SQLite FTS 做首轮召回
3. 通过 `row_id` / `app_no` / `line_no` 回查按年 TSV
4. 若需要更长上下文，再回原始 CSV
5. 若主题复杂且候选集已收敛，再对子集做 dense rerank / embeddings

也就是：
- `SQLite FTS -> TSV 回查 -> 原始 CSV 回查 -> 可选 dense rerank`

## 与目标架构的对应关系

### 已完成的 Phase-1
- 高性能解析：CSV -> TSV 分片
- 核心元数据表格：SQLite
- Sparse RAG：FTS5
- 编排层就绪：查询脚本可封成 agent tool

### 留给 Phase-2/3 的部分
- DuckDB/Parquet 分析层
- 全库或专题 dense embedding
- FAISS/Chroma 向量索引
- 完整 LangGraph 工具链封装

## 典型交付物
- `build_llm_retrieval_artifacts.py`
- `build_patent_phase1_stack_lean.py`
- `query_patent_phase1.py`
- `中国专利数据库_llm_retrieval/manifest.json`
- `中国专利数据库_phase1_stack/manifest.json`
- 架构说明 markdown

## 写法要求
- 对用户要明确写出：当前已完成的是 Phase-1 检索栈
- 不要把“embedding-ready 语料”误写成“完整向量库已建成”
- 若 FTS 复杂语法与 IPC 含斜杠冲突，默认在查询脚本中做基础字符清洗/转义

## 对本用户的特别偏好
- 优先在项目目录下保存权威 markdown 说明文件
- 产物应可直接作为后续 LLM/agent 工作流的基础设施
- 强调“原始数据保留 + 衍生层分层检索”，而不是一次性 destructive 压缩