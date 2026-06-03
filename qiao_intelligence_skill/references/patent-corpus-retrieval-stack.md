# 中国专利数据库大规模检索栈（LLM 交互用）

适用场景：
- `/home/qiao/qiao_design/e_coli_model/5000万专利申请全量数据1985-2025/中国专利数据库.csv` 这类超大专利 CSV/表格库
- 目标是让 LLM 可以先做候选召回，再做细读，而不是每次直接读原始大文件

## 本次会话沉淀的有效做法

### 1. 先区分“物理行数”和“真实记录数”
该专利 CSV 中摘要/主权项含换行，因此 shell 统计到的 line count 会显著大于真实专利条数。

建议：
- 不要把 `wc -l` 或二进制换行计数当作真实记录数
- 真实条数应以 CSV 解析器读出的记录数为准

### 2. 第一层先做 LLM-friendly 文本压缩分片
不要直接让模型接触原始 98GB CSV。先生成按申请年份分片的 TSV：
- 只保留高价值字段：row_id, line_no, 申请号, 专利名称, 专利类型, 申请人, 申请人类型, 申请年份, 公开公告号, 公开公告年份, IPC主分类号, 发明人, 摘要精简, 主权项精简
- 摘要文本截断到约 220 字符
- 主权项内容截断到约 120 字符
- 按 `patents_YYYY.tsv` 分片

用途：
- 作为 LLM 首轮候选召回层
- 命中后可再回查原始 CSV

### 3. SQLite 层要做 Lean 版，不要把长文本全塞进去
对 5000 万级记录，SQLite 最稳妥的做法是：
- 主表只存核心元数据：row_id, line_no, app_no, title, patent_type, applicant, applicant_type, application_year, public_no, public_year, ipc_main, inventors
- FTS5 只覆盖：title, applicant, ipc_main
- 长文本留在 TSV 分片或原始 CSV 中回查

经验：
- 把摘要/主权项也大量塞入 SQLite + FTS，会导致数据库和 WAL 迅速膨胀
- 更好的结构是：SQLite 负责 candidate retrieval，TSV/原始 CSV 负责 detail fetch

### 4. Parquet 层非常适合作为下一层，而不是立刻全量做 dense embeddings
当 Phase-1 SQLite/FTS 已完成，下一步优先级通常是：
- 先把按年 TSV 转成 `year=YYYY/data.parquet`
- 作为 DuckDB-ready 的列式分析层
- 再根据专题或候选集做 dense embedding，而不是全库一次性 embedding

原因：
- Parquet 更适合大规模聚合、统计、筛选
- SQLite 更适合快速召回
- Dense index 更适合小范围高质量 rerank，不适合一开始就全库铺开

### 5. 推荐的多层检索路径
1. 用户问题进入编排层
2. 先用 SQLite/FTS 做 sparse candidate retrieval
3. 若需要统计/批量过滤，走 Parquet 层
4. 若需要文本细节，回查按年 TSV
5. 若需要完整上下文，再回原始 CSV
6. 只有在主题明确或候选集缩小后，才做 dense embedding / rerank

## 适合该项目的架构表达
- 原始层：`中国专利数据库.csv`
- 回查层：`中国专利数据库_llm_retrieval/by_year/*.tsv`
- 检索层：`中国专利数据库_phase1_stack/patent_metadata_lean.sqlite`
- 分析层：`中国专利数据库_parquet/year=YYYY/data.parquet`
- 编排层：Moshi / LangGraph / AutoGen 调用 SQLite、Parquet 和 TSV 回查脚本

## 脚本与产物命名约定
建议保留以下结构：
- `build_llm_retrieval_artifacts.py`：原始 CSV -> 年份 TSV 压缩层
- `build_patent_phase1_stack_lean.py`：TSV -> SQLite Lean + FTS5
- `query_patent_phase1.py`：FTS 查询入口
- `build_patent_parquet_layer.py`：TSV -> Parquet 年分区

## 易踩坑
- 不要把换行计数误当记录数
- 不要把所有长摘要/主权项都装进 SQLite FTS
- 不要在没有主题缩小的前提下直接做全库 dense embeddings
- DuckDB 不在环境里时，不要伪造 DuckDB 成品；先产出 DuckDB-ready Parquet 层

## 一句话原则
面对超大专利库时，优先构建“SQLite 稀疏召回 + Parquet 分析 + TSV 回查 + 原始 CSV 全文回查”的分层检索栈，再按专题补 dense vector 库。